# Typing Alignment Architecture Proposal

## Status

Approved. ADRs 001–011 are Accepted and authorize the phased implementation
described below.

## Summary

Align `compas`, `compas_occ`, and `compas_cgal` around one truthful rule:

> Public annotations describe values the public API genuinely accepts; native
> adapters normalize those values to exact backend buffers; return annotations
> describe the representation callers actually receive.

The design distinguishes three boundaries that are currently conflated:

1. **Coercible public input**: Python/COMPAS values and supported NumPy values.
2. **Exact native ABI buffer**: validated dtype, rank, shape, and memory layout.
3. **Retained result buffer**: a zero-copy buffer whose ownership and concrete
   type remain visible to the caller.

This is deliberately not a universal array framework. It uses small explicit
aliases, runtime validation for constraints Python typing cannot express, and
localized native-boundary uncertainty.

Public Python APIs remain duck typed. Aliases describe verified common inputs,
not nominal runtime allow-lists. Code should use values through their documented
operations and should not add `isinstance` checks, copies, or conversions merely
to mirror annotations. Early validation is reserved for stated invariants,
object validity, and safe native calls. Repeated capability contracts may use a
small Protocol only when concrete consumers and tests justify it.

## Recommended contracts

### Version and tooling baseline

- Python 3.12+ in all three packages.
- Integration packages require `compas>=3,<4`.
- NumPy 1.26+ as the tested Python 3.12 baseline, plus current NumPy 2.x.
- Pin Pyright 1.1.414, the version verified in `compas3` for the approved
  implementation baseline.
- Use Pyright only; do not add mypy.
- Run authoritative checks through `compas3`.

### Numeric and coordinate inputs

Core owns aliases for Python and NumPy real/integral scalar inputs, coordinate
inputs, coordinate collections, and index collections. The aliases include
NumPy arrays and NumPy scalar values only where runtime behavior intentionally
supports them.

Do not use `numpy.typing.ArrayLike` as the default geometry input type. It is
appropriate for APIs that really call `np.asarray` on broad numerical input,
but it overstates many ordinary geometry contracts.

### Dtype, shape, and layout

Annotations express dtype where NumPy supports it reliably. Shape, rank,
contiguity, writability, ownership, finiteness, and index range remain explicit
docstring and runtime-validation contracts. Descriptive `Annotated` shape
metadata must not be presented as checker enforcement.

### Tessellation buffers

`Tessellation` remains the explicit zero-copy exception to ordinary normalized
containers. Its generic bounds accept supported nested Python sequences,
NumPy arrays, and compatible native buffers while preserving the concrete
buffer type. Construction checks only the minimal structural invariants needed
for a valid retained object and does not coerce or take ownership.

### Native adapters

Public wrappers accept the approved broad input contract. Private adapters
normalize it before native calls.

- CGAL: C-contiguous `float64` coordinates and `int32` indices.
- OCC: enforce required dimensions at the native boundary and convert only
  scalars PythonOCC demonstrably requires to Python `float`/`int`, immediately
  before SWIG calls. OCC continues returning core objects/Python containers.

### Plugins

Core owns documented public invariants and plugin signatures. A public wrapper
validates only when early enforcement is necessary, does not nominally gate
usable duck-typed values, and does not duplicate backend validation. It may
dispatch to a narrow private pluggable. Backend functions use explicit matching
signatures instead of generic `*args, **kwargs`.

Conformance is checked with runtime signature tests and typed integration
fixtures. Do not create a separate Protocol for every plugin operation.

Plugin typing must not turn unsupported backend semantics into authoritative
values. In particular, unknown BRep predicates must not be represented as
`False`, and unavailable trim extraction must not be represented as an empty
topology. ADR 011 requires an independently failing query boundary for these
cases; other plugin signature alignment remains independent.

### OCC subclassing and native isolation

Core base-class signatures are authoritative. OCC overrides accept the same or
broader inputs and return compatible public types. Backend-specialized items do
not justify incompatible invariant list annotations. PythonOCC downcasts and
incorrect upstream overloads are localized in small boundary helpers with
narrow, explained ignores.

### Returns and serialization

- Ordinary geometry/datastructure APIs return COMPAS objects, Python
  containers, and Python scalar values.
- Explicit numerical APIs may return NumPy arrays.
- `Tessellation` may retain NumPy/native buffers.
- Plugins return the representation declared by core.
- Serialization normalizes NumPy arrays/scalars to lists and Python built-ins.

When a backend result differs from a declared public representation,
normalization occurs once at that public, plugin, or serialization boundary and
only when needed.

Do not introduce a broad hierarchy of serialization `TypedDict` definitions.
Type only stable, versioned public records where it materially helps.

### Typed distribution

All three packages ship `py.typed`. CGAL continues maintaining native `.pyi`
files initially, with exported-name parity, typed smoke tests, and wheel-content
verification. Stub generation is deferred until it demonstrably improves the
maintained contracts. OCC relies on inline typing and upstream PythonOCC stubs,
adding only narrow local corrections where evidence requires them.

## Alternatives and tradeoffs

### Keep sequence-only public types

Simple, but rejects NumPy inputs already supported at runtime and leaves native
plugins dependent on ignores. Rejected.

### Use `ArrayLike` everywhere

Compact, but accepts scalars, strings, and shapes that many geometry APIs do not
support. Rejected as an over-promise.

### Introduce shape-typed tensor generics

Potentially expressive, but Pyright cannot enforce the important runtime
layout/ownership constraints and COMPAS has no current consumer requiring that
complexity. Rejected.

### Normalize all data to NumPy

Would simplify native adapters but changes allocation, ownership, dependency,
and public return semantics across core. Rejected.

### Normalize everything to Python lists

