"""External type consumer for installed native integration candidates."""

# pyright: strict

import site
from pathlib import Path
from types import ModuleType
from typing import assert_type

import compas
import compas_cgal
import compas_libigl
import compas_occ
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Native
from compas.typing import Float64Array
from compas.typing import Int32Array
from compas.typing import RayMeshHit
from compas.typing import VerticesFaces
from compas_cgal.triangulation import delaunay_triangulation
from compas_cgal.types import DelaunayResult
from compas_libigl.geodistance import trimesh_geodistance
from compas_libigl.intersections import intersection_ray_mesh
from compas_libigl.isolines import trimesh_isolines
from compas_libigl.massmatrix import trimesh_massmatrix
from compas_libigl.meshing import trimesh_remesh_along_isoline
from compas_libigl.parametrisation import trimesh_harmonic
from compas_libigl.parametrisation import trimesh_lscm
from compas_occ.brep import OCCBrep


def assert_installed(module: ModuleType) -> None:
    """Assert that a candidate module was imported from the environment."""
    origin = module.__file__
    assert origin is not None, f"Cannot determine the origin of {module.__name__}."
    path = Path(origin).resolve()
    installation_roots = [Path(location).resolve() for location in site.getsitepackages()]
    assert any(path.is_relative_to(root) for root in installation_roots), f"{module.__name__} was imported from {path}, not an installed-package location."


def consume_native_geometry_packages() -> None:
    """Exercise coordinated public runtime and typing contracts."""
    for module in (compas, compas_occ, compas_cgal, compas_libigl):
        assert_installed(module)

    box = assert_type(Box(1), Box)
    tessellation = box.tessellate(Native())
    occ_direct = assert_type(OCCBrep.from_box(box), OCCBrep)
    occ_plugin = assert_type(Brep.from_box(box), Brep)

    points = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
    delaunay = assert_type(delaunay_triangulation(points), DelaunayResult)
    structural: VerticesFaces = delaunay
    mesh = Mesh.from_vertices_and_faces(*delaunay)

    triangles = [[0, 1, 2], [0, 2, 3]]
    triangle_mesh: VerticesFaces = (points, triangles)
    scalarfield = [point[0] + point[1] for point in points]

    hits = assert_type(
        intersection_ray_mesh(([-1.0, 0.5, 0.0], [1.0, 0.0, 0.0]), triangle_mesh),
        list[RayMeshHit],
    )
    distances = assert_type(trimesh_geodistance(triangle_mesh, 0), list[float])
    isolines = assert_type(
        trimesh_isolines(triangle_mesh, scalarfield, 2),
        tuple[list[list[float]], list[list[int]]],
    )
    masses = assert_type(trimesh_massmatrix(triangle_mesh), list[float])
    harmonic = assert_type(trimesh_harmonic(triangle_mesh), list[list[float]])
    lscm = assert_type(trimesh_lscm(triangle_mesh), list[list[float]])
    remeshed = assert_type(
        trimesh_remesh_along_isoline(triangle_mesh, scalarfield, 0.5),
        tuple[Float64Array, Int32Array],
    )

    assert tessellation.number_of_triangles > 0
    assert occ_direct.volume > 0.0
    assert occ_plugin.volume > 0.0
    assert mesh.number_of_vertices() == len(structural[0])
    assert hits
    assert len(distances) == len(points)
    assert len(isolines) == 2
    assert len(masses) == len(points)
    assert len(harmonic) == len(points)
    assert len(lscm) == len(points)
    assert len(remeshed) == 2


if __name__ == "__main__":
    consume_native_geometry_packages()
