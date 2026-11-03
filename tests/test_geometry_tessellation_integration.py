from typing import Any
from typing import cast

import pytest

import compas
from compas.geometry import Adaptive
from compas.geometry import Box
from compas.geometry import CylindricalSurface
from compas.geometry import Deflection
from compas.geometry import DiagonalSplit
from compas.geometry import FaceTriangulation
from compas.geometry import MinimumAreaTriangulation
from compas.geometry import Native
from compas.geometry import PlanarSurface
from compas.geometry import PolygonalSurface
from compas.geometry import ProjectedEarClipping
from compas.geometry import Tessellation
from compas.geometry import UVGrid


pytestmark = pytest.mark.integration


def test_shape_and_surface_use_stable_discrete_representations():
    box = Box(1)
    box_data = box.__data__

    polygonal = box.polygonize(Native())
    tessellation = box.tessellate(Native())

    assert isinstance(polygonal, PolygonalSurface)
    assert isinstance(tessellation, Tessellation)
    assert len(polygonal.faces) == 6
    assert tessellation.number_of_triangles == 12
    assert box.__data__ == box_data
    assert not hasattr(box, "resolution_u")
    assert not hasattr(box, "resolution_v")

    surface = PlanarSurface()
    surface_data = surface.__data__
    strategy = UVGrid(3, 2)
    surface_polygonal = surface.polygonize(strategy)
    surface_tessellation = surface.tessellate(strategy)
    vertex_normals = surface_tessellation.vertex_normals
    texture_coordinates = surface_tessellation.texture_coordinates

    assert len(surface_polygonal.faces) == 6
    assert surface_tessellation.number_of_triangles == 12
    assert vertex_normals is not None
    assert texture_coordinates is not None
    assert len(vertex_normals) == surface_tessellation.number_of_vertices
    assert len(texture_coordinates) == surface_tessellation.number_of_vertices
    assert surface.__data__ == surface_data
    assert not hasattr(surface, "resolution_u")
    assert not hasattr(surface, "resolution_v")


def test_shape_and_surface_tessellation_defaults_are_deterministic_and_fresh():
    box = Box(1)
    box_data = box.__data__

    box_default = box.tessellate()
    box_none = box.tessellate(None)
    box_explicit = box.tessellate(Native())

    assert box_default is not box_none
    assert [tuple(vertex) for vertex in box_default.vertices] == [tuple(vertex) for vertex in box_explicit.vertices]
    assert [tuple(triangle) for triangle in box_none.triangles] == [tuple(triangle) for triangle in box_explicit.triangles]
    assert box_default.number_of_vertices == 8
    assert box_default.number_of_triangles == 12
    assert box.__data__ == box_data

    surface = PlanarSurface()
    surface_data = surface.__data__

    surface_default = surface.tessellate()
    surface_none = surface.tessellate(None)
    surface_explicit = surface.tessellate(UVGrid(64, 64))

    assert surface_default is not surface_none
    assert surface_default.number_of_vertices == 4225
    assert surface_default.number_of_triangles == 8192
    assert [tuple(vertex) for vertex in surface_default.vertices] == [tuple(vertex) for vertex in surface_explicit.vertices]
    assert [tuple(triangle) for triangle in surface_none.triangles] == [tuple(triangle) for triangle in surface_explicit.triangles]
    assert surface.__data__ == surface_data

    with pytest.raises(TypeError):
        cast(Any, box).polygonize()


def test_direct_and_explicit_two_step_paths_preserve_geometry():
    surface = PlanarSurface()
    strategy = UVGrid(3, 2)

    direct = surface.tessellate(strategy)
    explicit = surface.polygonize(strategy).triangulated(FaceTriangulation(quad=DiagonalSplit("02")))

    assert [tuple(vertex) for vertex in direct.vertices] == [tuple(vertex) for vertex in explicit.vertices]
    assert {tuple(triangle) for triangle in direct.triangles} == {tuple(triangle) for triangle in explicit.triangles}


def test_periodic_surface_preserves_seam_normals_and_uv_coordinates():
    surface = CylindricalSurface(2.0)
    strategy = UVGrid(4, 2)

    tessellation = surface.tessellate(strategy)
    vertex_normals = tessellation.vertex_normals
    texture_coordinates = tessellation.texture_coordinates

    assert vertex_normals is not None
    assert texture_coordinates is not None

    for v_index in range(strategy.v + 1):
        first = v_index
        last = strategy.u * (strategy.v + 1) + v_index
        assert tuple(tessellation.vertices[first]) == pytest.approx(tuple(tessellation.vertices[last]))
        assert tuple(vertex_normals[first]) == pytest.approx(tuple(vertex_normals[last]))
        assert texture_coordinates[first][0] == 0.0
        assert texture_coordinates[last][0] == 1.0


@pytest.mark.roundtrip
@pytest.mark.parametrize(
    "strategy",
    [
        Native(),
        UVGrid(3, 2),
        Deflection(0.05, 12.0),
        Adaptive(max_deviation=0.1, max_angle=15.0),
        ProjectedEarClipping(0.01),
        MinimumAreaTriangulation(),
        FaceTriangulation(quad=MinimumAreaTriangulation(), ngon=ProjectedEarClipping(0.01)),
    ],
)
def test_strategy_data_roundtrips_across_the_framework_boundary(strategy):
    restored = compas.json_loads(compas.json_dumps(strategy))

    assert type(restored) is type(strategy)
    assert restored == strategy


@pytest.mark.roundtrip
def test_persistent_polygonal_surface_roundtrips_but_tessellation_does_not():
    polygonal = Box(1).polygonize(Native())
    tessellation = Box(1).tessellate(Native())

    restored = compas.json_loads(compas.json_dumps(polygonal))

    assert isinstance(restored, PolygonalSurface)
    assert restored.__data__ == polygonal.__data__
    with pytest.raises(TypeError):
        compas.json_dumps(tessellation)


def test_plugin_boundaries_reject_raw_triangle_tuples():
    from compas.geometry import Plane
    from compas.geometry import trimesh_slice

    raw = Box(1).tessellate(Native()).to_vertices_and_triangles()

    with pytest.raises(TypeError, match="Tessellation"):
        trimesh_slice(cast(Any, raw), [Plane.worldXY()])
