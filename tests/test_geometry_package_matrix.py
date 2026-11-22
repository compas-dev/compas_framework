from pathlib import Path
import tomllib

import pytest
from packaging.requirements import Requirement
from packaging.version import Version


pytestmark = pytest.mark.integration

CODE_ROOT = Path(__file__).parents[2]


def _pyproject(repository):
    with (CODE_ROOT / repository / "pyproject.toml").open("rb") as stream:
        return tomllib.load(stream)


def _compas_requirement(requirements):
    return next(Requirement(value) for value in requirements if Requirement(value).name == "compas")


def _assert_compas_3(requirement, *, bounded=False):
    assert Version("3.0.0") in requirement.specifier
    assert Version("2.99.99") not in requirement.specifier
    if bounded:
        assert Version("3.99.99") in requirement.specifier
        assert Version("4.0.0") not in requirement.specifier


@pytest.mark.parametrize("repository", ["compas_occ", "compas_cgal", "compas_libigl"])
def test_plugin_packages_require_compas_3(repository):
    requirement = _compas_requirement(_pyproject(repository)["project"]["dependencies"])

    _assert_compas_3(requirement)


def test_cgal_runtime_wheel_and_pixi_use_the_same_compas_3_line():
    configuration = _pyproject("compas_cgal")
    runtime = _compas_requirement(configuration["project"]["dependencies"])
    wheel = _compas_requirement(configuration["tool"]["cibuildwheel"]["test-requires"])
    pixi = Requirement("compas" + configuration["tool"]["pixi"]["dependencies"]["compas"])

    for requirement in (runtime, wheel, pixi):
        _assert_compas_3(requirement, bounded=True)


def test_libigl_wheel_setup_uses_compas_3():
    configuration = _pyproject("compas_libigl")["tool"]["cibuildwheel"]
    requirement = _compas_requirement(configuration["test-requires"])
    before_test = configuration["before-test"]

    _assert_compas_3(requirement)
    assert "compas>=3.0.0" in before_test.replace(" ", "")
    assert "compas>=2" not in before_test.replace(" ", "")
