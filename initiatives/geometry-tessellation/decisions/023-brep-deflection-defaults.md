# Title: Should BRep tessellation conversion require explicit deflection controls?

## Status

Proposed.

## Context

Accepted ADR 021 deliberately kept BRep and BRepFace deflection controls
mandatory because no backend-independent default had been approved. Proposed
Typing ADR 015 subsequently used `None` to resolve deterministic defaults from
the core tolerance object. The user-authored terminology now makes BRep
tessellation the sole precision-controlled tessellation operation, which makes
the default policy more consequential rather than resolving it implicitly.

The choice is independent of the accepted representation-oriented public
naming. `Brep.to_tessellation` performs the underlying tessellation operation.

## Options

1. **Require both controls.** Every call states its approximation request.
   This is maximally explicit but makes generic scene conversion verbose and
   forces every caller to select values without necessarily understanding the
   model scale.
2. **Use deterministic core defaults when either keyword is omitted.** Resolve
   `linear_deflection=None` from `TOL.lineardeflection` and
   `angular_deflection=None` from the degree equivalent of
   `TOL.angulardeflection` before plugin dispatch. This supports no-argument
   visualization while keeping explicit overrides visible and backend
   independent.
3. **Let each backend choose defaults.** This is convenient but makes the same
   public call backend dependent and obscures units.

## Recommendation

Choose option 2:

```python
brep.to_tessellation(
    *,
    linear_deflection: float | None = None,
    angular_deflection: float | None = None,
) -> Tessellation
```

`BrepFace` exposes the same signature and delegates through `as_brep`. Core
resolves every `None` before dispatch to `brep_to_tessellation`. That plugin
hook receives concrete positive finite values and never chooses defaults.

The defaults are operation policy, not a guarantee that either requested
deflection is an achieved error bound. Documentation must describe the backend
contract accurately. `TOL.temporary(...)` affects subsequent calls
deterministically and is covered by tests.

## Consequences

- Generic scene conversion can use `brep.to_tessellation()` without importing a
  backend policy object.
- Explicit values and defaults use one public unit contract.
- Results may change inside an explicit `TOL.temporary(...)` context; there is
  no caching contract.
- Backends cannot silently select different defaults.
- The defaults are conventional ambient policy, not values derived from BRep
  dimensions or model scale. Applications working at materially different
  scales pass explicit values or configure `TOL` deliberately.
- Users requiring reproducible values independent of ambient tolerance state
  pass both keywords explicitly.

## Verification

- Compare omitted keywords with the corresponding explicit core tolerance
  values.
- Cover one omitted and one explicit keyword independently.
- Verify `TOL.temporary(...)` resolution, fresh results, and source
  non-mutation.
- Assert `brep_to_tessellation` rejects `None` and receives concrete
  public-unit values.
- Verify OCC converts the angular value to radians exactly once.

## Affected packages

`compas`, `compas_occ`, and integration tests/documentation in
`compas_framework`.

## Dependencies

- [022 — Operation terminology and producer boundaries](022-operation-terminology-and-producer-boundaries.md)

## Approval boundary

This decision is **Proposed**. Typing ADR 015 may describe the optional public
signature, but implementation remains blocked until this default policy is
explicitly approved.
