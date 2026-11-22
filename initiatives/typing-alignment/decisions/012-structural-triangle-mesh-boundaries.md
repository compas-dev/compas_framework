# Title: What should triangle-mesh algorithms accept at numerical boundaries?

## Status

Accepted

## Context

`Tessellation` is useful as a retained discrete representation produced by
parametric geometry and handed to visualization or transfer systems. It is now
also a nominal gate for more than eighteen numerical mesh operations. Native
CGAL requires only coordinate and index arrays, and `compas_cgal` already has a
split API in which closely related functions accept raw buffers. Requiring a
core geometry object therefore adds coupling that the algorithm and native ABI
do not need.

## Options

1. Keep `Tessellation` as the mandatory algorithm input and result.
2. Permanently accept both `Tessellation` and raw buffers at every operation.
3. Use one structural triangle-buffer contract for numerical algorithms and
   retain `Tessellation` only as an explicit representation.

## Recommendation

Choose option 3. Define a single structural input contract equivalent to
`tuple[CoordinatesInput, IndicesCollectionInput]`. Core wrappers dispatch that
contract without converting to NumPy or recomputing mesh topology. Private
plugin hooks use the same structural contract. Native backends normalize once
at their ABI boundary and may return concrete NumPy-backed tuples.

After conversion, a backend enforces only the minimal array-level preconditions
needed for memory-safe native execution, such as matrix column counts and index
bounds when the native helper performs unchecked access. Operation-specific
geometric validity—closedness, manifoldness, orientation, degeneracy, or
self-intersection—is an algorithm precondition, not a Python pre-validation
pass. Native success/failure must be propagated, and returned buffer shapes
must be checked at the backend boundary.

Keep `Tessellation` as a retained triangular representation with explicit
conversion to and from vertex/triangle buffers. Do not implicitly convert
`Mesh`, `PolygonalSurface`, or `Tessellation` inside numerical algorithms. A
triangle-only operation validates face arity; quad or polygonal inputs must be
triangulated explicitly.

Replace the nominal `tessellation_pluggable` gate with ordinary public
wrapper/private-hook pairs. `compas_cgal` raw functions remain directly usable
without constructing core geometry objects.

## Decision

Approved on 2026-11-04. The retained representation role of `Tessellation` is
preserved, while numerical algorithms and plugin contracts move to one
structural vertex/triangle-buffer path. Permanent object/raw overloads and
implicit representation conversion are not part of the approved design.
The Boolean pilot subsequently established that core-side topology validation
was unnecessary complexity: normalization and minimal process-safety checks
belong at the backend boundary, while native operation failures remain
authoritative.

## Consequences

- Lists, tuples, and suitable NumPy buffers are first-class inputs.
- Existing `Tessellation` callers must explicitly export their buffers.
- Algorithm results are shape-checked structural buffers; callers construct a representation
  only when they need one.
- There is one public numerical path rather than permanent object/raw overloads.
- ADR 004 remains valid for retained `Tessellation` buffers, but it no longer
  implies that algorithms should consume or return `Tessellation`.
- ADRs 005–006 become simpler: core owns semantic validation, and backends own
  native dtype/layout normalization.

## Affected packages

`compas`, `compas_cgal`, `compas_occ` where it implements the same plugin
contracts, and cross-package consumer tests in `compas_framework`.

## Verification

- Python list/tuple and NumPy float32/64 plus int32/64 inputs.
- C/Fortran, sliced, and read-only buffers and source non-mutation.
- Backend conversion, safe matrix shapes and index ranges, native failure
  propagation, and output shapes.
- Plugin signature parity and direct backend use without core objects.
- Explicit conversion to `Tessellation`, `PolygonalSurface`, and `Mesh`.

## Dependencies

- [002 — Numeric and array inputs](002-numeric-array-inputs.md)
- [003 — Array guarantees](003-array-guarantees.md)
- [004 — Tessellation buffers](004-tessellation-buffers.md)
- [005 — Native normalization](005-native-normalization.md)
- [006 — Plugin conformance](006-plugin-conformance.md)
