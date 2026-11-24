import sys
from pathlib import Path

import pytest


CODE_ROOT = Path(__file__).resolve().parents[3]
SIBLING_REPOSITORIES = ("compas", "compas_occ", "compas_cgal", "compas_libigl")


def pytest_configure(config):
    sources = {name: CODE_ROOT / name / "src" for name in SIBLING_REPOSITORIES}
    missing = [str(source) for source in sources.values() if not source.is_dir()]
    if missing:
        raise pytest.UsageError("Integration tests require sibling checkouts: " + ", ".join(missing))

    for name, source in sources.items():
        module = sys.modules.get(name)
        if module is not None:
            module_file = getattr(module, "__file__", None)
            if not module_file or not Path(module_file).resolve().is_relative_to(source.resolve()):
                raise pytest.UsageError(f"{name} was already imported from {module_file!r}. Start with a fresh Python process.")

    sys.path[:0] = [str(source) for source in sources.values()]
