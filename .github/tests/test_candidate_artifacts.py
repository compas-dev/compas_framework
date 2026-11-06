import copy
import hashlib
import importlib.util
import json
import stat
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[2]
SCRIPT = ROOT / ".github" / "scripts" / "candidate_artifacts.py"
SPEC = importlib.util.spec_from_file_location("candidate_artifacts", SCRIPT)
assert SPEC and SPEC.loader
candidate_artifacts = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = candidate_artifacts
SPEC.loader.exec_module(candidate_artifacts)

CandidateError = candidate_artifacts.CandidateError


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def package(
    name: str,
    repository: str,
    *,
    artifact_id: int,
    depends_on: list[str] | None = None,
    platform: str = "any",
) -> dict[str, object]:
    normalized = name.replace("_", "-")
    wheel_name = f"{name.replace('-', '_')}-3.0.0-py3-none-{platform}.whl"
    return {
        "distribution": normalized,
        "version": "3.0.0",
        "repository": repository,
        "commit": digest(f"commit-{name}".encode())[:40],
        "workflow": {
            "run_id": artifact_id + 1000,
            "run_attempt": 1,
            "path": ".github/workflows/build.yml",
            "event": "pull_request",
            "pull_request": artifact_id + 10,
            "base_ref": "c3-upgrade",
        },
        "artifact": {
            "id": artifact_id,
            "name": "candidate-linux-py312" if name in {"compas", "compas_occ"} else "wheels-manylinux",
            "archive_sha256": digest(f"archive-{name}".encode()),
        },
        "wheel": {"filename": wheel_name, "sha256": digest(f"wheel-{name}".encode())},
        "depends_on": depends_on or [],
    }


def manifest_data(*packages: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "target": {
            "runner": "ubuntu-24.04",
            "os": "linux",
            "architecture": "x86_64",
            "python": "3.12",
        },
        "packages": list(packages),
    }


def live_manifest_data() -> dict[str, object]:
    return manifest_data(
        package("compas", "compas-dev/compas", artifact_id=1),
        package("compas_occ", "compas-dev/compas_occ", artifact_id=2, depends_on=["compas"]),
        package("compas_cgal", "compas-dev/compas_cgal", artifact_id=3, depends_on=["compas"], platform="manylinux_2_28_x86_64"),
        package("compas_libigl", "compas-dev/compas_libigl", artifact_id=4, depends_on=["compas"], platform="manylinux_2_28_x86_64"),
    )


def write_wheel(
    directory: Path,
    entry: dict[str, object],
    *,
    requires: list[str] | None = None,
    tags: list[str] | None = None,
    native: bool | None = None,
) -> Path:
    wheel_data = entry["wheel"]
    assert isinstance(wheel_data, dict)
    filename = str(wheel_data["filename"])
    distribution = str(entry["distribution"])
    version = str(entry["version"])
    wheel = directory / filename
    platform = filename.removesuffix(".whl").rsplit("-", 1)[-1]
    tags = tags or [f"py3-none-{part}" for part in platform.split(".")]
    if native is None:
        native = platform != "any"
    metadata = [
        "Metadata-Version: 2.4",
        f"Name: {distribution}",
        f"Version: {version}",
        "Requires-Python: >=3.12",
    ]
    metadata.extend(f"Requires-Dist: {requirement}" for requirement in (requires or []))
    dist_info = f"{distribution.replace('-', '_')}-{version}.dist-info"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(f"{distribution.replace('-', '_')}/__init__.py", "")
        if native:
            archive.writestr(f"{distribution.replace('-', '_')}/_native.so", "")
        archive.writestr(f"{dist_info}/METADATA", "\n".join(metadata) + "\n")
        archive.writestr(
            f"{dist_info}/WHEEL",
            "Wheel-Version: 1.0\nRoot-Is-Purelib: {}\n{}".format(
                "false" if native else "true",
                "".join(f"Tag: {tag}\n" for tag in tags),
            ),
        )
        archive.writestr(f"{dist_info}/RECORD", "")
    wheel_data["sha256"] = candidate_artifacts.sha256_file(wheel)
    return wheel


