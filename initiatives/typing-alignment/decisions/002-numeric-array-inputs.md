# Title: Which Python and NumPy scalar and array values should public APIs accept?

## Status

Accepted

## Context

Core sequence aliases reject NumPy arrays statically even where runtime calls
succeed. Numeric scalar acceptance varies between built-in checks and
`Real`/`Integral`. `ArrayLike` would be broader than many geometry APIs.

## Options

1. Keep sequence-only annotations and document NumPy as unsupported.
2. Use `ArrayLike` for every numerical input.
3. Define a small explicit core vocabulary for supported Python/NumPy real and
   integral scalars, coordinates, coordinate collections, and index arrays.
4. Introduce a generic tensor abstraction with shape parameters.

## Recommendation

Choose option 3. Core aliases explicitly include supported NumPy scalar and
array types alongside Python/COMPAS inputs. Use `ArrayLike` only in APIs whose
real behavior is broad `np.asarray` coercion. Consolidate duplicated
datastructure coordinate aliases into the core vocabulary.

Where bool exclusion, dimension, shape, finiteness, or range is a stated
invariant, runtime behavior remains authoritative. Enforce it at the narrow
boundary that needs it; do not pre-screen all inputs nominally or traverse them
solely for typing. Do not widen annotations beyond tested runtime support.

These aliases identify verified common Python and NumPy families; they are not
runtime nominal allow-lists. Do not reject an otherwise usable value merely
because its concrete class is absent from a union. Prefer documented operations
such as iteration, indexing, unpacking, and numeric arithmetic. Retain targeted
semantic checks, such as bool rejection, only where the public contract requires
them.

When an intentionally supported, stable capability extends beyond the listed
concrete families, express it with a small structural Protocol backed by real
consumers and static/runtime fixtures. Do not use concrete unions to falsely
reject that supported capability, and do not add speculative Protocols.

## Consequences

- Existing supported NumPy calls type-check.
- Public signatures import a small NumPy typing vocabulary; NumPy is already a
  core dependency.
- Static consumer and runtime matrix tests are required for every alias.
- Widening annotations alone must not create new runtime behavior.
- Documentation must list accepted Python and NumPy forms.
- Tests include representative custom duck-typed scalar and sequence objects.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`.

## Dependencies

- [001 — Supported baseline](001-supported-baseline.md)
