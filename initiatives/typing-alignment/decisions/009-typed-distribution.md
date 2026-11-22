# Title: How should COMPAS packages distribute typing and native stubs?

## Status

Accepted

## Context

Only CGAL contains `py.typed` and native `.pyi` files. Source checks do not
prove wheel contents. CGAL stubs are hand-maintained without export parity;
OCC relies on upstream PythonOCC typing and broad local ignores.

## Options

1. Keep typing development-only and do not advertise PEP 561 support.
2. Generate all stubs automatically immediately.
3. Ship `py.typed` from all packages, retain maintained CGAL stubs initially,
   and verify source/runtime/wheel parity.

## Recommendation

Choose option 3. Add `py.typed` and wheel-content tests to core and OCC; retain
CGAL's marker. Every compiled CGAL module has a maintained stub, exported-name
parity test, and typed smoke calls. Defer generation until it demonstrably
improves these contracts. OCC uses inline typing and upstream PythonOCC stubs,
with narrow local helpers for proven upstream defects rather than duplicated
native stubs.

## Consequences

- Downstream checkers consume COMPAS annotations by default.
- Incorrect annotations become user-visible and therefore release-relevant.
- Wheel builds must include markers and stubs on all platforms.
- Export parity catches missing/stale names but not semantic dtype or ownership;
  focused tests remain necessary.
- Documentation states the supported checker/baseline.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, and release checks in
`compas_framework`.

## Dependencies

- [001 — Supported baseline](001-supported-baseline.md)
- [005 — Native normalization](005-native-normalization.md)
- [006 — Plugin conformance](006-plugin-conformance.md)
- [007 — Backend substitutability](007-backend-substitutability.md)
- [008 — Return normalization](008-return-normalization.md)