def rewrite_wheel(wheel: Path, transform) -> None:
    rewritten = wheel.with_suffix(".rewritten")
    with zipfile.ZipFile(wheel) as source, zipfile.ZipFile(rewritten, "w") as target:
        for member in source.infolist():
            name, content = transform(member.filename, source.read(member))
            target.writestr(name, content)
    rewritten.replace(wheel)


def write_manifest(path: Path, data: dict[str, object]) -> candidate_artifacts.Manifest:
    path.write_text(json.dumps(data), encoding="utf-8")
    return candidate_artifacts.load_manifest(path)


def write_bundle(tmp_path: Path) -> tuple[Path, candidate_artifacts.Manifest]:
    data = live_manifest_data()
    bundle = tmp_path / "bundle"
    wheels = bundle / "wheels"
    wheels.mkdir(parents=True)
    packages = data["packages"]
    assert isinstance(packages, list)
    for entry in packages:
        assert isinstance(entry, dict)
        dependencies = entry["depends_on"]
        assert isinstance(dependencies, list)
        requirements = [f"{name}>=3,<4" for name in dependencies]
        write_wheel(wheels, entry, requires=requirements)
    manifest = write_manifest(bundle / "manifest.json", data)
    bundle_data = {"schema_version": 1, "wheels": {item.wheel.filename: item.wheel.sha256 for item in manifest.packages}}
    (bundle / "bundle.json").write_text(json.dumps(bundle_data), encoding="utf-8")
    return bundle, manifest


def test_manifest_accepts_exact_candidate_set_and_derives_dependency_order():
    manifest = candidate_artifacts.parse_manifest(live_manifest_data(), require_live_set=True)

    order = [item.distribution for item in candidate_artifacts._topological_candidates(manifest)]

    assert order.index("compas") < order.index("compas-occ")
    assert order.index("compas") < order.index("compas-cgal")
    assert order.index("compas") < order.index("compas-libigl")


def test_manifest_fixture_conforms_to_the_documented_json_schema():
    schema = json.loads((ROOT / ".github" / "candidates" / "schema-v1.json").read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(live_manifest_data())


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda data: data["packages"].append(copy.deepcopy(data["packages"][0])), "duplicate package"),
        (lambda data: data["packages"][1].update(depends_on=["missing"]), "unknown dependencies"),
        (lambda data: data["packages"][0].update(depends_on=["compas-occ"]), "cycle"),
        (lambda data: data["packages"][0].update(commit="a" * 39), "full lowercase commit"),
        (lambda data: data["packages"][0]["artifact"].update(archive_sha256="placeholder"), "placeholder"),
        (lambda data: data["target"].update(python="3.13"), "initial supported target"),
    ],
)
def test_manifest_rejects_invalid_contracts(mutate, message):
    data = live_manifest_data()
    mutate(data)

    with pytest.raises(CandidateError, match=message):
        candidate_artifacts.parse_manifest(data)


def test_manifest_rejects_missing_candidate_from_live_set():
    data = live_manifest_data()
    packages = data["packages"]
    assert isinstance(packages, list)
    packages.pop()

    with pytest.raises(CandidateError, match="exactly"):
        candidate_artifacts.parse_manifest(data, require_live_set=True)


def test_live_manifest_rejects_unapproved_repository_or_artifact_name():
    data = live_manifest_data()
    packages = data["packages"]
    assert isinstance(packages, list)
    first = packages[0]
    assert isinstance(first, dict)
    first["repository"] = "other/compas"
    with pytest.raises(CandidateError, match="repository"):
        candidate_artifacts.parse_manifest(data, require_live_set=True)

    data = live_manifest_data()
    packages = data["packages"]
    assert isinstance(packages, list)
    first = packages[0]
    assert isinstance(first, dict)
    artifact = first["artifact"]
    assert isinstance(artifact, dict)
    artifact["name"] = "other"
    with pytest.raises(CandidateError, match="artifact name"):
        candidate_artifacts.parse_manifest(data, require_live_set=True)


