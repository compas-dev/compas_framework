import os
import re
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path


RUNTIME_DEPENDENCIES = {
    "compas",
    "compas-cgal",
    "compas-gmsh",
    "compas-libigl",
    "compas-model",
    "compas-occ",
    "compas-session",
    "compas-shapeop",
    "compas-viewer",
}
DEVELOPMENT_DEPENDENCIES = {"build", "invoke", "mkdocs", "pyright", "pytest", "ruff", "twine"}


def canonical_name(requirement: str) -> str:
    name = re.split(r"[ (;<>=]", requirement, maxsplit=1)[0]
    return re.sub(r"[-_.]+", "-", name).lower()


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
    requirements = {canonical_name(requirement) for requirement in raw_requirements}
    assert "compas_framework/__init__.py" in names
    assert set(metadata["Requires-Python"].split(",")) == {">=3.12", "<3.15"}
    assert RUNTIME_DEPENDENCIES <= requirements
    assert DEVELOPMENT_DEPENDENCIES.isdisjoint(requirements)
    assert metadata.get_all("Provides-Extra", []) == []
    assert all("extra ==" not in requirement for requirement in raw_requirements)

    with tarfile.open(sdists[0], mode="r:gz") as archive:
        members = archive.getnames()

    for required in ("LICENSE", "README.md", "pyproject.toml", "src/compas_framework/__init__.py"):
        assert any(member.endswith(f"/{required}") for member in members)
