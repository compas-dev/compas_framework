# Title: Which array guarantees should annotations express statically?

## Status

Accepted

## Context

NumPy typing expresses dtype better than shape. Current `Annotated` shape
metadata is descriptive but not enforced. Rank, contiguity, writability,
ownership, and value constraints are runtime properties.

## Options

1. Encode shapes through extensive generics and `Annotated` metadata.
2. Use unparameterized `NDArray[Any]` everywhere.
3. Express meaningful dtypes with simple aliases and document/runtime-validate
   all shape and layout constraints.

## Recommendation

Choose option 3. Define simple numeric, floating, integer, `float64`, and
`int32` array aliases. State expected ranks/shapes in docstrings and enforce
them at the boundary where the invariant is required for object validity,
mutation, or native safety. Treat contiguity, writability, ownership, finiteness,
and range as documented runtime guarantees. Do not claim `Annotated` shape
metadata is checker enforcement and do not add a shape-typing framework.

Ordinary Python algorithms validate only invariants needed before mutation or
retention, or needed for a clear and safe failure. Exact dtype, rank, and layout
checks belong at native ABI boundaries. Do not eagerly walk or convert inputs
solely to prove an annotation; inspect required capabilities and observable
properties instead of concrete types.

## Consequences

- Annotations remain readable and truthful.
- Invalid shapes may still pass static checking and must fail clearly at
  runtime.
- Native adapter tests must cover dtype, rank, shape, layout, and ownership.
- Documentation must distinguish static from runtime guarantees.

## Affected packages

`compas`, `compas_cgal`, and NumPy-facing `compas_occ` adapters.

## Dependencies

- [001 — Supported baseline](001-supported-baseline.md)
- [002 — Numeric and array inputs](002-numeric-array-inputs.md)
