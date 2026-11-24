import json
import re
import tomllib
from pathlib import Path
from runpy import run_path
from urllib.parse import urlsplit

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


ROOT = Path(__file__).resolve().parents[1]


def test_version_is_available():
    namespace = run_path(str(Path(__file__).parents[1] / "src" / "compas_framework" / "__init__.py"))

    assert namespace["__version__"]


def test_local_build_uses_current_working_tree(tmp_path):
    source = Path(__file__).parents[1]
    namespace = run_path(str(source / "tasks.py"))
    command = namespace["_build_command"](source, tmp_path / "dist")

    assert f'uv build "{source}"' in command
    assert "git archive" not in command


def test_release_workflow_cannot_publish():
    workflow = (Path(__file__).parents[1] / ".github" / "workflows" / "release.yml").read_text()

    forbidden = (
        "contents: write",
        "id-token: write",
        "gh-action-pypi-publish",
        "github-release",
        'deploy: "true"',
    )
    assert all(value not in workflow for value in forbidden)


def test_candidate_contracts_validate_every_workflow():
    workflow = (Path(__file__).parents[1] / ".github" / "workflows" / "candidate-contracts.yml").read_text()

    assert "github.com/rhysd/actionlint/cmd/actionlint@914e7df21a07ef503a81201c76d2b11c789d3fca" in workflow
    assert "-color .github/workflows/*.yml" in workflow


def test_candidate_integration_push_runs_build_and_docs_but_not_release():
    workflows = Path(__file__).parents[1] / ".github" / "workflows"
    build = (workflows / "build.yml").read_text()
    docs = (workflows / "docs.yml").read_text()
    release = (workflows / "release.yml").read_text()

    trigger = "branches: [main, initiative/candidate-artifact-integration]"
    assert trigger in build
    assert trigger in docs
    assert trigger not in release
    assert "branches: [main]" in release


def test_native_candidate_integration_runs_from_the_protected_initiative_branch():
    workflow = (Path(__file__).parents[1] / ".github" / "workflows" / "native-candidate-integration.yml").read_text()

    assert "push:\n    branches:\n      - initiative/candidate-artifact-integration" in workflow
    assert "inputs.manifest_path || '.github/candidates/native-linux-py312.json'" in workflow


@pytest.mark.parametrize(
    ("filename", "distribution", "repository"),
    [
        ("core-requirements.txt", "compas", "compas-dev/compas"),
        ("viewer-requirements.txt", "compas_viewer", "compas-dev/compas_viewer"),
        ("model-requirements.txt", "compas_model", "BlockResearchGroup/compas_model"),
    ],
)
def test_scene_candidate_pins_exact_source_revision(filename, distribution, repository):
    requirement = Requirement((ROOT / ".github" / "scene-candidates" / filename).read_text().strip())
    assert requirement.name == distribution
    assert requirement.url is not None
    url = urlsplit(requirement.url)
    assert url.scheme == "git+https"
    assert url.netloc == "github.com"
    repository_path, _, revision = url.path.rpartition("@")
    assert repository_path == f"/{repository}.git"
    assert re.fullmatch(r"[0-9a-f]{40}", revision)
    assert requirement.marker is None
    assert not requirement.extras
    assert not url.query and not url.fragment
    workflow = (ROOT / ".github" / "workflows" / "scene-candidate-integration.yml").read_text()
    assert filename in workflow
    assert "--no-deps" in workflow
    assert "source-installed-candidates" in workflow


def test_framework_matrix_matches_package_metadata_and_candidate_coverage():
    matrix = json.loads((ROOT / "framework-matrix.json").read_text())
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    dependencies = {canonicalize_name(Requirement(value).name) for value in project["dependencies"]}
    assert set(matrix["packages"]) == dependencies
    assert matrix["python"] == [
        classifier.removeprefix("Programming Language :: Python :: ") for classifier in project["classifiers"] if classifier.startswith("Programming Language :: Python :: 3.")
    ]

    native_manifest = json.loads((ROOT / ".github" / "candidates" / "native-linux-py312.json").read_text())
    native_packages = {package["distribution"] for package in native_manifest["packages"]}
    scene_packages = {canonicalize_name(Requirement(path.read_text().strip()).name) for path in (ROOT / ".github" / "scene-candidates").glob("*-requirements.txt")}
    coverage = {name: set(gates) for name, gates in matrix["packages"].items()}
    assert coverage == {name: {gate for gate, packages in [("native-artifact", native_packages), ("scene-source", scene_packages)] if name in packages} for name in dependencies}
    assert native_packages | scene_packages <= dependencies


def test_framework_examples_page_is_link_oriented():
    page = (Path(__file__).parents[1] / "docs" / "examples.md").read_text()

    assert "outside the ordinary Ruff, Pyright, and runtime gates" in page
    assert "```python" not in page


def test_pending_candidate_fixtures_are_outside_ordinary_static_gates():
    configuration = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]

    assert "tests/integration" in configuration["ruff"]["extend-exclude"]
    assert configuration["pytest"]["ini_options"]["testpaths"] == ["tests/test_package.py"]
    assert not (ROOT / "tests" / "conftest.py").exists()
