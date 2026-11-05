# Definitions

## Poligonisation

To divide into polygons.

Polygonisation divides parametric surfaces and shapes into quads where possible, and triangles where necessary (for example, near the poles of a sphere).

The objective is to create structured, discrete representations.

The output is a `PolygonalSurface`.

Since BReps don't have a clear underlying uniform structure, they cannot be converted to a polygonal representation in this way.

## Triangulation

To divide into triangles.

Polygons can be divided into triangles using various strategies.

Quads can be split along a diagonal.

Ngons can be split using earclipping or through a delaunay triangulation, depending on the desired qualities of the result.

Polygons that are near planar can still be processed in this way by projecting onto a bestfit plane.

Polygons that are far from planar require more sophisticated approaches that may require the insertion of additional points.

For general planar regions different delaunay strategies exist to generate (constrained) triangulations.

## Tessellation

Although technically, this means to populate a surface or shape with noon-overlapping tiles, in the context of computational geometry, it is often understood as a form of triangulation, usually for visualisation purposes, of BReps and trimmed (nurbs) surfaces, with a required precision, typically formulated through a linear and/or angular deflection criteria.
