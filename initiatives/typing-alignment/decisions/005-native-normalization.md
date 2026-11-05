# Title: Where should broad public inputs become exact native buffers?

## Status

Accepted

## Context

CGAL needs exact dtype/layout buffers. PythonOCC accepts values inconsistently
by dtype because SWIG conversion is accidental. Public annotations currently
conflate coercible inputs with exact native ABI requirements.

## Options

1. Require exact native arrays in every public API.
2. Pass broad inputs directly to native libraries and rely on their coercion.
3. Accept approved broad inputs in public wrappers and normalize them in a
   private backend adapter before native calls.

## Recommendation

Choose option 3. CGAL adapters normalize coordinates to C-contiguous `float64`
and indices to C-contiguous `int32`. OCC adapters validate shape and convert
each value to Python `float`/`int` before SWIG calls. OCC returns core objects
and Python containers unless a separately approved API requires NumPy output.

Do not broaden an OCC annotation until its adapter implements and tests the
promised normalization.

Normalization is a single private last-mile native-boundary operation, not a
general public-wrapper policy. Reuse an input that already satisfies the exact
ABI contract when backend ownership and lifetime permit. Otherwise perform only
the required conversion. OCC scalar conversion occurs immediately before SWIG
only where PythonOCC demonstrably requires built-ins; repeated normalization is
not allowed.

## Consequences

- Native ABI requirements become explicit and localized.
- Public callers need not pre-normalize valid inputs.
- Conversion may allocate; documentation must state when this occurs.
- Tests cover dtype, shape, contiguity, non-contiguous input, source mutation,
  and errors.
- Native helper modules own the few justified third-party casts/ignores.
- Tests instrument conversion and copy counts to detect redundant work.

## Affected packages

`compas_occ`, `compas_cgal`, and core plugin boundaries in `compas`.

## Dependencies

- [002 — Numeric and array inputs](002-numeric-array-inputs.md)
- [003 — Array guarantees](003-array-guarantees.md)
- [004 — Tessellation buffers](004-tessellation-buffers.md)
