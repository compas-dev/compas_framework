"""Validate, retrieve, and install immutable COMPAS candidate artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from email.message import Message
from email.parser import BytesParser
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any
from xml.etree import ElementTree

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.tags import Tag
from packaging.tags import parse_tag
from packaging.utils import canonicalize_name
from packaging.utils import parse_wheel_filename
from packaging.version import Version

SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
PLACEHOLDER = re.compile(r"(?:change[-_ ]?me|placeholder|todo|example|0{12,})", re.IGNORECASE)
SUPPORTED_TARGET = ("ubuntu-24.04", "linux", "x86_64", "3.12")
LIVE_DISTRIBUTIONS = frozenset({"compas", "compas-occ", "compas-cgal", "compas-libigl"})
LIVE_REPOSITORIES = {
    "compas": "compas-dev/compas",
    "compas-occ": "compas-dev/compas_occ",
    "compas-cgal": "compas-dev/compas_cgal",
    "compas-libigl": "compas-dev/compas_libigl",
}
LIVE_ARTIFACT_NAMES = {
    "compas": "candidate-linux-py312",
    "compas-occ": "candidate-linux-py312",
    "compas-cgal": "wheels-manylinux",
    "compas-libigl": "wheels-manylinux",
}
LIVE_WORKFLOW_PATH = ".github/workflows/build.yml"


class CandidateError(ValueError):
    """Raised when candidate provenance or artifact content is invalid."""


@dataclass(frozen=True)
class Target:
    runner: str
    os: str
    architecture: str
    python: str


@dataclass(frozen=True)
class Workflow:
    run_id: int
    run_attempt: int
    path: str
    event: str
    pull_request: int | None
    base_ref: str | None


@dataclass(frozen=True)
class Artifact:
    id: int
    name: str
    archive_sha256: str


@dataclass(frozen=True)
class Wheel:
    filename: str
    sha256: str


@dataclass(frozen=True)
class Candidate:
    distribution: str
    version: Version
    repository: str
    commit: str
    workflow: Workflow
    artifact: Artifact
    wheel: Wheel
    depends_on: tuple[str, ...]


@dataclass(frozen=True)
class Manifest:
    schema_version: int
    target: Target
    packages: tuple[Candidate, ...]

    @property
    def by_name(self) -> dict[str, Candidate]:
        return {candidate.distribution: candidate for candidate in self.packages}


def _mapping(value: object, name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise CandidateError(f"{name} must be an object with string keys")
    return value


def _sequence(value: object, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise CandidateError(f"{name} must be an array")
    return value


def _required_string(mapping: dict[str, Any], key: str, context: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise CandidateError(f"{context}.{key} must be a nonempty string")
    if PLACEHOLDER.search(value):
        raise CandidateError(f"{context}.{key} contains a placeholder")
    return value


def _positive_integer(mapping: dict[str, Any], key: str, context: str) -> int:
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CandidateError(f"{context}.{key} must be a positive integer")
    return value


def _exact_keys(mapping: dict[str, Any], expected: set[str], context: str) -> None:
    unexpected = sorted(set(mapping) - expected)
    missing = sorted(expected - set(mapping))
    if unexpected or missing:
        raise CandidateError(f"{context} fields differ from schema: missing={missing!r}, unexpected={unexpected!r}")


def _digest(value: str, context: str) -> str:
    digest = value.removeprefix("sha256:")
    if not SHA256.fullmatch(digest) or PLACEHOLDER.search(digest):
        raise CandidateError(f"{context} must be a complete lowercase SHA-256 digest")
    return digest


def parse_manifest(data: object, *, require_live_set: bool = False) -> Manifest:
    """Parse and validate a candidate manifest."""

    root = _mapping(data, "manifest")
    _exact_keys(root, {"schema_version", "target", "packages"}, "manifest")
    if root.get("schema_version") != 1:
        raise CandidateError("schema_version must be 1")

    target_data = _mapping(root.get("target"), "target")
    _exact_keys(target_data, {"runner", "os", "architecture", "python"}, "target")
    target = Target(
        runner=_required_string(target_data, "runner", "target"),
        os=_required_string(target_data, "os", "target"),
        architecture=_required_string(target_data, "architecture", "target"),
        python=_required_string(target_data, "python", "target"),
    )
    if (target.runner, target.os, target.architecture, target.python) != SUPPORTED_TARGET:
        raise CandidateError(f"target must be the initial supported target {SUPPORTED_TARGET!r}")

    packages_data = _sequence(root.get("packages"), "packages")
    if not packages_data:
        raise CandidateError("packages must not be empty")

    candidates: list[Candidate] = []
    names: set[str] = set()
    repositories: set[str] = set()
    artifact_ids: set[tuple[str, int]] = set()
    for index, item in enumerate(packages_data):
        context = f"packages[{index}]"
        package = _mapping(item, context)
        _exact_keys(
            package,
            {"distribution", "version", "repository", "commit", "workflow", "artifact", "wheel", "depends_on"},
            context,
        )
        distribution = canonicalize_name(_required_string(package, "distribution", context))
        if distribution in names:
            raise CandidateError(f"duplicate package {distribution!r}")
        names.add(distribution)

        repository = _required_string(package, "repository", context)
        if not REPOSITORY.fullmatch(repository):
            raise CandidateError(f"{context}.repository must be owner/name")
        if repository in repositories:
            raise CandidateError(f"duplicate repository {repository!r}")
        repositories.add(repository)

        version_text = _required_string(package, "version", context)
        try:
            version = Version(version_text)
        except Exception as error:
            raise CandidateError(f"{context}.version is invalid") from error

        commit = _required_string(package, "commit", context)
        if not COMMIT.fullmatch(commit):
            raise CandidateError(f"{context}.commit must be a full lowercase commit SHA")

        workflow_data = _mapping(package.get("workflow"), f"{context}.workflow")
        _exact_keys(
            workflow_data,
            {"run_id", "run_attempt", "path", "event", "pull_request", "base_ref"},
            f"{context}.workflow",
        )
        event = _required_string(workflow_data, "event", f"{context}.workflow")
        if event not in {"pull_request", "push", "workflow_dispatch"}:
            raise CandidateError(f"{context}.workflow.event is unsupported")
        pull_request = workflow_data.get("pull_request")
        base_ref = workflow_data.get("base_ref")
        if event == "pull_request":
            if isinstance(pull_request, bool) or not isinstance(pull_request, int) or pull_request <= 0:
                raise CandidateError(f"{context}.workflow.pull_request must be positive for a pull_request run")
            if not isinstance(base_ref, str) or not base_ref:
                raise CandidateError(f"{context}.workflow.base_ref is required for a pull_request run")
        elif pull_request is not None or base_ref is not None:
            raise CandidateError(f"{context}.workflow pull_request/base_ref fields are only valid for pull_request runs")
        workflow = Workflow(
            run_id=_positive_integer(workflow_data, "run_id", f"{context}.workflow"),
            run_attempt=_positive_integer(workflow_data, "run_attempt", f"{context}.workflow"),
            path=_required_string(workflow_data, "path", f"{context}.workflow"),
            event=event,
            pull_request=pull_request,
            base_ref=base_ref,
        )
        if not workflow.path.startswith(".github/workflows/") or not workflow.path.endswith((".yml", ".yaml")):
            raise CandidateError(f"{context}.workflow.path must identify a workflow file")

        artifact_data = _mapping(package.get("artifact"), f"{context}.artifact")
        _exact_keys(artifact_data, {"id", "name", "archive_sha256"}, f"{context}.artifact")
        artifact = Artifact(
            id=_positive_integer(artifact_data, "id", f"{context}.artifact"),
            name=_required_string(artifact_data, "name", f"{context}.artifact"),
            archive_sha256=_digest(
                _required_string(artifact_data, "archive_sha256", f"{context}.artifact"),
                f"{context}.artifact.archive_sha256",
            ),
        )
        artifact_key = (repository, artifact.id)
        if artifact_key in artifact_ids:
            raise CandidateError(f"duplicate artifact ID {artifact.id} in {repository}")
        artifact_ids.add(artifact_key)

        wheel_data = _mapping(package.get("wheel"), f"{context}.wheel")
        _exact_keys(wheel_data, {"filename", "sha256"}, f"{context}.wheel")
        wheel = Wheel(
            filename=_required_string(wheel_data, "filename", f"{context}.wheel"),
            sha256=_digest(_required_string(wheel_data, "sha256", f"{context}.wheel"), f"{context}.wheel.sha256"),
        )
        try:
            parsed_name, parsed_version, _, _ = parse_wheel_filename(wheel.filename)
        except Exception as error:
            raise CandidateError(f"{context}.wheel.filename is invalid") from error
        if canonicalize_name(parsed_name) != distribution or parsed_version != version:
            raise CandidateError(f"{context}.wheel filename does not match distribution/version")

        dependencies = _sequence(package.get("depends_on"), f"{context}.depends_on")
        normalized_dependencies: list[str] = []
        for dependency in dependencies:
            if not isinstance(dependency, str) or not dependency:
                raise CandidateError(f"{context}.depends_on entries must be nonempty strings")
            normalized = canonicalize_name(dependency)
            if normalized == distribution:
                raise CandidateError(f"{distribution!r} cannot depend on itself")
            if normalized in normalized_dependencies:
                raise CandidateError(f"duplicate dependency {normalized!r} for {distribution!r}")
            normalized_dependencies.append(normalized)

        candidates.append(
            Candidate(
                distribution=distribution,
                version=version,
                repository=repository,
                commit=commit,
                workflow=workflow,
                artifact=artifact,
                wheel=wheel,
                depends_on=tuple(normalized_dependencies),
            )
        )

    manifest = Manifest(schema_version=1, target=target, packages=tuple(candidates))
    _topological_candidates(manifest)
    if require_live_set and set(manifest.by_name) != LIVE_DISTRIBUTIONS:
        raise CandidateError(f"live manifest must contain exactly {sorted(LIVE_DISTRIBUTIONS)!r}")
    if require_live_set:
        for distribution, repository in LIVE_REPOSITORIES.items():
            candidate = manifest.by_name[distribution]
            if candidate.repository != repository:
                raise CandidateError(f"live manifest repository for {distribution!r} must be {repository!r}")
            if candidate.artifact.name != LIVE_ARTIFACT_NAMES[distribution]:
                raise CandidateError(f"live manifest artifact name for {distribution!r} is not approved")
            if candidate.workflow.path != LIVE_WORKFLOW_PATH or candidate.workflow.event != "pull_request":
                raise CandidateError(f"live manifest workflow for {distribution!r} must be the protected pull-request build")
    return manifest


def load_manifest(path: Path, *, require_live_set: bool = False) -> Manifest:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CandidateError(f"cannot read candidate manifest {path}: {error}") from error
    return parse_manifest(data, require_live_set=require_live_set)


def _topological_candidates(manifest: Manifest) -> tuple[Candidate, ...]:
    by_name = manifest.by_name
    for candidate in manifest.packages:
        unknown = sorted(set(candidate.depends_on) - set(by_name))
        if unknown:
            raise CandidateError(f"{candidate.distribution!r} has unknown dependencies: {unknown!r}")

    result: list[Candidate] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            raise CandidateError("candidate dependency graph contains a cycle")
        if name in visited:
            return
        visiting.add(name)
        for dependency in by_name[name].depends_on:
            visit(dependency)
        visiting.remove(name)
        visited.add(name)
        result.append(by_name[name])

    for name in sorted(by_name):
        visit(name)
    return tuple(result)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _single_metadata(archive: zipfile.ZipFile, suffix: str) -> tuple[str, Message]:
    matches = [name for name in archive.namelist() if name.endswith(suffix)]
    if len(matches) != 1:
        raise CandidateError(f"wheel must contain exactly one {suffix.rsplit('/', 1)[-1]} file")
    return matches[0], BytesParser().parsebytes(archive.read(matches[0]))


def _native_members(names: Iterable[str]) -> list[str]:
    return [name for name in names if name.lower().endswith((".so", ".pyd", ".dylib"))]


def _target_compatible(tag: Tag, target: Target) -> bool:
    if target != Target(*SUPPORTED_TARGET):
        return False
    if tag.platform == "any":
        return tag.abi == "none" and tag.interpreter in {"py3", "py312", "cp312"}
    manylinux = re.fullmatch(r"manylinux_(\d+)_(\d+)_x86_64", tag.platform)
    compatible_platform = tag.platform == "linux_x86_64" or (manylinux is not None and (int(manylinux.group(1)), int(manylinux.group(2))) <= (2, 39))
    compatible_python = (tag.interpreter == "cp312" and tag.abi in {"abi3", "cp312", "none"}) or (tag.interpreter in {"py3", "py312"} and tag.abi == "none")
    return compatible_platform and compatible_python


def verify_wheel(path: Path, candidate: Candidate, manifest: Manifest) -> None:
    """Verify one selected wheel against its manifest and dependency entries."""

    if path.name != candidate.wheel.filename:
        raise CandidateError(f"expected wheel {candidate.wheel.filename!r}, found {path.name!r}")
    if sha256_file(path) != candidate.wheel.sha256:
        raise CandidateError(f"wheel digest mismatch for {path.name}")
    try:
        parsed_name, parsed_version, _, filename_tags = parse_wheel_filename(path.name)
    except Exception as error:
        raise CandidateError(f"invalid wheel filename {path.name!r}") from error
    if canonicalize_name(parsed_name) != candidate.distribution or parsed_version != candidate.version:
        raise CandidateError(f"wheel filename does not match manifest for {candidate.distribution}")

    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        metadata_path, metadata = _single_metadata(archive, ".dist-info/METADATA")
        wheel_metadata_path, wheel_metadata = _single_metadata(archive, ".dist-info/WHEEL")
        record = [name for name in names if name.endswith(".dist-info/RECORD")]
        if len(record) != 1:
            raise CandidateError("wheel must contain exactly one RECORD file")
        native_members = _native_members(names)

    metadata_root = metadata_path.split("/", 1)[0]
    wheel_metadata_root = wheel_metadata_path.split("/", 1)[0]
    record_root = record[0].split("/", 1)[0]
    if metadata_root != wheel_metadata_root or metadata_root != record_root or not metadata_root.endswith(".dist-info"):
        raise CandidateError("wheel metadata files must share one dist-info directory")
    try:
        dist_info_name, dist_info_version = metadata_root.removesuffix(".dist-info").rsplit("-", 1)
        valid_dist_info = canonicalize_name(dist_info_name) == candidate.distribution and Version(dist_info_version) == candidate.version
    except Exception:
        valid_dist_info = False
    if not valid_dist_info:
        raise CandidateError("wheel dist-info directory does not match manifest")

    if canonicalize_name(metadata.get("Name", "")) != candidate.distribution:
        raise CandidateError("wheel METADATA name does not match manifest")
    try:
        metadata_version = Version(metadata.get("Version", ""))
    except Exception as error:
        raise CandidateError("wheel METADATA version is invalid") from error
    if metadata_version != candidate.version:
        raise CandidateError("wheel METADATA version does not match manifest")
    requires_python = metadata.get("Requires-Python")
    if not requires_python or not SpecifierSet(requires_python).contains(Version(manifest.target.python), prereleases=True):
        raise CandidateError(f"wheel Requires-Python does not accept {manifest.target.python}")

    wheel_tag_values = wheel_metadata.get_all("Tag", [])
    try:
        wheel_tags = frozenset(tag for value in wheel_tag_values for tag in parse_tag(value))
    except Exception as error:
        raise CandidateError("wheel contains an invalid WHEEL tag") from error
    if wheel_tags != filename_tags:
        raise CandidateError("WHEEL tags do not exactly match filename tags")
    if native_members and any(tag.platform == "any" for tag in filename_tags):
        raise CandidateError("native wheel content must not use the any platform tag")
    if candidate.distribution in {"compas-cgal", "compas-libigl"} and not native_members:
        raise CandidateError(f"{candidate.distribution} candidate wheel contains no native extension")
    if not any(_target_compatible(tag, manifest.target) for tag in filename_tags):
        raise CandidateError(f"wheel {path.name!r} is incompatible with the manifest target")

    try:
        requirements = [Requirement(value) for value in metadata.get_all("Requires-Dist", [])]
    except Exception as error:
        raise CandidateError("wheel contains invalid Requires-Dist metadata") from error
    candidate_requirements: dict[str, Requirement] = {}
    for requirement in requirements:
        name = canonicalize_name(requirement.name)
        if name not in manifest.by_name:
            continue
        if name in candidate_requirements:
            raise CandidateError(f"{candidate.distribution} has duplicate candidate requirement {name}")
        if requirement.marker is not None:
            raise CandidateError(f"{candidate.distribution} candidate requirement {name} must be unconditional")
        candidate_requirements[name] = requirement
    if set(candidate_requirements) != set(candidate.depends_on):
        raise CandidateError(
            f"{candidate.distribution} candidate requirements do not match depends_on: metadata={sorted(candidate_requirements)!r}, manifest={sorted(candidate.depends_on)!r}"
        )
    for dependency in candidate.depends_on:
        requirement = candidate_requirements[dependency]
        selected = manifest.by_name[dependency]
        if requirement.specifier and not requirement.specifier.contains(selected.version, prereleases=True):
            raise CandidateError(f"{candidate.distribution} requirement {requirement} rejects selected {dependency} {selected.version}")


def _safe_zip_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members: list[zipfile.ZipInfo] = []
    for member in archive.infolist():
        path = PurePosixPath(member.filename)
        mode = member.external_attr >> 16
        if path.is_absolute() or ".." in path.parts or member.is_dir() or stat.S_ISLNK(mode):
            raise CandidateError(f"unsafe or non-file artifact member {member.filename!r}")
        members.append(member)
    return members


def extract_single_wheel(archive_path: Path, destination: Path, expected_filename: str) -> Path:
    """Safely extract the single expected wheel from an Actions artifact."""

    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path) as archive:
        members = _safe_zip_members(archive)
        if len(members) != 1 or PurePosixPath(members[0].filename).name != expected_filename:
            raise CandidateError("candidate artifact must contain exactly the selected wheel")
        output = destination / expected_filename
        with archive.open(members[0]) as source, output.open("wb") as target:
            shutil.copyfileobj(source, target)
    return output


class _CrossHostAuthorizationRedirect(urllib.request.HTTPRedirectHandler):
    """Drop the GitHub token before following a redirect to object storage."""

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        redirected = super().redirect_request(request, file_pointer, code, message, headers, new_url)
        if redirected is not None:
            original = urllib.parse.urlsplit(request.full_url)
            destination = urllib.parse.urlsplit(new_url)
            if destination.scheme != "https":
                raise urllib.error.HTTPError(new_url, code, "artifact redirect must use HTTPS", headers, file_pointer)
            if (destination.scheme, destination.netloc) != (original.scheme, original.netloc):
                redirected.remove_header("Authorization")
        return redirected


class GitHubClient:
    def __init__(self, token: str, api_url: str = "https://api.github.com") -> None:
        if not token:
            raise CandidateError("a GitHub App token is required for retrieval")
        self.token = token
        self.api_url = api_url.rstrip("/")

    def _request(self, url: str, *, accept: str = "application/vnd.github+json") -> urllib.request.Request:
        return urllib.request.Request(
            url,
            headers={
                "Accept": accept,
                "Authorization": f"Bearer {self.token}",
                "User-Agent": "compas-framework-candidate-verifier",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    def json(self, path: str) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(self._request(f"{self.api_url}/{path.lstrip('/')}"), timeout=30) as response:
                value = json.load(response)
        except (OSError, urllib.error.HTTPError, json.JSONDecodeError) as error:
            raise CandidateError(f"GitHub API request failed for {path}: {error}") from error
        return _mapping(value, f"GitHub response {path}")

    def download(self, url: str, destination: Path) -> None:
        try:
            opener = urllib.request.build_opener(_CrossHostAuthorizationRedirect())
            with opener.open(self._request(url, accept="application/octet-stream"), timeout=60) as response:
                with destination.open("wb") as stream:
                    shutil.copyfileobj(response, stream)
        except (OSError, urllib.error.HTTPError) as error:
            raise CandidateError(f"artifact download failed: {error}") from error


def _verify_pull_request_run(candidate: Candidate, run: dict[str, Any]) -> None:
    pull_requests = run.get("pull_requests")
    if not isinstance(pull_requests, list):
        raise CandidateError("workflow run pull_requests is missing")
    matches = [item for item in pull_requests if isinstance(item, dict) and item.get("number") == candidate.workflow.pull_request]
    if len(matches) != 1:
        raise CandidateError("workflow run does not belong to the selected pull request")
    selected = matches[0]
    head = _mapping(selected.get("head"), "workflow pull request head")
    base = _mapping(selected.get("base"), "workflow pull request base")
    if head.get("sha") != candidate.commit or base.get("ref") != candidate.workflow.base_ref:
        raise CandidateError("workflow pull request head/base provenance mismatch")


def verify_run_provenance(candidate: Candidate, run: dict[str, Any]) -> None:
    if run.get("id") != candidate.workflow.run_id:
        raise CandidateError("workflow run ID mismatch")
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        raise CandidateError("workflow run must be completed successfully")
    if run.get("head_sha") != candidate.commit:
        raise CandidateError("workflow run head SHA mismatch")
    if run.get("run_attempt") != candidate.workflow.run_attempt:
        raise CandidateError("workflow run attempt mismatch")
    if run.get("path") != candidate.workflow.path or run.get("event") != candidate.workflow.event:
        raise CandidateError("workflow path/event mismatch")
    head_repository = _mapping(run.get("head_repository"), "workflow head repository")
    if head_repository.get("full_name") != candidate.repository:
        raise CandidateError("workflow head repository mismatch")
    if candidate.workflow.event == "pull_request":
        _verify_pull_request_run(candidate, run)


def _github_timestamp(value: object, context: str) -> datetime:
    if not isinstance(value, str):
        raise CandidateError(f"{context} timestamp is missing")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise CandidateError(f"{context} timestamp is invalid") from error


def verify_artifact_provenance(candidate: Candidate, artifact: dict[str, Any], run: dict[str, Any]) -> str:
    if artifact.get("id") != candidate.artifact.id or artifact.get("name") != candidate.artifact.name:
        raise CandidateError("artifact identity mismatch")
    if artifact.get("expired") is not False:
        raise CandidateError("artifact is expired")
    workflow_run = _mapping(artifact.get("workflow_run"), "artifact workflow_run")
    if workflow_run.get("id") != candidate.workflow.run_id or workflow_run.get("head_sha") != candidate.commit:
        raise CandidateError("artifact does not belong to the selected workflow run")
    head_repository_id = workflow_run.get("head_repository_id")
    if isinstance(head_repository_id, bool) or not isinstance(head_repository_id, int) or head_repository_id <= 0:
        raise CandidateError("artifact workflow_run lacks an owning head repository ID")
    artifact_created = _github_timestamp(artifact.get("created_at"), "artifact created_at")
    attempt_started = _github_timestamp(run.get("run_started_at"), "workflow attempt run_started_at")
    attempt_finished = _github_timestamp(run.get("updated_at"), "workflow attempt updated_at")
    if not attempt_started <= artifact_created <= attempt_finished:
        raise CandidateError("artifact was not created during the selected workflow attempt")
    digest = artifact.get("digest")
    if not isinstance(digest, str) or _digest(digest, "artifact API digest") != candidate.artifact.archive_sha256:
        raise CandidateError("artifact API digest mismatch")
    download_url = artifact.get("archive_download_url")
    if not isinstance(download_url, str) or not download_url.startswith("https://api.github.com/"):
        raise CandidateError("artifact download URL is invalid")
    return download_url


def retrieve_candidates(manifest_path: Path, output: Path, client: GitHubClient) -> None:
    """Retrieve and verify all candidate artifacts into an offline bundle."""

    manifest = load_manifest(manifest_path, require_live_set=True)
    if output.exists():
        if not output.is_dir() or any(output.iterdir()):
            raise CandidateError(f"output directory must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    wheels = output / "wheels"
    wheels.mkdir()

    with tempfile.TemporaryDirectory(prefix="compas-candidate-download-") as temporary:
        temporary_path = Path(temporary)
        for candidate in manifest.packages:
            run = client.json(f"repos/{candidate.repository}/actions/runs/{candidate.workflow.run_id}/attempts/{candidate.workflow.run_attempt}")
            verify_run_provenance(candidate, run)
            artifact = client.json(f"repos/{candidate.repository}/actions/artifacts/{candidate.artifact.id}")
            download_url = verify_artifact_provenance(candidate, artifact, run)
            archive = temporary_path / f"{candidate.distribution}.zip"
            client.download(download_url, archive)
            if sha256_file(archive) != candidate.artifact.archive_sha256:
                raise CandidateError(f"downloaded archive digest mismatch for {candidate.distribution}")
            wheel = extract_single_wheel(archive, wheels, candidate.wheel.filename)
            verify_wheel(wheel, candidate, manifest)

    shutil.copyfile(manifest_path, output / "manifest.json")
    bundle = {
        "schema_version": 1,
        "wheels": {candidate.wheel.filename: candidate.wheel.sha256 for candidate in sorted(manifest.packages, key=lambda item: item.distribution)},
    }
    (output / "bundle.json").write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    verify_offline_bundle(output, manifest)


def verify_offline_bundle(bundle: Path, manifest: Manifest | None = None) -> Manifest:
    """Revalidate a credential-free candidate bundle before installation."""

    bundled_manifest = load_manifest(bundle / "manifest.json", require_live_set=True)
    if manifest is not None and bundled_manifest != manifest:
        raise CandidateError("bundled manifest differs from the selected manifest")
    actual_root = {path.name for path in bundle.iterdir()}
    if actual_root != {"manifest.json", "bundle.json", "wheels"}:
        raise CandidateError("offline bundle root contains missing or unexpected entries")
    try:
        bundle_data = _mapping(json.loads((bundle / "bundle.json").read_text(encoding="utf-8")), "bundle")
    except (OSError, json.JSONDecodeError) as error:
        raise CandidateError(f"cannot read offline bundle inventory: {error}") from error
    _exact_keys(bundle_data, {"schema_version", "wheels"}, "bundle")
    if bundle_data.get("schema_version") != 1:
        raise CandidateError("bundle schema_version must be 1")
    wheel_digests = _mapping(bundle_data.get("wheels"), "bundle.wheels")
    expected = {candidate.wheel.filename: candidate.wheel.sha256 for candidate in bundled_manifest.packages}
    if wheel_digests != expected:
        raise CandidateError("bundle wheel inventory does not exactly match the manifest")
    wheel_directory = bundle / "wheels"
    if not wheel_directory.is_dir():
        raise CandidateError("offline bundle wheels entry must be a directory")
    actual_files = {path.name for path in wheel_directory.iterdir() if path.is_file()}
    if actual_files != set(expected) or any(not path.is_file() for path in wheel_directory.iterdir()):
        raise CandidateError("offline bundle contains missing or unexpected wheel files")
    for candidate in bundled_manifest.packages:
        verify_wheel(wheel_directory / candidate.wheel.filename, candidate, bundled_manifest)
    return bundled_manifest


def _framework_wheel(framework_bundle: Path) -> Path:
    wheel_directory = framework_bundle / "framework"
    wheels = sorted(wheel_directory.glob("*.whl"))
    if len(wheels) != 1:
        raise CandidateError("framework bundle must contain exactly one wheel")
    checksum_file = wheel_directory / "SHA256SUMS"
    try:
        digest, filename = checksum_file.read_text(encoding="utf-8").strip().split(maxsplit=1)
    except (OSError, ValueError) as error:
        raise CandidateError("framework bundle has an invalid SHA256SUMS file") from error
    filename = filename.lstrip("*").removeprefix("./")
    if filename != wheels[0].name or _digest(digest, "framework wheel digest") != sha256_file(wheels[0]):
        raise CandidateError("framework wheel digest mismatch")
    return wheels[0]


def install_candidates(bundle: Path, framework_bundle: Path, python: Path) -> None:
    """Install the verified candidates and framework wheel without resolution."""

    manifest = verify_offline_bundle(bundle)
    framework_wheel = _framework_wheel(framework_bundle)
    environment = os.environ.copy()
    environment["PIP_NO_INDEX"] = "1"
    environment["PYTHONPATH"] = ""
    for candidate in _topological_candidates(manifest):
        command = [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-deps",
            str(bundle / "wheels" / candidate.wheel.filename),
        ]
        subprocess.run(command, check=True, env=environment)
    subprocess.run(
        [str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(framework_wheel)],
        check=True,
        env=environment,
    )
    expected_versions = {candidate.distribution: str(candidate.version) for candidate in manifest.packages}
    check_versions = (
        "import json; from importlib.metadata import version; "
        "expected=json.loads(" + repr(json.dumps(expected_versions, sort_keys=True)) + "); "
        "actual={name: version(name) for name in expected}; "
        "assert actual == expected, (actual, expected)"
    )
    subprocess.run([str(python), "-I", "-c", check_versions], check=True, env=environment)


def verify_junit(path: Path, required: Iterable[str]) -> None:
    """Fail unless a JUnit report contains only passing required tests."""

    try:
        root = ElementTree.parse(path).getroot()
    except (OSError, ElementTree.ParseError) as error:
        raise CandidateError(f"cannot read JUnit report: {error}") from error
    cases = list(root.iter("testcase"))
    if not cases:
        raise CandidateError("required native suite executed zero tests")
    failures = [case for case in cases if case.find("failure") is not None]
    errors = [case for case in cases if case.find("error") is not None]
    skips = [case for case in cases if case.find("skipped") is not None]
    if failures or errors or skips:
        raise CandidateError(f"JUnit report is not clean: failures={len(failures)}, errors={len(errors)}, skipped={len(skips)}")
    identifiers = {f"{case.get('classname')}::{case.get('name')}" if case.get("classname") else str(case.get("name")) for case in cases}
    names = {str(case.get("name")) for case in cases}
    missing = sorted(item for item in required if item not in identifiers and item not in names)
    if missing:
        raise CandidateError(f"JUnit report is missing required tests: {missing!r}")


def _pypi_payload(candidate: Candidate, base_url: str) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/{candidate.distribution}/{candidate.version}/json"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            value = json.load(response)
    except (OSError, urllib.error.HTTPError, json.JSONDecodeError) as error:
        raise CandidateError(f"public artifact lookup failed for {candidate.distribution}: {error}") from error
    return _mapping(value, f"PyPI response for {candidate.distribution}")


def verify_public_candidate(candidate: Candidate, payload: dict[str, Any]) -> None:
    info = _mapping(payload.get("info"), f"PyPI metadata for {candidate.distribution}")
    if info.get("name") is None or canonicalize_name(str(info["name"])) != candidate.distribution:
        raise CandidateError(f"public distribution name mismatch for {candidate.distribution}")
    try:
        public_version = Version(str(info.get("version", "")))
    except Exception as error:
        raise CandidateError(f"public version is invalid for {candidate.distribution}") from error
    if public_version != candidate.version:
        raise CandidateError(f"public version mismatch for {candidate.distribution}")
    urls = payload.get("urls")
    if not isinstance(urls, list):
        raise CandidateError(f"PyPI response for {candidate.distribution} has no files")
    matches = [item for item in urls if isinstance(item, dict) and item.get("filename") == candidate.wheel.filename]
    if len(matches) != 1:
        raise CandidateError(f"public filename mismatch for {candidate.distribution}")
    selected = matches[0]
    if selected.get("yanked") is not False:
        raise CandidateError(f"public file is yanked for {candidate.distribution}")
    digests = _mapping(selected.get("digests"), f"PyPI digests for {candidate.distribution}")
    if digests.get("sha256") != candidate.wheel.sha256:
        raise CandidateError(f"public file digest mismatch for {candidate.distribution}")


def _transitive_dependencies(manifest: Manifest, distribution: str) -> set[str]:
    by_name = manifest.by_name
    name = canonicalize_name(distribution)
    if name not in by_name:
        raise CandidateError(f"unknown promotion target {distribution!r}")
    result: set[str] = set()

    def collect(current: str) -> None:
        for dependency in by_name[current].depends_on:
            if dependency not in result:
                result.add(dependency)
                collect(dependency)

    collect(name)
    return result


def verify_public_artifacts(manifest: Manifest, *, before: str | None = None, base_url: str = "https://pypi.org/pypi") -> None:
    if before is None:
        selected = set(manifest.by_name)
    else:
        selected = _transitive_dependencies(manifest, before)
    for candidate in _topological_candidates(manifest):
        if candidate.distribution in selected:
            verify_public_candidate(candidate, _pypi_payload(candidate, base_url))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-manifest")
    validate.add_argument("manifest", type=Path)
    validate.add_argument("--live", action="store_true")

    retrieve = subparsers.add_parser("retrieve")
    retrieve.add_argument("manifest", type=Path)
    retrieve.add_argument("output", type=Path)

    verify_bundle = subparsers.add_parser("verify-bundle")
    verify_bundle.add_argument("bundle", type=Path)

    install = subparsers.add_parser("install")
    install.add_argument("bundle", type=Path)
    install.add_argument("framework_bundle", type=Path)
    install.add_argument("--python", required=True, type=Path)

    junit = subparsers.add_parser("verify-junit")
    junit.add_argument("report", type=Path)
    junit.add_argument("--required", action="append", default=[])

    public = subparsers.add_parser("verify-public")
    public.add_argument("manifest", type=Path)
    public.add_argument("--before")
    public.add_argument("--base-url", default="https://pypi.org/pypi")
    return parser


def main() -> None:
    args = _parser().parse_args()
    try:
        if args.command == "validate-manifest":
            load_manifest(args.manifest, require_live_set=args.live)
        elif args.command == "retrieve":
            token = os.environ.get("CANDIDATE_ARTIFACT_TOKEN", "")
            retrieve_candidates(args.manifest, args.output, GitHubClient(token))
        elif args.command == "verify-bundle":
            verify_offline_bundle(args.bundle)
        elif args.command == "install":
            install_candidates(args.bundle, args.framework_bundle, args.python)
        elif args.command == "verify-junit":
            verify_junit(args.report, args.required)
        elif args.command == "verify-public":
            verify_public_artifacts(load_manifest(args.manifest, require_live_set=True), before=args.before, base_url=args.base_url)
        else:
            raise CandidateError(f"unsupported command {args.command!r}")
    except CandidateError as error:
        print(f"candidate verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
