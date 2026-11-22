import json
import tomllib
from pathlib import Path
from runpy import run_path


def test_version_is_available():
    namespace = run_path(str(Path(__file__).parents[1] / "src" / "compas_framework" / "__init__.py"))

    assert namespace["__version__"]


def test_install_matrix_covers_declared_python_versions():
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    matrix = json.loads((root / "framework-matrix.json").read_text(encoding="utf-8"))
    classifier_prefix = "Programming Language :: Python :: 3."
    declared = {classifier.removeprefix("Programming Language :: Python :: ") for classifier in project["classifiers"] if classifier.startswith(classifier_prefix)}
    assert set(matrix["python"]) == declared
