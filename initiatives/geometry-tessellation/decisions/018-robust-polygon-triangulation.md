# Title: How should COMPAS triangulate polygons beyond valid planar face rings?

## Status

Accepted

## Context

Accepted ADR 017 separates quad and n-gon policies but preserves the existing
face-decomposition contract: triangles reference only the original face
vertices and no new topology is introduced.

That contract covers valid simple planar rings. It does not cover every input
commonly called a polygon:

- holes require multiple rings;
- self-intersections require a fill rule and intersection vertices;
- touching or retraced contours require arrangement and repair semantics;
- slightly warped rings require an explicit projection decision;
- arbitrary spatial loops do not define a unique surface.

`PolygonalSurface` faces contain one index ring and cannot represent holes.
`PlanarRegion` represents an exterior ring plus holes. `Tessellation` can carry
new vertices, but the current face helper returns only indices into existing
vertices. Hiding repair and vertex insertion in a face strategy would leave
Mesh keys, attributes, shared-edge splitting, and crack prevention undefined.

Mapbox Earcut is suitable for valid rings but does not guarantee arbitrary
invalid input. The current CGAL constrained-domain backend supports planar
boundaries, holes, and constraints, but does not yet provide an exact-
intersection contract for arbitrary self-intersecting arrangements.

## Options

1. Add one `Robust` face strategy that attempts projection, repair,
   intersection, and triangulation. This is convenient but silently chooses
   geometry semantics and breaks the no-insertion face contract.
2. Try progressively more permissive algorithms until one succeeds. This can
   turn invalid geometry into an unnoticed reinterpretation.
3. Separate strict face decomposition, explicit near-planar projection,
   planar-domain/arrangement tessellation, and spatial surface construction.

## Recommendation

Choose option 3.

### Strict face triangulation

Keep `FaceTriangulation` as the normal collection policy. `EarClipping`
accepts a valid simple planar ring, including concave polygons and supported
collinear boundary vertices, without inserting vertices. It rejects duplicate
coordinates, zero-length edges, zero area, self-intersection, and
non-planarity. `DiagonalSplit` retains its explicit warped-quad semantics.

### Explicit near-planar faces

Add a separately named leaf strategy:

```python
ProjectedEarClipping(max_deviation=...)
```

It computes a documented best-fit plane, rejects vertices farther than
`max_deviation`, rejects degenerate or self-intersecting projections,
triangulates the projected simple ring, and returns indices into the original
3D vertices. Projection is never an implicit fallback. This strategy may be
used as `FaceTriangulation.ngon` and, when explicitly selected, as its quad
policy.

### Planar regions with holes

Use `PlanarRegion` and domain-level triangulation. Results are independent
`Tessellation` objects and may contain generated vertices when permitted by the
selected constrained or conforming strategy.

### Self-intersecting planar contours

Introduce a separate plugin operation:

```python
triangulate_planar_arrangement(
    contours,
    plane=plane,
    strategy=PlanarArrangement(fill_rule="even_odd"),
) -> Tessellation
```

The plane and fill rule are explicit. Initially support `even_odd` and
`nonzero`. The operation resolves proper intersections and touches, may insert
intersection vertices, and may produce multiple filled components and holes.
Generated vertices lie on the supplied plane. Unsupported coincident or
retraced segments and zero-area inputs raise precise errors.

Do not expose this operation until a backend provides the stated robust
intersection contract. The existing inexact-construction CGAL implementation
is not sufficient evidence by itself; an exact-intersection implementation and
tests are required.

### Arbitrary spatial loops

Keep arbitrary non-planar loops outside polygon triangulation. They require a
separately named surface-patch or hole-filling operation with an explicit
objective or supplied support surface. Defer that API until there is a concrete
consumer and backend.

## Consequences

- “Robust” does not mean silently repairing or projecting invalid geometry.
- Normal `PolygonalSurface` and Mesh triangulation remains no-insertion and
  atomic.
- Slightly warped imported faces have an explicit bounded-deviation policy.
- Holes, intersections, fill rules, multiple components, and generated
  vertices use domain-level `Tessellation` results.
- Arrangement processing cannot be hidden inside per-face Mesh triangulation,
  avoiding inconsistent shared-edge splits and cracks.
- Backend absence or insufficient robustness produces an explicit unavailable-
  plugin error rather than a weaker fallback.
- Tests must cover concavity, collinear boundary vertices, projection
  deviation, projected self-intersection, fill rules, intersection vertices,
  components, holes, non-planar rejection, and backend absence.

## Affected packages

`compas`, `compas_cgal`, and documentation/examples in `compas_framework`.

## Dependencies

- [003 — Strategy objects](003-strategy-objects.md)
- [007 — Triangulation operations](007-triangulation-operations.md)
- [011 — Planar triangulation contract](011-planar-triangulation-contract.md)
- [012 — Plugin boundaries](012-plugin-boundaries.md)
- [017 — Mixed-face triangulation](017-mixed-face-triangulation.md)
