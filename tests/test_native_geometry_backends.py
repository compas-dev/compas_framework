from copy import deepcopy
from importlib import import_module
from math import pi
from typing import Any
from typing import cast

import pytest

from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Circle
from compas.geometry import ConstrainedDelaunay
from compas.geometry import Deflection
from compas.geometry import Native
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Tessellation
from compas.geometry import Vector
from compas.geometry import intersection_ray_mesh
from compas.geometry import triangulate_planar_domain
from compas.geometry import trimesh_geodistance
from compas.geometry import trimesh_harmonic
from compas.geometry import trimesh_isolines
from compas.geometry import trimesh_lscm
from compas.geometry import trimesh_massmatrix
from compas.geometry import trimesh_remesh_along_isoline
from compas.geometry import trimesh_slice
from compas.plugins import plugin_manager


pytestmark = [pytest.mark.integration, pytest.mark.native_backend]


@pytest.fixture(autouse=True)
def reset_plugin_discovery():
    plugin_manager.reset()
    yield
    plugin_manager.reset()


def require_native_module(module_name, backend):
    try:
        return import_module(module_name)
    except ImportError as error:
        pytest.skip(f"{backend} native extension unavailable: {error}")


def signed_area_xy(points):
    return 0.5 * sum(points[index][0] * points[(index + 1) % len(points)][1] - points[(index + 1) % len(points)][0] * points[index][1] for index in range(len(points)))


def signed_triangle_area_xy(vertices, triangle):
    a, b, c = (vertices[index] for index in triangle)
    return 0.5 * ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def test_occ_brep_tessellation_exports_buffers_for_cgal_slice():
    require_native_module("OCC.Core.TopoDS", "Open CASCADE")
    require_native_module("compas_cgal._slicer", "CGAL slicer")
    brep = Brep.from_box(Box(1))
    strategy = Deflection(0.05, 12.0)

    with pytest.raises(TypeError):
        cast(Any, brep).tessellate()

    tessellation = brep.tessellate(strategy)
    polygonal = brep.polygonize(strategy)
    slices = trimesh_slice(tessellation.to_vertices_and_triangles(), [Plane(Point(0, 0, 0), Vector(0, 0, 1))])

    assert isinstance(tessellation, Tessellation)
    assert tessellation.number_of_triangles == 12
    assert len(tessellation.polylines) == 12
    assert len(polygonal.faces) == tessellation.number_of_triangles
    assert slices
    assert all(len(point) == 3 for polyline in slices for point in polyline)


def test_occ_trimmed_planar_brep_preserves_hole_and_exports_cgal_input():
    require_native_module("OCC.Core.TopoDS", "Open CASCADE")
    require_native_module("compas_cgal._slicer", "CGAL slicer")
    from compas_occ.brep import OCCBrepEdge
    from compas_occ.brep import OCCBrepFace
    from compas_occ.brep import OCCBrepLoop

    boundary = OCCBrepLoop.from_edges([OCCBrepEdge.from_circle(Circle(2.0))])
    hole = OCCBrepLoop.from_edges([OCCBrepEdge.from_circle(Circle(0.5))])
    face = OCCBrepFace.from_plane(Plane.worldXY(), boundary=boundary, holes=[hole])
    brep = Brep.from_brepfaces([face])

    tessellation = brep.tessellate(Deflection(0.05, 12.0))
    vertices_before = deepcopy(tessellation.vertices)
    triangles_before = deepcopy(tessellation.triangles)
    slices = trimesh_slice(tessellation.to_vertices_and_triangles(), [Plane(Point(0, 0, 0), Vector(1, 0, 0))])

    triangle_areas = [signed_triangle_area_xy(tessellation.vertices, triangle) for triangle in tessellation.triangles]
    boundary_areas = [signed_area_xy(polyline) for polyline in tessellation.polylines]
    assert brep.area == pytest.approx(pi * (2.0**2 - 0.5**2))
    assert sum(triangle_areas) == pytest.approx(brep.area, rel=0.02)
    assert all(area > 0.0 for area in triangle_areas)
    assert len(tessellation.polylines) == 2
    assert all(area > 0.0 for area in boundary_areas)
    assert abs(boundary_areas[0]) > abs(boundary_areas[1])
    assert slices
    assert tessellation.vertices == vertices_before
    assert tessellation.triangles == triangles_before


