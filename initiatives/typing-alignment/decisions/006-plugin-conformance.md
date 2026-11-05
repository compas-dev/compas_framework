# Title: How should backend plugin signatures conform to core contracts?

## Status

Accepted

## Context

The plugin decorator preserves local callable typing, but registered methods
are stored broadly and backend packages repeat signatures manually. OCC plugin
modules frequently use untyped `*args, **kwargs`. Cross-package parity is not
statically verified.

## Options

1. Continue relying on runtime registration and duplicated annotations.
2. Define a separate Protocol for every plugin operation.
3. Let core own documented public invariants and narrow private pluggables,
   require explicit matching backend signatures, and verify conformance in
   integration.

## Recommendation

Choose option 3. Core enforces only documented public invariants before dispatch
when early validation is necessary; it does not nominally gate otherwise usable
duck-typed inputs. Private pluggables expose the narrow backend contract. Backend
implementations use explicit parameter and return annotations. Add runtime
signature comparison for names, kinds, and defaults plus typed integration
fixtures for argument and result compatibility.

Do not duplicate the same validation in both the public wrapper and backend.

Do not add per-operation Protocol classes unless a concrete non-plugin consumer
requires one.

## Consequences

- Plugin differences fail in focused tests rather than downstream use.
- Some public wrappers/private selectors need separation.
- OCC generic forwarding functions must become explicit.
- Runtime signature checks cannot prove semantic return compatibility, so typed
  consumer fixtures remain required.
- Plugin documentation identifies public versus backend contracts.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, and `compas_framework`.

## Dependencies

- [002 — Numeric and array inputs](002-numeric-array-inputs.md)
- [005 — Native normalization](005-native-normalization.md)
