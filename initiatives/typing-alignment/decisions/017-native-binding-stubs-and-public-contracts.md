# Title: How should native bindings and public wrappers publish coordinated typing?

## Status

Proposed.

## Context

The two nanobind packages currently take materially different approaches:

- `compas_cgal` ships `py.typed` and one maintained `.pyi` for each of its 14
  extension modules. Symbol coverage is complete, but
  `pyright --verifytypes compas_cgal --ignoreexternal` reports 83% public type
  completeness and runtime inspection found inaccurate parameter and result
  declarations.
- `compas_libigl` ships `py.typed` but committed source suppresses imports of
  all 13 extension modules with unqualified `# type: ignore`. Only 8 of 21
  public wrappers are fully annotated, and verify-types completeness is 51.6%.

Both packages normalize broad public values to exact native arrays, but they
do not share a complete public vocabulary or a common rule for native stubs.
Green source Pyright and wheel-marker checks therefore do not prove that a
native call has the right arguments, that its result is known, or that a
backend result is accepted by core.

## Options

1. **Permit each package to choose stubs or ignores.** This minimizes migration
   but makes `py.typed` mean different things and allows `Unknown` to escape.
2. **Annotate only public Python wrappers.** This can hide the compiled seam
   behind casts but cannot verify native names, signatures, or results.
3. **Require accurate private native stubs plus coordinated public wrappers.**
   Stubs describe exact ABI values; wrappers use core structural types,
   normalize once, and return the actual public representation.
4. **Generate all stubs automatically and treat them as authoritative.** This
   is repeatable, but generated declarations still need semantic dtype,
   ownership, sparse-result, and wrapper-contract review.

## Recommendation

Choose option 3. Generation may bootstrap a stub, but reviewed source and
runtime evidence remain authoritative.

### Native extension contract

Every private compiled module has a packaged `.pyi` that describes its actual
Python ABI:

- parameters are the exact post-normalization NumPy arrays, scalar types, or
  STL-like values accepted by the binding;
- results use exact NumPy dtypes, SciPy sparse classes, Python containers, or
  heterogeneous tuples observed from the binding;
- rank, column count, contiguity, ownership, and value restrictions that
  static typing cannot express are documented and verified at runtime;
- nanobind vector wrappers are modeled structurally by their real methods and
  iteration behavior, not falsely as `list` subclasses;
- no unqualified import ignore suppresses a missing compiled module or stale
  symbol;
- a narrow ignore is permitted only for a demonstrated checker/upstream-stub
  defect, with its reason and a regression fixture at that exact boundary.

The `.pyi` contract is intentionally narrower than the public wrapper. It must
not claim that a compiled function accepts general COMPAS coordinate protocols
when the wrapper performs the conversion first.

### Public wrapper and plugin contract

Public direct wrappers:

1. accept core-owned aliases from the public `compas.typing` module in ADR
   016;
2. normalize once in a private package adapter to the native ABI;
3. perform only native-safety and operation-specific result-shape checks;
4. return the documented representation with an exact annotation; and
5. expose a complete public signature without `Any`, `Unknown`, casts, or
   ignores masking the binding result.

Plugin registration wrappers match the core hook exactly in names, kinds,
defaults, input structure, and semantic result. A backend implementation may
return a statically narrower concrete subtype, such as `VerticesFacesNumpy`,
when the core hook permits `VerticesFaces`. Exact ABI/result tuple aliases such
as `VerticesFacesNumpy` remain package-local implementation vocabulary built
from core primitive array aliases; they are not redefined public input types.
Discovery modules remain
lightweight and import native implementation code only inside wrapper bodies.

Do not convert a correct native array or sparse result to a list merely for
typing. Normalize a result only when the approved public/plugin contract
requires a different representation. Conversely, do not annotate a concrete
result with a broad input union to avoid learning its actual type.

### CGAL corrections

The CGAL slice must:

- replace package-local `Vertices`, `Faces`, and `VerticesFaces` with imports
  from `compas.typing`, while retaining only package-specific concrete and
  heterogeneous result aliases;
- correct straight-skeleton list-versus-array results, meshing fixed-vertex
  input, native vector-wrapper models, Boolean literals, and native vector
  return declarations identified by runtime inspection;
- annotate all public straight-skeleton and other currently incomplete
  wrappers;
- make public `__all__` boundaries explicit so imported helper aliases are not
  accidental API; and
- retain its useful stub/export parity and wheel-content checks while adding
  semantic signature/result fixtures.

### libigl corrections

The libigl slice must:

- add one reviewed `.pyi` for every one of its 13 private extension modules;
- remove the extension-import ignores after those stubs are in scope;
- annotate all 21 public wrappers and their exported results;
- distinguish `scipy.sparse.csc_matrix` results from dense NumPy arrays and
  distinguish Python list/tuple results from native arrays;
- replace `MeshType` casts and package-local mesh shapes with core
  `VerticesFaces`; and
- expand the installed consumer beyond its current curated eight functions to
  every supported public wrapper and plugin implementation.

No private native module becomes public merely because it has a stub.

## Typed distribution and verification

For each native package, completion requires:

- `pyright --verifytypes <package> --ignoreexternal` with 100% known types for
  the intentionally exported public surface;
- strict source Pyright with no unknown native imports;
- a stub/export parity test for every compiled module;
- runtime ABI fixtures for every native function family, covering actual
  result class, dtype, rank/shape, ownership, and representative failures;
- package tests proving every `.pyi` and `py.typed` is present in the wheel and
  that no stub exists only in the checkout;
- an external clean installed-wheel consumer with `assert_type` coverage for
  every public wrapper and plugin family;
- direct handoff of applicable native results into core constructors under ADR
  016; and
- lowest/current supported dependency jobs where NumPy/SciPy typing or runtime
  representation can differ.

`py.typed` is a package-wide promise. A marker plus a small curated green
fixture is not sufficient evidence when public functions still expose unknown
types.

## Compatibility and migration

This work corrects annotations and the accepted structural inputs; it does not
redesign numerical algorithms. Preserve runtime result representations unless
an existing public annotation already promises a different approved contract.
Any such mismatch is recorded and tested as a deliberate compatibility choice,
not silently converted during stub cleanup.

CGAL and libigl migrate in parallel only after ADR 016 supplies the common
vocabulary. Core/plugin conformance and installed consumers integrate the two
packages before the typing initiative can be closed.

## Consequences

- Both native packages give `py.typed` the same enforceable meaning.
- Stubs verify the compiled seam instead of merely suppressing it.
- Public wrappers remain convenient and duck-typed while native ABIs remain
  exact.
- Backend result types become directly usable by core constructors without
  casts or list conversions.
- Stub maintenance grows, but parity, runtime, and artifact tests make that
  maintenance observable.

## Affected packages

`compas_cgal`, `compas_libigl`, shared hook declarations in `compas`, and
installed integration fixtures in `compas_framework`.

## Dependencies

- [005 — Native normalization](005-native-normalization.md)
- [006 — Plugin conformance](006-plugin-conformance.md)
- [008 — Return normalization](008-return-normalization.md)
- [009 — Typed distribution](009-typed-distribution.md)
- [010 — Verification ratchet](010-verification-ratchet.md)
- [016 — Core structural type vocabulary](016-core-structural-type-vocabulary.md)

## Approval boundary

This decision is **Proposed**. Adding libigl stubs, correcting CGAL stubs,
removing ignores, changing public annotations, and making 100% public type
completeness blocking require explicit approval before package source changes.
