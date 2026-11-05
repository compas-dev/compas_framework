# Title: How should OCC subclasses and native uncertainty align with core APIs?

## Status

Accepted

## Context

OCC Curve, Surface, NURBS, and BRep subclasses currently narrow parameters,
return invariant backend lists, disagree on properties versus methods, and call
removed core APIs. PythonOCC downcasts and overload uncertainty are spread
through broad ignores.

## Options

1. Preserve backend-specialized annotations even when they violate base-class
   substitutability.
2. Loosen core and OCC types to `Any`.
3. Treat core signatures as authoritative and isolate native uncertainty in
   small typed boundary helpers.

## Recommendation

Choose option 3. Overrides accept the same or broader inputs and return
compatible core public types. `__eq__` accepts `object`. Preserve property/
method contracts. Annotate public invariant lists with the base item type rather
than changing core lists to `Sequence` solely for covariance. Keep stable
mutable native attributes typed to their native base class and centralize
downcasts/overload workarounds in narrow helpers with explained ignores.

## Consequences

- OCC loses some backend-specific precision in overridden public annotations,
  while runtime items remain backend instances.
- Real stale-API/runtime defects must be fixed rather than suppressed.
- Backend-specific access may use explicit native properties only when a real
  consumer requires them.
- Tests cover base-typed use of OCC instances and native conversion helpers.
- No module-wide ignores or global diagnostic suppression are allowed.

## Affected packages

`compas` and `compas_occ`.

## Dependencies

- [001 — Supported baseline](001-supported-baseline.md)
- [005 — Native normalization](005-native-normalization.md)
- [006 — Plugin conformance](006-plugin-conformance.md)
