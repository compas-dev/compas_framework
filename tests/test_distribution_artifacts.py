import os
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


DEVELOPMENT_DEPENDENCIES = {"build", "invoke", "mkdocs", "pyright", "pytest", "ruff", "twine"}


def test_built_distributions_are_complete():
    distribution_directory = Path(os.environ["COMPAS_FRAMEWORK_DIST_DIR"])
    wheels = sorted(distribution_directory.glob("*.whl"))
    sdists = sorted(distribution_directory.glob("*.tar.gz"))

    assert len(wheels) == 1
    assert len(sdists) == 1

    with zipfile.ZipFile(wheels[0]) as archive:
        names = archive.namelist()
        metadata_path = next(name for name in names if name.endswith(".dist-info/METADATA"))
        metadata = BytesParser().parsebytes(archive.read(metadata_path))

    raw_requirements = metadata.get_all("Requires-Dist", [])
    requirements = {Requirement(value) for value in raw_requirements}
    assert "compas_framework/__init__.py" in names
    assert set(metadata["Requires-Python"].split(",")) == {">=3.12", "<3.15"}
    assert DEVELOPMENT_DEPENDENCIES.isdisjoint(canonicalize_name(requirement.name) for requirement in requirements)
    project = tomllib.loads((Path(__file__).resolve().parents[1] / "pyproject.toml").read_text())["project"]
    assert requirements == {Requirement(value) for value in project["dependencies"]}
    assert metadata.get_all("Provides-Extra", []) == []
    assert all("extra ==" not in requirement for requirement in raw_requirements)

    with tarfile.open(sdists[0], mode="r:gz") as archive:
        members = archive.getnames()

    for required in ("LICENSE", "README.md", "pyproject.toml", "src/compas_framework/__init__.py"):
        assert any(member.endswith(f"/{required}") for member in members)