Would remove typing ambiguity but destroy approved zero-copy tessellation and
native interoperability. Rejected.

### Suppress existing backend errors

Fast, but hides real override and stale-API defects. Rejected. OCC errors are
ratcheted down through scoped work packages.

### Generate all native stubs immediately

Generation cannot infer dtype, ownership, or semantic contracts and may produce
worse APIs. Retain maintained stubs plus parity checks first.

## Package effects

### `compas`

- Consolidate central numeric/coordinate/index aliases.
- Make `Tessellation` buffer generics truthful for NumPy/native buffers.
- Align Mesh construction and selected scalar returns.
- Add validated plugin wrappers and typed consumer fixtures.
- Ship `py.typed`.

### `compas_cgal`

- Separate broad wrapper inputs from exact native arrays.
- Apply `float64`/`int32` C-contiguous normalization consistently.
- Align plugin signatures and result representations with core.
- Remove suppressions made unnecessary by truthful core buffer types.
- Verify stubs and typed wheel contents.

### `compas_occ`

- Align Python and COMPAS version metadata.
- Add Pyright, `py.typed`, and CI checks.
- Correct Curve, Surface, NURBS, BRep, and plugin substitutability.
- Centralize PythonOCC/SWIG conversion and downcast helpers.
- Add intentional NumPy input normalization only where the public contract
  supports it.

### `compas_framework`

- Own cross-package consumer fixtures, version matrix, wheel checks, and status.

## Compatibility implications

- Most core NumPy work widens annotations to match existing runtime behavior.
- Typed consumers may see deliberate changes where current annotations are
  wrong or backend overrides are incompatible.
- Python/NumPy metadata alignment removes unsupported combinations.
- Python scalar normalization for ordinary APIs is a small runtime change and
  requires explicit tests.
- Adding `py.typed` exposes annotations to downstream checkers; wheel checks
  must precede that claim.
- OCC stale-API and override corrections may reveal real runtime defects and
  must be tested per family.

No compatibility shims or duplicate old annotations are recommended.

## Tests and documentation

### Static consumer fixtures

Cover accepted and expected-error calls for:

- Python lists/tuples and COMPAS objects;
- NumPy `float32`/`float64`, `int32`/`int64` arrays;
- NumPy scalar inputs;
- invalid dtype/rank/shape calls;
- plugin results and subclass returns.

### Runtime matrix

Cover contiguous, sliced/non-contiguous, Fortran-order, read-only, and
zero-dimensional arrays. Assert acceptance, normalization, rejection, output
dtype, shape, contiguity, ownership, and source non-mutation as applicable.

### Native and distribution checks

- Import every compiled module in `compas3`.
- Verify wrapper-to-ABI normalization.
- Verify every native module has a stub and matching exported names.
- Install built wheels and type-check an external consumer.
- Verify `py.typed` and `.pyi` files are present in wheels.

### Documentation

Document broad inputs separately from native ABI constraints. State which
properties annotations express and which runtime validation enforces. Include
examples for Python and NumPy inputs and ownership-sensitive results.

## Accepted decisions

1. Supported baseline and checker.
2. Numeric scalar and array input policy.
3. Dtype versus shape/layout guarantees.
4. Retained Tessellation buffer contract.
5. Public-to-native normalization boundary.
6. Plugin signature ownership and conformance.
7. Backend subclass substitutability and OCC isolation.
8. Public return normalization.
9. Typed distribution and native stubs.
10. Verification and error ratchet.

ADRs 001–011 are Accepted and authorize the phased implementation below.

## Phased implementation

1. Align metadata/tooling and add consumer fixtures.
2. Establish core scalar/array vocabulary.
3. Make core retained buffers and selected returns truthful.
4. Align plugin boundaries.
5. Normalize CGAL wrappers/stubs and OCC SWIG boundaries in parallel.
6. Correct OCC public subclass families in independent owned work packages.
7. Verify source, wheels, native imports, documentation, and downstream use.

See `implementation-plan.md` for dependencies and ownership.

## Proposed architecture correction: representations are not algorithm gates

New evidence from the core and `compas_cgal` implementation shows that the
current design conflates retained discrete representations, numerical mesh
boundaries, and algorithm selection. Native CGAL consumes raw arrays, while a
core decorator nominally requires `Tessellation` for more than eighteen mesh
operations. Empty strategy objects such as `Delaunay` and `Native` also expose
dispatch choices as top-level geometry classes.

The proposed correction is:

1. retain `Tessellation` as an explicit discrete representation for parametric
   conversion, visualization, and transfer;
2. make numerical triangle-mesh and plugin boundaries structural
   `(vertices, triangles)` contracts that accept Python and NumPy buffers;
3. replace nominal `Tessellation` gates with public validation wrappers and
   private backend hooks;
4. replace empty triangulation flags with named operations;
5. replace universal tessellation strategy objects with explicit,
   producer-specific keyword controls.

Named Delaunay operations remain planar-domain algorithms. Three-dimensional
coordinates are accepted only when coplanar in the explicit or documented
default frame; there is no implicit curved-domain flattening. Non-planar
polygon triangulation remains the responsibility of the polygon and
`PolygonalSurface` algorithms. Slightly curved domains are deferred to a
future, separately named approximation contract.

Do not add `TriangleMesh` or `QuadMesh` classes. Face arity is an operation
invariant, and existing `Mesh`, `PolygonalSurface`, and `Tessellation`
representations already cover the required object roles. Do not retain
permanent dual object/raw algorithm paths.

This correction is specified by Accepted ADRs 012–013. It supersedes only the
algorithm-gating interpretation of ADR 004; retained-buffer semantics remain
accepted. The decisions were approved on 2026-11-04. Implementation proceeds
from an affected-API migration table before package source changes.
