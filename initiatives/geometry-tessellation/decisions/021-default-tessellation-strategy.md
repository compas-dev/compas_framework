# Title: Should shape and surface tessellation provide deterministic default strategies?

## Status

Accepted

## Context

ADRs 003, 006, and 014 require callers to supply every tessellation strategy
explicitly. This keeps approximation policy visible, but makes common ephemeral
tessellation unnecessarily verbose when a geometry type has one natural
strategy family.

The strategy arity is fixed by geometry type: Box uses `Native`; Cylinder and
Cone use `UGrid`; Sphere, Torus, Capsule, and all current Surface types use
`UVGrid`. Grid dimensions count cells, not sample points. A value of 64 is valid
for every listed type, including Capsule's even-v requirement.

BRep and BRepFace tessellation use `Deflection`. Existing OCC defaults are
inconsistent and historically express angular values in radians, while public
`Deflection.angular` values are degrees. There is no approved,
backend-independent default for that policy.

## Options

1. Keep every tessellation strategy mandatory.
2. Permit `None` everywhere and let backends choose, making results opaque and
   backend-dependent.
3. Permit `None` only for Shape and Surface, with fixed core defaults. Keep
   persistent polygonization and deflection-based BRep tessellation explicit.

## Recommendation

Choose option 3:

```python
shape.tessellate(strategy=None)
surface.tessellate(strategy=None)
```

Resolve `None` at operation entry to:

| Geometry | Default |
|---|---|
| `Box` | `Native()` |
| `Cylinder`, `Cone` | `UGrid(64)` |
| `Sphere`, `Torus`, `Capsule` | `UVGrid(64, 64)` |
| every `Surface` | `UVGrid(64, 64)` |

An omitted argument and explicit `None` are equivalent. Explicit strategies
remain unchanged and validated. Defaults are operation policy, not stored
geometry state. Do not cache results; every call returns a fresh independent
`Tessellation` and leaves the source unchanged.

Keep `polygonize(strategy)`, `Brep.tessellate(Deflection(...))`, and
`BrepFace.tessellate(Deflection(...))` explicit. A BRep default requires a
separate decision with fixed linear and degree-based angular values.

## Consequences

- Common ephemeral Shape and Surface tessellation becomes concise and
  deterministic.
- UV defaults generally produce about 4,000 vertices and 8,000 triangles;
  NURBS evaluation may be materially more expensive.
- `tessellate()` and `polygonize(strategy)` are intentionally asymmetric:
  convenience applies only to the ephemeral result.
- Tests must compare omitted and explicit `None` with explicit defaults,
  verify fresh non-mutating results and explicit overrides, and confirm BRep
  and polygonization strategies remain mandatory.
- This supersedes the mandatory-strategy rule of ADRs 003, 006, and 014 only
  for Shape and Surface `tessellate`.

## Affected packages

`compas` and integration documentation/tests in `compas_framework`.

## Dependencies

- [003 — Strategy objects](003-strategy-objects.md)
- [006 — Tessellation API](006-tessellation-api.md)
- [014 — Continuous geometry materialization](014-continuous-geometry-materialization.md)
