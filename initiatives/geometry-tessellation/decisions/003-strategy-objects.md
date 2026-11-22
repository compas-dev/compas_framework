# Title: How should tessellation policies be represented and serialized?

## Status

Accepted

## Context

Current controls are unrelated scalar parameters: U/V counts on surfaces and
shapes, OCC linear/angular deflection, CGAL edge-length and partial quality
controls, and Gmsh sizing options. No common strategy object exists. The
objective asks for lightweight serializable configuration compatible with
COMPAS `Data`, while backend algorithms must remain owned by their producers.

Existing count APIs are in
`../compas/src/compas/geometry/surfaces/surface.py` and
`../compas/src/compas/geometry/shapes/shape.py`; OCC deflection is in
`../compas_occ/src/compas_occ/brep/brep.py`.

## Options

1. Keep scalar keywords on every producer. This minimizes new types but keeps
   inconsistent names, weak cache keys, and broad signatures.
2. Introduce executable strategy objects with `apply(geometry)`. This enables
   injection but creates double dispatch and unclear algorithm ownership.
3. Introduce immutable, serializable policy configurations implemented by each
   producer through one common `TessellationStrategy` base.
4. Create one broad strategy containing every possible control. This appears
   uniform but encourages ignored fields and false equivalence.

## Recommendation

Choose option 3. Every strategy inherits the common
`TessellationStrategy(compas.data.Data)` base, remains algorithm-free,
validates its values, and is serializable through the normal COMPAS data
contract. The accepted public configurations are:

```python
class TessellationStrategy(Data):
    pass


class Native(TessellationStrategy):
    pass


class UGrid(TessellationStrategy):
    u: int


class UVGrid(TessellationStrategy):
    u: int
    v: int


class Deflection(TessellationStrategy):
    linear: float
    angular: float


class Adaptive(TessellationStrategy):
    max_deviation: float | None = None
    max_angle: float | None = None
    max_edge_length: float | None = None
```

- `Native` has no fields and requests fixed natural topology.
- `UGrid.u` is a positive integer and controls one-parameter shapes.
- `UVGrid.u` and `UVGrid.v` are positive integers. Domain restrictions are not
  part of `UVGrid`; it controls two-parameter surfaces and shapes.
- `Deflection.linear` is expressed in model units. `Deflection.angular` is
  public degrees. Both are positive and finite; `angular` is at most 180
  degrees. Backends convert degrees to radians where required.
- `Adaptive` requires at least one non-`None` field. Every provided value is
  positive and finite. `max_angle` is public degrees. There is no public
  maximum-depth or recursion-control field.
- A producer raises an error for any requested strategy parameter it does not
  support; unsupported fields are never ignored.

Initial type/strategy support is explicit:

- `Box` supports `Native`.
- `Cylinder` and `Cone` support `UGrid`.
- `Capsule`, `Sphere`, `Torus`, and general parametric surfaces support
  `UVGrid`.

Invalid type/strategy combinations raise an error. A producer never ignores an
extra sampling dimension to make an invalid strategy appear to work.

The strategy is a required tessellation argument. Producers do not hide
approximation policy behind stored or backend-specific defaults.

## Consequences

- Strategies can be serialized, compared, cached, and documented consistently.
- Each backend must publish supported strategy types and fields through the
  capability contract in ADR 004.
- Public tessellation APIs accept the strategy object only; legacy scalar
  controls are removed instead of normalized through parallel call forms.
- Backend implementation code may unpack strategy values internally, but those
  scalars are not a second public API.
- Unit tests must cover serialization, validation, equality, cache identity,
  public degree units, backend radian conversion, absence of domain/depth
  controls, fixed/one-/two-parameter support, and errors for unsupported
  dimensions or strategy combinations.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, optionally `compas_gmsh`, and
`compas_framework`.

## Dependencies

- [001 — Terminology](001-terminology.md)
