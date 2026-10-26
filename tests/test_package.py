from pathlib import Path
from runpy import run_path


def test_version_is_available():
    namespace = run_path(Path(__file__).parents[1] / "src" / "compas_framework" / "__init__.py")

    assert namespace["__version__"]