def test_wheel_verification_accepts_compressed_platform_tags_and_dependencies(tmp_path: Path):
    data = manifest_data(
        package("compas", "compas-dev/compas", artifact_id=1),
        package(
            "compas_cgal",
            "compas-dev/compas_cgal",
            artifact_id=2,
            depends_on=["compas"],
            platform="manylinux_2_27_x86_64.manylinux_2_28_x86_64",
        ),
    )
    packages = data["packages"]
    assert isinstance(packages, list)
    entry = packages[1]
    assert isinstance(entry, dict)
    wheel = write_wheel(tmp_path, entry, requires=["compas>=3,<4"])
    manifest = candidate_artifacts.parse_manifest(data)

    candidate_artifacts.verify_wheel(wheel, manifest.by_name["compas-cgal"], manifest)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda wheel, entry: entry["wheel"].update(sha256="a" * 64), "digest mismatch"),
        (lambda wheel, entry: entry.update(version="3.0.1"), "filename does not match"),
    ],
)
def test_wheel_verification_rejects_digest_and_identity_mismatches(tmp_path: Path, change, message):
    data = manifest_data(package("compas", "compas-dev/compas", artifact_id=1))
    packages = data["packages"]
    assert isinstance(packages, list)
    entry = packages[0]
    assert isinstance(entry, dict)
    wheel = write_wheel(tmp_path, entry)
    change(wheel, entry)

    with pytest.raises(CandidateError, match=message):
        manifest = candidate_artifacts.parse_manifest(data)
        candidate_artifacts.verify_wheel(wheel, manifest.packages[0], manifest)


def test_wheel_verification_rejects_missing_dependency_metadata(tmp_path: Path):
    data = manifest_data(
        package("compas", "compas-dev/compas", artifact_id=1),
        package("compas_occ", "compas-dev/compas_occ", artifact_id=2, depends_on=["compas"]),
    )
    packages = data["packages"]
    assert isinstance(packages, list)
    entry = packages[1]
    assert isinstance(entry, dict)
    wheel = write_wheel(tmp_path, entry)
    manifest = candidate_artifacts.parse_manifest(data)

    with pytest.raises(CandidateError, match="do not match depends_on"):
        candidate_artifacts.verify_wheel(wheel, manifest.by_name["compas-occ"], manifest)


@pytest.mark.parametrize(
    ("suffix", "replacement", "message"),
    [
        (".dist-info/METADATA", (b"Name: compas\n", b"Name: other\n"), "METADATA name"),
        (".dist-info/WHEEL", (b"Tag: py3-none-any\n", b"Tag: py2-none-any\n"), "tags do not exactly match"),
    ],
)
def test_wheel_verification_rejects_wrong_metadata_and_tags(tmp_path: Path, suffix: str, replacement, message: str):
    data = manifest_data(package("compas", "compas-dev/compas", artifact_id=1))
    packages = data["packages"]
    assert isinstance(packages, list)
    entry = packages[0]
    assert isinstance(entry, dict)
    wheel = write_wheel(tmp_path, entry)

    def transform(name, content):
        if name.endswith(suffix):
            content = content.replace(*replacement)
        return name, content

    rewrite_wheel(wheel, transform)
    wheel_data = entry["wheel"]
    assert isinstance(wheel_data, dict)
    wheel_data["sha256"] = candidate_artifacts.sha256_file(wheel)
    manifest = candidate_artifacts.parse_manifest(data)

    with pytest.raises(CandidateError, match=message):
        candidate_artifacts.verify_wheel(wheel, manifest.packages[0], manifest)


@pytest.mark.parametrize("platform", ["musllinux_1_2_x86_64", "manylinux_2_40_x86_64"])
def test_wheel_verification_rejects_incompatible_linux_policies(tmp_path: Path, platform: str):
    data = manifest_data(
        package("compas", "compas-dev/compas", artifact_id=1),
        package("compas_cgal", "compas-dev/compas_cgal", artifact_id=2, depends_on=["compas"], platform=platform),
    )
    packages = data["packages"]
    assert isinstance(packages, list)
    entry = packages[1]
    assert isinstance(entry, dict)
    wheel = write_wheel(tmp_path, entry, requires=["compas>=3,<4"])
    manifest = candidate_artifacts.parse_manifest(data)

    with pytest.raises(CandidateError, match="incompatible"):
        candidate_artifacts.verify_wheel(wheel, manifest.by_name["compas-cgal"], manifest)


