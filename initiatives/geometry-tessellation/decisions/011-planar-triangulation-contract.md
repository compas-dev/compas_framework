# Title: What canonical contract should planar constrained triangulation use?

## Status

Accepted

The operation names recorded below were subsequently made explicit by
[ADR 020](020-planar-delaunay-naming.md): `triangulate_planar_points` and
`triangulate_planar_domain`. The contract and strategy names are unchanged.

## Context

Core constrained Delaunay uses `boundary, polylines, polygons`; conforming adds
`angle, area`. CGAL uses `boundary, points, holes, curves` and does not accept
the core quality arguments. Positional dispatch can silently reinterpret data,
while keyword calls can fail plugin signature validation. Plain Delaunay also
returns only faces whereas constrained variants return `(V, F)`.

Sources:
`../compas/src/compas/geometry/triangulation_delaunay.py` and
`../compas_cgal/src/compas_cgal/triangulation.py`.

## Options

1. Make CGAL mimic the current core names exactly. This repairs dispatch but
   retains ambiguous `polylines`/`polygons` meanings and incomplete interior
   point vocabulary.
2. Make core mimic current CGAL signatures. This exposes actual CGAL concepts
   but omits a structured quality contract and breaks core keywords.
3. Adopt canonical keyword-only concepts: `boundary`, `holes`, `constraints`,
   `points`, and `quality`; return `Tessellation` from every planar
   triangulation operation and remove the incompatible legacy contracts.
4. Leave direct and dispatched APIs intentionally different. This avoids
   migration but makes plugins unreliable through core.

## Recommendation

Choose option 3. Contracts must state projection/coordinate space, input-vertex
preservation, Steiner insertion, winding, hole/constraint behavior, and which
quality fields are supported. Arguments after `boundary` are keyword-only.
Plain, constrained, conforming, and refined planar triangulation all return
`Tessellation`, so vertices and triangle indices always travel together.

Planar triangulation is a separate serializable `Data` strategy family from the
face strategies in ADR 007:

```python
class Delaunay(Data):
    pass


class ConstrainedDelaunay(Data):
    pass


class ConformingDelaunay(Data):
    quality: TriangulationQuality | None = None


class TriangulationQuality(Data):
    min_angle: float | None = None
    max_area: float | None = None
    max_edge_length: float | None = None
```

`TriangulationQuality` requires at least one provided field. Every provided
value is positive and finite. `min_angle` is expressed in public degrees and
must be less than 60 degrees; `max_area` is in model-units squared; and
`max_edge_length` is in model units. A backend errors on unsupported fields;
it never ignores them. Quality values are triangulation targets and are
distinct from `Adaptive` tessellation controls and from estimated or guaranteed
error contracts in ADR 004.

The canonical functions are:

```python
def triangulate_points(
    points,
    *,
    strategy: Delaunay,
    frame: Frame | None = None,
) -> Tessellation: ...


def triangulate_domain(
    boundary,
    *,
    holes=(),
    constraints=(),
    points=(),
    strategy: ConstrainedDelaunay | ConformingDelaunay,
    frame: Frame | None = None,
) -> Tessellation: ...
```

With `frame=None`, every input coordinate must lie in world XY within the
standard COMPAS tolerance. With an explicit `Frame`, every input coordinate
must lie on that frame's plane within the standard COMPAS tolerance. Inputs
outside the applicable tolerance are rejected. Projection to local XY is an
internal algorithm step only; implementations never silently discard Z.

Coordinates of existing input vertices are preserved exactly in the returned
`Tessellation`. Generated Steiner vertices are lifted onto the specified plane
(world XY when `frame=None`, otherwise the explicit frame plane). All
parameters after `points` or `boundary` are keyword-only.

`Delaunay` preserves the supplied point set. `ConstrainedDelaunay` preserves
input vertices subject to documented vertex insertion where constraints
intersect. `ConformingDelaunay` may insert Steiner vertices to pursue its
quality targets.

## Consequences

- Core and plugin signatures can be validated and safely dispatched.
- Existing keywords, positional calls, face-only arrays, and `(V, F)` returns
  break; no alias or dual return mode is retained.
- Unsupported quality fields must fail rather than be mapped to non-equivalent
  controls.
- Stable results always carry vertices with triangles.
- Tests must cover standard-tolerance acceptance/rejection for world XY and an
  explicit frame, exact preservation of input coordinates, lifting of generated
  Steiner vertices, permitted insertion, intersecting constraints, units and
  validation of every quality field, and rejection of unsupported fields.
- Tests must exercise installed-plugin dispatch, not only direct imports.

## Affected packages

`compas`, `compas_cgal`, and `compas_framework`.

## Dependencies

- [001 — Terminology](001-terminology.md)
- [003 — Strategy objects](003-strategy-objects.md)
- [004 — Error contracts](004-error-contracts.md)
- [007 — Triangulation operations](007-triangulation-operations.md)
- [008 — Triangle interoperability](008-triangle-interoperability.md)
