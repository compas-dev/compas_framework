# Title: How should COMPAS triangulate a heavily twisted 3D polygon without projection?

## Status

Accepted

## Context

ADR 017 defines `DiagonalSplit` and `EarClipping` as leaf policies used by the
composite `FaceTriangulation`. `EarClipping` is intentionally limited to planar
polygons. A heavily twisted ordered 3D boundary may have no intersection-free
planar projection, but can still be spanned combinatorially by triangles using
only its boundary vertices.

No primary source was found for an algorithm named “Seitz–Belyaev Dynamic
Programming.” The established literature is the Barequet–Sharir dynamic
program for a single 3D polygon with additive per-triangle weights, followed by
the Barequet–Dickerson–Eppstein extension for adjacent-triangle weights.

The existing helper is named `triangulate_face`, although it consumes one
ordered polygon boundary and is also used by `Polygon`. `triangulate_polygon`
describes that contract more directly. Delaunay strategies belong to separate
planar point/domain APIs and are not leaf polygon-decomposition strategies.

## Options

1. Add a strategy named `SeitzBelyaev`. This uses an unverifiable attribution
   and leaves its optimization objective unspecified.
2. Add a configurable dynamic program supporting area, edge length, dihedral
   angle, and combined costs. This is flexible but introduces speculative
   complexity, multiple state formulations, and unclear defaults.
3. Add one explicitly named minimum-area dynamic-programming strategy with a
   narrow, documented contract.

## Recommendation

Choose option 3. Add:

```python
MinimumAreaTriangulation()
```

For ordered vertices `0 ... n - 1`, minimize the sum of triangle areas with
the recurrence:

```text
W(i, j) = min over i < k < j of
          area(i, k, j) + W(i, k) + W(k, j)
```

The strategy:

- accepts one ordered 3D polygon boundary;
- performs no planar projection;
- inserts no vertices;
- returns exactly `n - 2` consistently oriented index triples;
- preserves the input boundary order;
- rejects fewer than three vertices, repeated boundary vertices, zero-length
  boundary edges, and degenerate candidate triangles required by a result;
- uses deterministic lowest-index tie-breaking;
- takes `O(n^3)` time and `O(n^2)` space.

The result is a combinatorially manifold disk, but is not guaranteed to be a
geometrically embedded or intersection-free surface. Document this limitation
prominently. Do not add an expensive intersection-free guarantee: deciding
whether a general 3D polygon has such a triangulation without additional
vertices is computationally intractable in the general case.

Allow `MinimumAreaTriangulation` as both the `quad` and `ngon` policy of
`FaceTriangulation`. It is opt-in and never an implicit fallback from
`EarClipping`.

Rename the internal helper:

```python
triangulate_face(...) -> triangulate_polygon(...)
```

The helper remains distinct from Delaunay point/domain triangulation and
planar-arrangement operations. Collection-level callers continue using
`FaceTriangulation`.

Do not implement adjacent-triangle or dihedral-angle objectives now. They need
an `O(n^4)`/`O(n^3)` dynamic-programming state and should be introduced only
for a concrete requirement through a separate decision.

## Consequences

- Twisted polygons gain a deterministic no-projection triangulation policy.
- The public strategy name communicates its actual optimization objective
  rather than an uncertain attribution.
- The algorithm may return a self-intersecting geometric surface; callers that
  require an embedded patch need a different operation and validation.
- Large polygons incur cubic runtime and quadratic memory; documentation must
  state this cost.
- `FaceTriangulation` validation, serialization, exports, tests, and
  documentation must accept the new leaf policy.
- Existing internal `triangulate_face` callers and tests migrate to
  `triangulate_polygon` without a compatibility alias under ADR 013.
- References must cite Barequet–Sharir and
  Barequet–Dickerson–Eppstein accurately.

## Affected packages

`compas` and integration documentation/tests in `compas_framework`.

## Dependencies

- [003 — Strategy objects](003-strategy-objects.md)
- [007 — Triangulation operations](007-triangulation-operations.md)
- [017 — Mixed-face triangulation](017-mixed-face-triangulation.md)
- [018 — Robust polygon triangulation](018-robust-polygon-triangulation.md),
  related but not required; this decision does not implement planar repair or
  an intersection-free spatial patch