def test_artifact_redirect_does_not_forward_authorization_cross_host():
    handler = candidate_artifacts._CrossHostAuthorizationRedirect()
    request = urllib.request.Request(
        "https://api.github.com/repos/compas-dev/compas/actions/artifacts/1/zip",
        headers={"Authorization": "Bearer secret"},
    )

    redirected = handler.redirect_request(request, None, 302, "Found", {}, "https://objects.example/artifact.zip")

    assert redirected is not None
    assert not redirected.has_header("Authorization")

    with pytest.raises(urllib.error.HTTPError, match="must use HTTPS"):
        handler.redirect_request(request, None, 302, "Found", {}, "http://api.github.com/artifact.zip")


def run_payload(entry: dict[str, object]) -> dict[str, object]:
    workflow = entry["workflow"]
    assert isinstance(workflow, dict)
    return {
        "id": workflow["run_id"],
        "status": "completed",
        "conclusion": "success",
        "head_sha": entry["commit"],
        "run_attempt": workflow["run_attempt"],
        "path": workflow["path"],
        "event": workflow["event"],
        "run_started_at": "2026-11-06T10:00:00Z",
        "updated_at": "2026-11-06T10:30:00Z",
        "head_repository": {"full_name": entry["repository"]},
        "pull_requests": [
            {
                "number": workflow["pull_request"],
                "head": {"sha": entry["commit"], "repo": {"name": str(entry["repository"]).split("/")[-1]}},
                "base": {"ref": workflow["base_ref"]},
            }
        ],
    }


def artifact_payload(entry: dict[str, object]) -> dict[str, object]:
    workflow = entry["workflow"]
    artifact = entry["artifact"]
    assert isinstance(workflow, dict)
    assert isinstance(artifact, dict)
    return {
        "id": artifact["id"],
        "name": artifact["name"],
        "expired": False,
        "digest": f"sha256:{artifact['archive_sha256']}",
        "archive_download_url": f"https://api.github.com/artifacts/{artifact['id']}/zip",
        "created_at": "2026-11-06T10:15:00Z",
        "workflow_run": {"id": workflow["run_id"], "head_sha": entry["commit"], "head_repository_id": 123},
    }


def test_provenance_accepts_exact_run_and_artifact():
    data = live_manifest_data()
    entry = data["packages"][0]
    assert isinstance(entry, dict)
    candidate = candidate_artifacts.parse_manifest(data).packages[0]

    run = run_payload(entry)
    candidate_artifacts.verify_run_provenance(candidate, run)
    url = candidate_artifacts.verify_artifact_provenance(candidate, artifact_payload(entry), run)

    assert url.startswith("https://api.github.com/")


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda payload: payload.update(conclusion="failure"), "completed successfully"),
        (lambda payload: payload.update(head_sha="a" * 40), "head SHA mismatch"),
        (lambda payload: payload["head_repository"].update(full_name="fork/compas"), "head repository mismatch"),
        (lambda payload: payload["pull_requests"][0]["base"].update(ref="main"), "head/base"),
    ],
)
def test_provenance_rejects_untrusted_runs(mutate, message):
    data = live_manifest_data()
    entry = data["packages"][0]
    assert isinstance(entry, dict)
    candidate = candidate_artifacts.parse_manifest(data).packages[0]
    payload = run_payload(entry)
    mutate(payload)

    with pytest.raises(CandidateError, match=message):
        candidate_artifacts.verify_run_provenance(candidate, payload)


def test_artifact_provenance_rejects_expired_changed_digest_and_wrong_attempt():
    data = live_manifest_data()
    entry = data["packages"][0]
    assert isinstance(entry, dict)
    candidate = candidate_artifacts.parse_manifest(data).packages[0]
    expired = artifact_payload(entry)
    expired["expired"] = True
    changed = artifact_payload(entry)
    changed["digest"] = "sha256:" + "b" * 64
    wrong_attempt = artifact_payload(entry)
    wrong_attempt["created_at"] = "2026-11-06T09:59:59Z"
    run = run_payload(entry)

    with pytest.raises(CandidateError, match="expired"):
        candidate_artifacts.verify_artifact_provenance(candidate, expired, run)
    with pytest.raises(CandidateError, match="digest mismatch"):
        candidate_artifacts.verify_artifact_provenance(candidate, changed, run)
    with pytest.raises(CandidateError, match="selected workflow attempt"):
        candidate_artifacts.verify_artifact_provenance(candidate, wrong_attempt, run)


