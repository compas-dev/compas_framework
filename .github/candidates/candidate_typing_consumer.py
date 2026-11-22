"""External type consumer for exact installed native candidate wheels."""

# pyright: strict

from typing import assert_type

from compas.datastructures import Mesh
from compas.typing import VerticesFaces
from compas_cgal.triangulation import delaunay_triangulation
from compas_cgal.types import DelaunayResult
from compas_libigl.geodistance import trimesh_geodistance

points = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
]
inferred = delaunay_triangulation(points)
assert_type(inferred, DelaunayResult)
result: DelaunayResult = inferred
structural: VerticesFaces = result
mesh: Mesh = Mesh.from_vertices_and_faces(*result)
distances = trimesh_geodistance(structural, 0)
assert_type(distances, list[float])

assert mesh.number_of_vertices() == len(distances)
