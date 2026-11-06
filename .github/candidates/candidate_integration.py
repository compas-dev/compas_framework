"""Installed-artifact integration contracts for the Linux Python 3.12 gate."""

from importlib.metadata import distribution

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Brep
from compas.plugins import PluginManager
from compas_cgal.triangulation import delaunay_triangulation
from compas_libigl.geodistance import trimesh_geodistance


def test_exact_candidate_distributions_are_installed() -> None:
    for name in ("compas", "compas_occ", "compas_cgal", "compas_libigl", "compas_framework"):
        assert distribution(name).version


def test_installed_entry_points_discover_lightweight_plugins() -> None:
    manager = PluginManager()

    assert manager.load_plugins() > 0

    modules = {implementation.plugin.__name__ for implementations in manager.registry.values() for implementation in implementations}
    assert any(name.startswith("compas_occ.plugins.") for name in modules)
    assert any(name.startswith("compas_cgal.plugins.") for name in modules)
    assert any(name.startswith("compas_libigl.plugins.") for name in modules)


def test_cgal_result_passes_directly_to_core_and_libigl() -> None:
    result = delaunay_triangulation(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
        ]
    )

    mesh = Mesh.from_vertices_and_faces(*result)
    distances = trimesh_geodistance(result, 0)

    assert mesh.number_of_vertices() == len(result[0])
    assert mesh.number_of_faces() == len(result[1])
    assert len(distances) == len(result[0])
    assert distances[0] == 0.0


def test_occ_backend_constructs_core_brep() -> None:
    brep = Brep.from_box(Box.from_width_height_depth(1.0, 1.0, 1.0))
    tessellation = brep.to_tessellation()

    assert brep.volume > 0.0
    assert tessellation.number_of_triangles > 0