def test_retrieval_verifies_provenance_and_downloaded_archive_digest(tmp_path: Path):
    data = live_manifest_data()
    source = tmp_path / "source"
    source.mkdir()
    archives: dict[str, Path] = {}
    packages = data["packages"]
    assert isinstance(packages, list)
    for entry in packages:
        assert isinstance(entry, dict)
        dependencies = entry["depends_on"]
        assert isinstance(dependencies, list)
        wheel = write_wheel(source, entry, requires=[f"{name}>=3,<4" for name in dependencies])
        artifact = entry["artifact"]
        assert isinstance(artifact, dict)
        archive = source / f"{artifact['id']}.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.write(wheel, wheel.name)
        artifact["archive_sha256"] = candidate_artifacts.sha256_file(archive)
        archives[f"https://api.github.com/artifacts/{artifact['id']}/zip"] = archive
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    class Client:
        def json(self, path: str) -> dict[str, object]:
            repository = path.removeprefix("repos/").split("/actions/", 1)[0].split("/pulls/", 1)[0]
            entry = next(item for item in packages if isinstance(item, dict) and item["repository"] == repository)
            if "/actions/runs/" in path:
                return run_payload(entry)
            return artifact_payload(entry)

        def download(self, url: str, destination: Path) -> None:
            destination.write_bytes(archives[url].read_bytes())

    client = Client()
    output = tmp_path / "verified"
    candidate_artifacts.retrieve_candidates(manifest_path, output, client)

    assert candidate_artifacts.verify_offline_bundle(output).by_name.keys() == candidate_artifacts.LIVE_DISTRIBUTIONS

    corrupt = tmp_path / "corrupt.zip"
    corrupt.write_bytes(b"changed archive")
    archives[next(iter(archives))] = corrupt
    with pytest.raises(CandidateError, match="downloaded archive digest mismatch"):
        candidate_artifacts.retrieve_candidates(manifest_path, tmp_path / "rejected", client)


def test_safe_extraction_rejects_traversal_symlinks_and_extra_files(tmp_path: Path):
    destination = tmp_path / "output"
    for index, writer in enumerate(
        (
            lambda archive: archive.writestr("../candidate.whl", ""),
            lambda archive: _write_symlink(archive, "candidate.whl"),
            lambda archive: (archive.writestr("candidate.whl", ""), archive.writestr("extra.txt", "")),
        )
    ):
        archive_path = tmp_path / f"artifact-{index}.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            writer(archive)
        with pytest.raises(CandidateError):
            candidate_artifacts.extract_single_wheel(archive_path, destination / str(index), "candidate.whl")


def _write_symlink(archive: zipfile.ZipFile, name: str) -> None:
    info = zipfile.ZipInfo(name)
    info.create_system = 3
    info.external_attr = (stat.S_IFLNK | 0o777) << 16
    archive.writestr(info, "target")


def test_offline_bundle_revalidates_exact_inventory_and_hashes(tmp_path: Path):
    bundle, manifest = write_bundle(tmp_path / "hash")

    assert candidate_artifacts.verify_offline_bundle(bundle) == manifest

    selected = bundle / "wheels" / manifest.packages[0].wheel.filename
    selected.write_bytes(selected.read_bytes() + b"tampered")
    with pytest.raises(CandidateError, match="digest mismatch"):
        candidate_artifacts.verify_offline_bundle(bundle)

    missing_bundle, missing_manifest = write_bundle(tmp_path / "missing")
    (missing_bundle / "wheels" / missing_manifest.packages[0].wheel.filename).unlink()
    with pytest.raises(CandidateError, match="missing or unexpected"):
        candidate_artifacts.verify_offline_bundle(missing_bundle)

    extra_bundle, _ = write_bundle(tmp_path / "extra")
    (extra_bundle / "wheels" / "unexpected.whl").write_bytes(b"unexpected")
    with pytest.raises(CandidateError, match="missing or unexpected"):
        candidate_artifacts.verify_offline_bundle(extra_bundle)