def test_cgal_domain_dispatch_uses_canonical_contract():
    require_native_module("compas_cgal._triangulation", "CGAL")
    boundary = [[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0]]
    hole = [[0.5, 0.5, 0], [1.5, 0.5, 0], [1.5, 1.5, 0], [0.5, 1.5, 0]]
    boundary_before = deepcopy(boundary)
    hole_before = deepcopy(hole)

    result = triangulate_planar_domain(boundary, holes=[hole], strategy=ConstrainedDelaunay())

    assert isinstance(result, Tessellation)
    assert result.number_of_vertices >= len(boundary) + len(hole)
    assert result.number_of_triangles > 0
    dtype = getattr(result.triangles, "dtype", None)
    assert dtype is not None
    assert dtype.name == "int32"
    assert boundary == boundary_before
    assert hole == hole_before
    assert min(min(triangle) for triangle in result.triangles) >= 0
    assert max(max(triangle) for triangle in result.triangles) < result.number_of_vertices
    areas = [signed_triangle_area_xy(result.vertices, triangle) for triangle in result.triangles]
    assert all(area > 0.0 for area in areas)
    assert sum(areas) == pytest.approx(3.0)
    for triangle in result.triangles:
        centroid = [sum(result.vertices[index][axis] for index in triangle) / 3.0 for axis in range(2)]
        assert not (0.5 < centroid[0] < 1.5 and 0.5 < centroid[1] < 1.5)


def test_libigl_structural_mesh_algorithms():
    require_native_module("compas_libigl._intersections", "libigl")
    require_native_module("compas_libigl._geodistance", "libigl")
    require_native_module("compas_libigl._isolines", "libigl")
    require_native_module("compas_libigl._massmatrix", "libigl")
    tessellation = Box(1).tessellate(Native())
    vertices, triangles = tessellation.to_vertices_and_triangles()
    vertices_before = deepcopy(vertices)
    triangles_before = deepcopy(triangles)
    mesh = (vertices, triangles)

    hits = intersection_ray_mesh(([-2, 0, 0], [1, 0, 0]), mesh)
    distances = trimesh_geodistance(mesh, 0)
    scalarfield = [vertex[0] + 2.0 * vertex[1] + 3.0 * vertex[2] for vertex in vertices]
    points, segments = trimesh_isolines(mesh, scalarfield, 3)
    masses = trimesh_massmatrix(mesh)

    assert len(distances) == tessellation.number_of_vertices
    assert len(masses) == tessellation.number_of_vertices
    assert hits
    assert len(points) > 0
    assert len(segments) > 0
    assert all(len(point) == 3 for point in points)
    assert all(len(segment) == 2 for segment in segments)
    assert vertices == vertices_before
    assert triangles == triangles_before


def test_libigl_structural_mesh_parametrisation():
    require_native_module("compas_libigl._parametrisation", "libigl")
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    triangles = [[0, 1, 2], [0, 2, 3]]
    vertices_before = deepcopy(vertices)
    triangles_before = deepcopy(triangles)
    mesh = (vertices, triangles)

    harmonic = trimesh_harmonic(mesh)
    lscm = trimesh_lscm(mesh)

    assert len(harmonic) == len(vertices)
    assert len(lscm) == len(vertices)
    assert all(len(uv) == 2 for uv in harmonic)
    assert all(len(uv) == 2 for uv in lscm)
    assert vertices == vertices_before
    assert triangles == triangles_before


def test_libigl_remesh_along_isoline_uses_structural_mesh_contract():
    require_native_module("compas_libigl._meshing", "libigl")
    tessellation = Box(1).tessellate(Native())
    vertices, triangles = tessellation.to_vertices_and_triangles()
    vertices_before = deepcopy(vertices)
    triangles_before = deepcopy(triangles)
    scalarfield = [vertex[2] for vertex in vertices]

    result_vertices, result_triangles = trimesh_remesh_along_isoline(
        (vertices, triangles),
        scalarfield,
        0.0,
    )

    assert len(result_vertices) > 0
    assert len(result_triangles) > 0
    assert all(len(vertex) == 3 for vertex in result_vertices)
    assert all(len(triangle) == 3 for triangle in result_triangles)
    assert vertices == vertices_before
    assert triangles == triangles_before
