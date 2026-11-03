# Title: What discretization state should continuous geometry retain?

## Status

Accepted

## Context

`Shape` and `Surface` currently retain `resolution_u` and `resolution_v` and
cache derived vertices, edges, faces, points, lines, and polygons. Those values
are not part of the serialized analytic definition, are inconsistently used by
one- and two-parameter geometry, and create invalidation and placement-cache
contracts that are unrelated to the defining geometry.

ADRs 003, 005, and 006 require explicit strategy objects and fresh
`polygonize(strategy)` and `tessellate(strategy)` operations. ADR 013 permits a
clean breaking API. The user explicitly approved removing the stored
resolution and caches until the discretization API is complete and consistent.

## Options

1. Keep stored resolutions and private derived-geometry caches, while requiring
   explicit strategies only in the new operations. This retains two competing
   sources of approximation policy and preserves invalidation complexity.
2. Remove stored resolutions and all derived discretization caches. Retain only
   defining analytic state and materialize results through explicit operations.
3. Remove public resolution properties but retain undocumented caches keyed by
   strategies and placement state. This reduces the public surface but commits
   the initial implementation to cache correctness before its inputs are stable.

## Recommendation

Choose option 2.

Continuous geometry stores only defining state: analytic parameters and frames,
or the control net, weights, knots, degrees, and periodicity of NURBS geometry.
Remove stored `resolution_u` and `resolution_v` and all cached derived
discretizations. Do not introduce private discretization caches initially.

The public materialization operations are exclusively:

```python
geometry.polygonize(strategy)  # -> PolygonalSurface
geometry.tessellate(strategy)  # -> Tessellation
```

Remove `Shape.to_vertices_and_faces()` and `Mesh.from_shape()`. The explicit
half-edge conversion is `shape.polygonize(strategy).to_mesh()`. Treat generic
shape and surface `compute_vertices`, `compute_edges`, `compute_faces`, and
surface `to_vertices_and_faces` as implementation machinery rather than a
parallel public discretization API. A future public point-grid sampling API, if
needed by a concrete consumer, requires a separate design.

Preserve exact, shape-specific finite access such as `Box.points`. Exact box
corners are defining geometric information, not an approximate sampled
representation, and do not establish a generic `Shape.points` contract.

## Consequences

- Approximation policy is supplied once, explicitly, at each operation.
- Every polygonization and tessellation result is newly materialized and
  independent of its source.
- Cache identity, invalidation, placement fingerprints, and resolution
  synchronization disappear from the API and tests.
- Strategy equality remains useful for value semantics and possible future
  caches, but no cache behavior is promised.
- Existing callers and examples using stored resolutions,
  `to_vertices_and_faces()`, or `Mesh.from_shape()` must migrate to explicit
  operations.
- Any later cache requires a new architectural decision after all effective
  inputs and invalidation rules are known.

## Affected packages

`compas`, `compas_occ`, `compas_model`, and `compas_framework`; examples and
tests in `compas_cgal` that materialize shapes are also affected.

## Dependencies

- [003 — Strategy objects](003-strategy-objects.md)
- [005 — Output topology](005-output-topology.md)
- [006 — Tessellation API](006-tessellation-api.md)
- [013 — Compatibility](013-compatibility.md)