def junit(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "junit.xml"
    path.write_text(f'<testsuite name="native">{body}</testsuite>', encoding="utf-8")
    return path


def test_junit_accepts_required_passing_cases(tmp_path: Path):
    report = junit(tmp_path, '<testcase classname="candidate" name="test_cgal_to_core"/>')

    candidate_artifacts.verify_junit(report, ["candidate::test_cgal_to_core"])


@pytest.mark.parametrize(
    ("body", "message"),
    [
        pytest.param("", "zero tests", id="zero"),
        pytest.param('<testcase name="failure"><failure/></testcase>', "failures=1", id="failure"),
        pytest.param('<testcase name="error"><error/></testcase>', "errors=1", id="error"),
        pytest.param('<testcase name="skip"><skipped/></testcase>', "skipped=1", id="skip"),
        pytest.param('<testcase name="other"/>', "missing required", id="missing"),
    ],
)
def test_junit_rejects_nonpassing_or_missing_evidence(tmp_path: Path, body: str, message: str):
    with pytest.raises(CandidateError, match=message):
        candidate_artifacts.verify_junit(junit(tmp_path, body), ["required"])


def test_public_artifact_requires_exact_filename_digest_and_non_yanked():
    candidate = candidate_artifacts.parse_manifest(live_manifest_data()).packages[0]
    payload = {
        "info": {"name": candidate.distribution, "version": str(candidate.version)},
        "urls": [
            {
                "filename": candidate.wheel.filename,
                "yanked": False,
                "digests": {"sha256": candidate.wheel.sha256},
            }
        ],
    }

    candidate_artifacts.verify_public_candidate(candidate, payload)

    for changed, message in (
        ({**payload, "urls": []}, "filename mismatch"),
        ({**payload, "info": {**payload["info"], "version": "9.0.0"}}, "version mismatch"),
        ({**payload, "urls": [{**payload["urls"][0], "yanked": True}]}, "yanked"),
        ({**payload, "urls": [{**payload["urls"][0], "digests": {"sha256": "b" * 64}}]}, "digest mismatch"),
    ):
        with pytest.raises(CandidateError, match=message):
            candidate_artifacts.verify_public_candidate(candidate, changed)


def test_release_order_checks_only_transitive_upstreams_and_blocks_missing_publication(monkeypatch):
    manifest = candidate_artifacts.parse_manifest(live_manifest_data(), require_live_set=True)
    requested: list[str] = []

    def payload(candidate, base_url):
        requested.append(candidate.distribution)
        return {
            "info": {"name": candidate.distribution, "version": str(candidate.version)},
            "urls": [
                {
                    "filename": candidate.wheel.filename,
                    "yanked": False,
                    "digests": {"sha256": candidate.wheel.sha256},
                }
            ],
        }

    monkeypatch.setattr(candidate_artifacts, "_pypi_payload", payload)

    candidate_artifacts.verify_public_artifacts(manifest, before="compas-occ")
    assert requested == ["compas"]

    def missing(candidate, base_url):
        raise CandidateError(f"public artifact lookup failed for {candidate.distribution}")

    monkeypatch.setattr(candidate_artifacts, "_pypi_payload", missing)
    for dependent in ("compas-occ", "compas-cgal", "compas-libigl"):
        with pytest.raises(CandidateError, match="public artifact lookup failed for compas"):
            candidate_artifacts.verify_public_artifacts(manifest, before=dependent)


@pytest.mark.parametrize(
    ("field", "message"),
    [("version", "version mismatch"), ("filename", "filename mismatch"), ("digest", "digest mismatch")],
)
def test_release_order_blocks_changed_public_files_for_every_dependent(monkeypatch, field: str, message: str):
    manifest = candidate_artifacts.parse_manifest(live_manifest_data(), require_live_set=True)

    def changed(candidate, base_url):
        version = "9.0.0" if field == "version" else str(candidate.version)
        filename = "rebuilt.whl" if field == "filename" else candidate.wheel.filename
        wheel_digest = "b" * 64 if field == "digest" else candidate.wheel.sha256
        return {
            "info": {"name": candidate.distribution, "version": version},
            "urls": [{"filename": filename, "yanked": False, "digests": {"sha256": wheel_digest}}],
        }

    monkeypatch.setattr(candidate_artifacts, "_pypi_payload", changed)

    for dependent in ("compas-occ", "compas-cgal", "compas-libigl"):
        with pytest.raises(CandidateError, match=message):
            candidate_artifacts.verify_public_artifacts(manifest, before=dependent)


def test_install_uses_topological_no_index_no_deps_commands(tmp_path: Path, monkeypatch):
    bundle, manifest = write_bundle(tmp_path)
    framework = tmp_path / "framework-bundle" / "framework"
    framework.mkdir(parents=True)
    framework_wheel = framework / "compas_framework-0.1.3-py3-none-any.whl"
    framework_wheel.write_bytes(b"framework")
    (framework / "SHA256SUMS").write_text(f"{candidate_artifacts.sha256_file(framework_wheel)}  {framework_wheel.name}\n")
    calls: list[tuple[list[str], dict[str, str]]] = []

    def run(command, *, check, env):
        assert check is True
        calls.append((command, env))
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(candidate_artifacts.subprocess, "run", run)

    candidate_artifacts.install_candidates(bundle, framework.parent, Path("/candidate/python"))

    assert len(calls) == len(manifest.packages) + 2
    install_calls = calls[:-1]
    assert all(call[0][3:6] == ["install", "--no-index", "--no-deps"] for call in install_calls)
    assert all(call[1]["PIP_NO_INDEX"] == "1" and call[1]["PYTHONPATH"] == "" for call in calls)
    assert Path(calls[0][0][-1]).name == manifest.by_name["compas"].wheel.filename
    assert Path(install_calls[-1][0][-1]).name == framework_wheel.name
    assert calls[-1][0][1:3] == ["-I", "-c"]


def test_live_manifest_is_intentionally_absent_until_producers_exist():
    assert not (ROOT / ".github" / "candidates" / "native-linux-py312.json").exists()
    readme = (ROOT / ".github" / "candidates" / "README.md").read_text(encoding="utf-8")
    assert "must not be fabricated" in readme


def test_trusted_workflow_isolated_from_pull_requests_and_secrets():
    workflow = (ROOT / ".github" / "workflows" / "native-candidate-integration.yml").read_text(encoding="utf-8")

    assert "pull_request:" not in workflow
    assert "pull_request_target:" not in workflow
    assert workflow.count("github.repository == 'compas-dev/compas_framework' && github.ref_protected") == 2
    assert "environment: candidate-artifact-retrieval" in workflow
    assert "persist-credentials: false" in workflow
    assert "permissions: {}" in workflow
    execute = workflow.split("  execute:", 1)[1]
    assert "secrets." not in execute
    assert "actions/checkout" not in execute


def test_pull_request_contract_workflow_has_no_credentials():
    workflow = (ROOT / ".github" / "workflows" / "candidate-contracts.yml").read_text(encoding="utf-8")

    assert "pull_request:" in workflow
    assert "secrets." not in workflow
    assert "create-github-app-token" not in workflow
    assert "permissions:\n  contents: read" in workflow


def test_candidate_workflows_pin_external_actions_and_release_cannot_publish():
    workflow_directory = ROOT / ".github" / "workflows"
    for filename in (
        "candidate-contracts.yml",
        "native-candidate-integration.yml",
        "verify-public-candidates.yml",
    ):
        workflow = (workflow_directory / filename).read_text(encoding="utf-8")
        uses = [line.split("uses:", 1)[1].strip().split(" #", 1)[0] for line in workflow.splitlines() if "uses:" in line]
        assert uses
        assert all("@" in value and len(value.rsplit("@", 1)[1]) == 40 for value in uses)

    release = (workflow_directory / "release.yml").read_text(encoding="utf-8")
    assert "pypa/gh-action-pypi-publish" not in release
    assert "gh release create" not in release
