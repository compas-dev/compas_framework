import sys
from importlib import import_module
from pathlib import Path

import pytest


FRAMEWORK_ROOT = Path(__file__).parents[1]
CODE_ROOT = FRAMEWORK_ROOT.parent
SIBLING_REPOSITORIES = (
    "compas",
    "compas_occ",
    "compas_cgal",
    "compas_libigl",
)


# Integration tests exercise the checked-out sibling sources without installing
# or modifying their environments. Insert in reverse so core COMPAS has highest
# precedence when multiple distributions are already installed.
for repository in reversed(SIBLING_REPOSITORIES):
    source = CODE_ROOT / repository / "src"
    if source.is_dir():
        sys.path.insert(0, str(source))


def _module_is_below(module, root):
    filepath = getattr(module, "__file__", None)
    return filepath is not None and Path(filepath).resolve().is_relative_to(root.resolve())


# Pytest plugins and interactive runners can populate sys.modules before this
# conftest is collected. Remove only mismatched sibling packages so collection
# cannot silently exercise an installed copy instead of the checkout.
for repository in SIBLING_REPOSITORIES:
    source = CODE_ROOT / repository / "src"
    module = sys.modules.get(repository)
    if source.is_dir() and module is not None and not _module_is_below(module, source):
        for name in [name for name in sys.modules if name == repository or name.startswith(repository + ".")]:
            del sys.modules[name]


@pytest.fixture(scope="session", autouse=True)
def assert_sibling_source_provenance():
    resolved = {}
    for repository in SIBLING_REPOSITORIES:
        source = CODE_ROOT / repository / "src"
        if not source.is_dir():
            continue
        module = import_module(repository)
        assert _module_is_below(module, source), f"{repository} resolved from {getattr(module, '__file__', None)!r}; expected checkout below {source}"
        resolved[repository] = module
    return resolved
