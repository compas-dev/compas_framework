# Title: How should Tessellation type retained zero-copy buffers?

## Status

Accepted

## Context

`Tessellation` intentionally retains NumPy and native buffers without copying,
but its generic bounds reject those buffers statically. Always normalizing to
lists or arrays would change ownership and allocation semantics.

## Options

1. Copy every buffer to Python lists.
2. Copy every buffer to canonical NumPy arrays.
3. Return broad unions and abandon concrete buffer-type preservation.
4. Expand generic buffer bounds to the supported Python, NumPy, and native
   retained-buffer contract.

## Recommendation

Choose option 4. Preserve the existing generic design and broaden its bounds to
supported nested sequences, NumPy arrays, and compatible native buffers.
Construction checks the minimal structural invariants required for a valid
retained object but does not coerce, copy, or take ownership. Preserve the
concrete buffer type in properties where Pyright can infer it. Apply the same
contract to optional normals, UVs, and polylines.

Construction checks only the minimal structural invariants required for a valid
retained `Tessellation`; it does not apply an elementwise nominal type allow-list.
Tests verify compatible duck-typed buffers, identity preservation, source
non-mutation, and absence of unnecessary conversion.

## Consequences

- CGAL and other native plugins no longer require ignores at this boundary.
- Ownership, mutability, lifetime, dtype, and shape must be explicitly
  documented and tested.
- Serialization still normalizes buffers to built-in data.
- Ordinary core containers do not inherit zero-copy semantics from this
  deliberate exception.

## Affected packages

`compas`, `compas_cgal`, and native consumers of `Tessellation`.

## Dependencies

- [002 — Numeric and array inputs](002-numeric-array-inputs.md)
- [003 — Array guarantees](003-array-guarantees.md)
