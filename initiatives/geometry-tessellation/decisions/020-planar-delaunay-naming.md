# Title: Should Delaunay triangulation operations state their planar contract in their names?

## Status

Accepted

## Context

The public operations `triangulate_points(...)` and
`triangulate_domain(...)` operate only on planar input. They use world XY or an
explicit `Frame`, validate that all input lies on that plane, and return a
planar `Tessellation`. Their unqualified names hide this material precondition
and are ambiguous beside polygon triangulation and any future 3D Delaunay or
tetrahedralization operation.

The associated strategy classes are named `Delaunay`, `ConstrainedDelaunay`,
and `ConformingDelaunay`. These are standard algorithm names selected within an
already planar operation.

## Options

1. Keep all existing names and rely on documentation for the planar
   precondition.
2. Add `Planar` to both operations and all strategy classes. This is explicit
   but produces verbose, nonstandard algorithm names.
3. Rename the public operations and plugin selectors to state the planar
   contract, while retaining the standard strategy class names.

## Recommendation

Choose option 3. Rename:

```python
triangulate_points(...)  -> triangulate_planar_points(...)
triangulate_domain(...)  -> triangulate_planar_domain(...)
```

The names follow COMPAS's verb-object convention and expose the input contract
at the operation boundary. Rename the corresponding core pluggables and CGAL
plugin registrations because plugin dispatch is name-based. Rename private
Python backend adapters for consistency where practical.

Keep:

- `Delaunay`
- `ConstrainedDelaunay`
- `ConformingDelaunay`
- `TriangulationQuality`
- the `triangulation_delaunay` module name
- native C++ algorithm identifiers where they are internal

The strategy names identify standard algorithms and gain their planar context
from the accepting operation. Do not add compatibility aliases under ADR 013.

## Consequences

- Planarity is visible at every public call site.
- The names remain unambiguous beside `triangulate_polygon` and any future 3D
  tetrahedralization API.
- Core exports, `Mesh.from_points`, CGAL plugin registrations/adapters, tests,
  API documentation, examples, and framework integration require coordinated
  migration.
- Historical changelogs and inventory records may retain old names when clearly
  historical.

## Affected packages

`compas`, `compas_cgal`, and `compas_framework`.

## Dependencies

- [003 — Strategy objects](003-strategy-objects.md)
- [011 — Planar triangulation contract](011-planar-triangulation-contract.md)
- [012 — Plugin boundaries](012-plugin-boundaries.md)
- [013 — Compatibility](013-compatibility.md)
