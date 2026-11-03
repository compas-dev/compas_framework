# Title: Should output topology be part of the tessellation strategy or a separate choice?

## Status

Accepted

## Context

`Surface.compute_faces()` produces a quad grid while
`Surface.compute_tessellation()` splits that grid into triangles. Shapes may
produce mixed triangle/quad topology, and trimmed BReps naturally produce
triangles. The objective asks to separate tessellation from triangulation and
consider output topology independently from approximation policy.

Returning triangles, quads, or polygons from one method based on a flag or
strategy would make return semantics and downstream validation unstable.

## Options

1. Put topology inside each strategy and allow `compute_tessellation()` to
   return unrelated representation types. This is flexible but complicates
   typing, caching, and consumers.
2. Make every tessellator return triangles and remove polygon-preserving
   conversions. This simplifies plugins but discards useful source topology.
3. Keep triangle tessellation as the stable computational interchange and add
   a separate topology-preserving `polygonize(strategy)` operation returning
   `PolygonalSurface`, followed by triangulation when needed.
4. Add separate triangle and quad strategy hierarchies. This makes topology
   explicit but duplicates sampling policy.

## Recommendation

Choose option 3. Sampling policy and output topology are conceptually separate,
and both public operations have stable return types:

```python
geometry.polygonize(strategy) -> PolygonalSurface
geometry.tessellate(strategy) -> Tessellation
```

`polygonize(strategy)` is a fresh, non-mutating, topology-preserving operation
for continuous surface-like geometry. It returns an independent, persistent,
serializable `PolygonalSurface`; it never returns `Mesh`. There is no cached
property, scalar-control alternative, or topology flag. A caller that needs
half-edge topology explicitly calls `.to_mesh()` on the polygonal result.

The operation applies to analytical `Shape`, parametric `Surface`, untrimmed
`NurbsSurface`, and `BrepFace`/`Brep` when the backend can provide a polygonal
result. Curves are excluded because their discrete connected result is a
`Polyline`, not a `PolygonalSurface`.

`polygonize` reuses the same `TessellationStrategy` objects as `tessellate`.
It preserves the natural face cells produced by the geometry/backend:

- `Native` preserves fixed natural topology, for example on `Box`.
- `UGrid` controls one-parameter analytical shapes such as `Cylinder` and
  `Cone`.
- `UVGrid` on regular parametric surfaces guarantees quadrilateral cells.
- `Capsule`, `Sphere`, `Torus`, and general parametric surfaces use both
  `UVGrid` dimensions.
- Analytical shapes may naturally produce mixed triangle/quad topology.
- `Deflection` and `Adaptive` do not guarantee quadrilateral output.
- Unsupported geometry/strategy/backend combinations raise an error and are
  never silently approximated with a different policy. Dimensions are never
  ignored to make an invalid combination appear supported.

## Consequences

- Triangle-oriented plugins receive a predictable representation.
- Quad, mixed, and source-natural topology remain available through a
  predictable persistent representation without union return types.
- A workflow may intentionally have two steps: create a topology-preserving
  polygonal discretization, then triangulate it.
- Documentation must distinguish a topology-preserving conversion from a
  triangle conversion.
- Tests must verify result independence, serialization, non-mutation, explicit
  `.to_mesh()` conversion, curve exclusion, strategy support errors, and the
  topology guarantees of each strategy/producer family.
- Regression tests must ensure original boundaries are not confused with
  generated diagonals.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_model`, and
`compas_framework`.

## Dependencies

- [001 — Terminology](001-terminology.md)
- [002 — Mesh representations](002-mesh-representations.md)
- [003 — Strategy objects](003-strategy-objects.md)
