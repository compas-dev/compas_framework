# Title: What polygonization and tessellation operations should continuous geometry expose?

## Status

Accepted

## Context

Current naming includes cached `.tessellation`, fresh
`compute_tessellation()`, OCC `to_tessellation()`, legacy misspelled
`to_tesselation()`, `to_viewmesh()`, and several mesh conversions. Surface and
shape override names also differ (`nu`/`nv` versus `u`/`v`). The objective asks
to distinguish operations from representation conversions.

The existing `Tessellation` return type and its zero-copy semantics are tested
in `../compas/tests/compas/geometry/test_tessellation.py`.

## Options

1. Use direct `tessellate(strategy) -> Tessellation` for canonical triangles
   and the separate `polygonize(strategy) -> PolygonalSurface` operation from
   ADR 005 for topology-preserving polygonal output. Require callers to use the
   semantically correct operation rather than a topology flag or universal
   conversion alias.
2. Standardize only on `to_triangle_mesh()`. This unifies conversion but hides
   the fact that continuous geometry is approximated by an operation.
3. Keep cached `.tessellation`, fresh `compute_tessellation()`, and
   `to_triangle_mesh()` together. This preserves existing distinctions but
   exposes three overlapping ways to obtain the same triangle result.
4. Keep all existing names, including OCC aliases and the misspelling. This
   avoids breakage but leaves no coherent contract.

## Recommendation

Choose option 1. Continuous geometry exposes exactly
`tessellate(strategy) -> Tessellation`. It performs a fresh operation; there is
no public cached `.tessellation` property and no parallel
`compute_tessellation()`, `to_tessellation()`, `to_tesselation()`, or
`to_viewmesh()` or `to_triangle_mesh()` spelling. Discrete polygonal geometry
uses `triangulated(strategy)` from ADR 007. Topology-preserving polygonal
output uses the accepted `polygonize(strategy) -> PolygonalSurface` operation
from ADR 005, with no topology flag or scalar/cached alternative.

The operation-oriented `polygonize`/`tessellate` pair avoids the mixed
`to_polygonal_surface`/`to_tessellation` conversion naming. `to_mesh()` remains
an explicit conversion of an existing discrete representation.

`tessellate` is the direct canonical triangle operation and need not be
implemented as `polygonize(...).triangulated(...)`. For the same tessellation
strategy, direct and two-step paths must be geometrically consistent, but
connectivity may differ. Backends must document their seam and boundary
behavior for each path.

Callers who care about the face-triangulation policy use the explicit two-step
workflow:

```python
geometry.polygonize(strategy).triangulated(triangulation_strategy)
```

## Consequences

- Continuous producers share two non-overlapping operations with stable result
  types: persistent polygonal discretization and ephemeral triangle
  tessellation.
- Removing public cached tessellations eliminates cache identity and invalidation
  from the API contract; implementations may cache privately if results remain
  observationally correct.
- The required strategy makes approximation policy explicit; tessellation must
  not mutate the source geometry.
- Direct and two-step results may differ in connectivity without violating the
  contract, so tests compare geometric consistency and documented boundary/
  seam behavior rather than exact triangle indices.
- Existing surface, shape, and OCC method/property names break and are removed,
  including the BRep misspelling and aliases.
- Tests and examples must cover both `tessellate(strategy)` and the explicit
  polygonize-then-triangulate workflow and must no longer assert public
  cached-result identity.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, and
`compas_framework`.

## Dependencies

- [002 — Mesh representations](002-mesh-representations.md)
- [003 — Strategy objects](003-strategy-objects.md)
- [005 — Output topology](005-output-topology.md)
