# Title: How should typing correctness be verified and existing errors removed?

## Status

Accepted

## Context

Source-only green checks miss consumer and wheel failures. OCC has a material
error baseline. NumPy dtype/layout and native ABI behavior need runtime tests,
while current ignores mix justified third-party gaps with contract debt.

## Options

1. Require only each package's source Pyright check.
2. Suppress existing errors through exclusions or a frozen baseline.
3. Combine source, consumer, runtime, native, and installed-wheel checks and
   ratchet errors to zero through scoped work packages.

## Recommendation

Choose option 3. Verify:

- source and typed consumer fixtures;
- accepted and expected-error Python/NumPy calls;
- scalar/dtype/layout/ownership runtime matrices;
- native imports and wrapper-to-ABI normalization;
- CGAL stub export parity;
- installed-wheel `py.typed`, stubs, and external consumers;
- custom duck-typed scalar, sequence, and buffer fixtures that are not tied to
  the listed concrete classes;
- instrumented fixtures proving that ordinary Python paths avoid unnecessary
  copies and conversions and that required native normalization occurs once;
- Ruff, formatting, relevant/full feasible tests, Pyright, and documentation.

Reduce OCC errors to zero by owned module family. Do not introduce global
suppression or baseline files. Every remaining ignore is narrow, explained,
and located at a demonstrated third-party/native boundary.

## Consequences

- CI becomes broader and slower but verifies the distributed contract.
- Environmental/native limitations must be reported explicitly rather than
  counted as passes.
- Error reduction is measurable per work package.
- Tests and documentation change with every contract correction.
- Verification tests observable behavior and capabilities rather than
  reinforcing nominal runtime allow-lists.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, and `compas_framework`.

## Dependencies

- [001 — Supported baseline](001-supported-baseline.md)
- [002 — Numeric and array inputs](002-numeric-array-inputs.md)
- [003 — Array guarantees](003-array-guarantees.md)
- [004 — Tessellation buffers](004-tessellation-buffers.md)
- [005 — Native normalization](005-native-normalization.md)
- [006 — Plugin conformance](006-plugin-conformance.md)
- [007 — Backend substitutability](007-backend-substitutability.md)
- [008 — Return normalization](008-return-normalization.md)
- [009 — Typed distribution](009-typed-distribution.md)
