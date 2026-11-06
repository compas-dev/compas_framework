from pathlib import Path
from runpy import run_path


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


def test_framework_examples_page_is_link_oriented():
    page = (Path(__file__).parents[1] / "docs" / "examples.md").read_text()

    assert "outside the ordinary Ruff, Pyright, and runtime gates" in page
    assert "```python" not in page


def test_pending_candidate_fixtures_are_outside_ordinary_static_gates():
    configuration = (Path(__file__).parents[1] / "pyproject.toml").read_text()

    assert '"tests/test_geometry_tessellation_integration.py"' in configuration
    assert '"tests/test_native_geometry_backends.py"' in configuration
