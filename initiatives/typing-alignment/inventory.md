# Typing Alignment Inventory

## Scope and method

This inventory records read-only reconnaissance of `compas`, `compas_occ`,
and `compas_cgal`, plus their shared tooling and integration checks. Commands
used the `compas3` environment with Python 3.12, NumPy 2.5.2, and Pyright
1.1.414. No package source was modified.

## Executive summary

The packages do not currently share one typing contract:

- `compas` accepts many NumPy arrays and scalars at runtime, but central
  sequence-based aliases reject them statically.
- `compas_cgal` has useful NumPy/native conventions, but public coercible input
  types, normalized ABI buffers, and returned zero-copy buffers are not clearly
  separated.
- `compas_occ` is not a typed distribution, has no Pyright configuration, and
  exposes numerous backend overrides incompatible with current core APIs.
- Plugin implementations are not statically checked against their core
  pluggable signatures.
- Only `compas_cgal` contains `py.typed` and native `.pyi` files; wheel contents
  and stub/runtime parity are not verified.

The initiative should first define the core runtime/static contract, then align
native boundaries and backend overrides. Removing ignores before those
contracts are explicit would hide rather than solve the design problems.

## Follow-up structural and native-binding audit

The 2026-11-05 follow-up expanded the initial CGAL/OCC inventory to
`compas_libigl` and rechecked core constructor interoperability.

- Core has two overlapping vertices/faces tuple aliases:
  `TriangleMeshInput`, despite its use for results and inability to prove
  triangle arity, and a NumPy-incompatible tuple-valued `MeshType` that can be
  confused with the real `Mesh` class.
- CGAL ships stubs for all 14 extension modules, but verify-types completeness
  is 83% and runtime inspection found inaccurate list/array, parameter, native
  vector, and literal contracts.
- Libigl ships `py.typed` while committed source suppresses all 13 native
  imports. Only 8 of 21 public wrappers are fully annotated; verify-types
  completeness is 51.6%.
- Exact CGAL/libigl `float64` vertex and `int32` face arrays are accepted by
  `Mesh.from_vertices_and_faces` and `Tessellation`, but not consistently by
  `Polygon`, `Polyline`, `Pointcloud`, `PolygonalSurface`, or `Polyhedron`.
- `PolygonalSurface` and `Polyhedron` reject NumPy integer face indices at
  runtime through a concrete `int` check, making the documented direct CGAL
  handoff fail without `.tolist()`.

Proposed ADRs 016–017 record the resulting core vocabulary, constructor,
native-stub, public-wrapper, and installed-artifact decisions. No package
source correction is authorized while those ADRs remain Proposed.

## Baseline

| Repository | Python metadata | Pyright scope | Baseline | Typed distribution |
|---|---|---|---:|---|
| `compas` | `>=3.12` | `src/compas` | 0 errors | no `py.typed` |
| `compas_occ` | `>=3.9` | none configured | 66 source errors; 94 including tests in the audit configuration | no `py.typed` or package stubs |
| `compas_cgal` | `>=3.12` | `src/compas_cgal` | 0 errors with explicit core source/interpreter | `py.typed` plus native stubs |
| `compas_framework` | `>=3.12` | source and tests | 0 errors | integration package only |

The green core and CGAL counts do not prove cross-package correctness. Their
configured scopes exclude typed consumer fixtures, and CGAL needs an explicit
interpreter and local core source path for a reproducible check.

## Core COMPAS

### Central aliases reject supported NumPy inputs

[`compas._typing`](/Users/vanmelet/Code/compas/src/compas/_typing.py) defines:

```python
CoordinateType = Coordinate | Sequence[float]
CoordinatesType = Coordinates | Sequence[CoordinateType]
MeshType = tuple[CoordinatesType, Sequence[Sequence[int]]]
```

NumPy arrays do not satisfy these nested sequence protocols in Pyright, even
though runtime calls succeed. Static probes rejected:

- one-dimensional `float32` and `float64` coordinate arrays;
- two-dimensional coordinate arrays;
- NumPy vertex and face arrays passed to `Mesh.from_vertices_and_faces`;
- NumPy vertex and triangle arrays passed to `Tessellation`.

Equivalent point-coordinate aliases are duplicated in Mesh, VolMesh, and
CellNetwork type modules, creating drift from the central aliases.

### `Tessellation` has a contradictory buffer contract

[`Tessellation`](/Users/vanmelet/Code/compas/src/compas/geometry/tessellation.py)
documents and preserves zero-copy NumPy/native buffers. Runtime validation uses
`numbers.Real` and `numbers.Integral`, correctly accepting NumPy scalar values.
Its generic bounds and optional normal/UV/polyline annotations remain
sequence-centric and reject those arrays statically. CGAL currently needs
Pyright suppressions at this boundary.

### Numeric scalar behavior is inconsistent

Newer APIs use `Real` and `Integral`; older APIs often test only built-in
`int`/`float`. Therefore `np.float64`, `np.float32`, `np.int32`, and `np.int64`
acceptance varies between otherwise equivalent operations. Some linalg
functions return NumPy scalar integers where ordinary geometry APIs normally
return Python built-ins.

### Different array boundaries are conflated

The code needs distinct contracts for:

1. general coordinate inputs;
2. coercible numerical computation inputs;
3. exact retained zero-copy buffers;
4. native ABI buffers;
5. serialized normalized data;
6. sparse matrices.

`numpy.typing.ArrayLike` is already used successfully in linalg, but many
returns remain `NDArray[Any]` or unparameterized. NumPy typing expresses dtype
more reliably than shape; documented/runtime shape validation remains
necessary.

### Plugins

The plugin decorator preserves a callable signature locally, but registered
implementations are stored as `Callable[..., Any]`. Backend conformance depends
on repeating signatures manually and is not checked across repositories. The
validated-public-wrapper/private-pluggable pattern used by planar
triangulation is a useful precedent: core owns broad input validation and the
plugin receives a narrower contract.

## COMPAS OCC

### Version and distribution mismatch

`compas_occ` still declares Python `>=3.9`, while current core requires 3.12+.
Its COMPAS dependency is unbounded. It has no Pyright configuration or CI type
check, no `py.typed`, and no package-owned native stubs.

### Backend subclasses are not substitutable

Pyright exposes repeated incompatibilities in Curve, Surface, NURBS, and BRep
subclasses:

- narrowed parameters in overrides and constructors;
- missing core parameters such as `world` or domains;
- property/method disagreements for length and bounds;
- invariant `list[BackendSubtype]` returns overriding `list[CoreBase]`;
- narrowed mutable native attributes;
- `__eq__` methods narrowed from `object` to a concrete OCC class;
- stale calls to removed core materialization APIs.

These are cross-package API defects, not checker noise.

### PythonOCC/SWIG boundary

The source and tests contain many broad ignores around overloads and native
downcasts. Repeated topology conversions should be localized in typed boundary
helpers. Narrow documented ignores may remain only where upstream stubs are
incorrect.

Plugin modules contain many unannotated functions and generic `*args,
**kwargs`, preventing signature comparison with core pluggables. Some plugins
still expose legacy tessellation contracts.

### NumPy behavior is accidental and dtype-dependent

OCC conversion functions are typed as concrete lists. Runtime probes show that
some `float64` arrays work while `float32` or integer arrays fail at SWIG
setters. NumPy support therefore requires explicit rank/shape checks and
normalization with `float(...)` and `int(...)` at the Python-to-SWIG boundary.
Simply widening annotations would be incorrect.

OCC should normally return core objects and Python containers. Introducing
NumPy outputs is unnecessary unless a separate real performance contract
requires them.

## COMPAS CGAL

### Existing native convention

CGAL's strongest pattern is its native tessellation boundary:

- coordinates normalized to C-contiguous `float64`;
- indices range-checked and normalized to C-contiguous `int32`;
- native output buffers retained by `Tessellation`.

Tests verify dtype, contiguity, and ownership. `NDArray` annotations cannot
express C-contiguity, so this must remain a documented runtime contract.

### Public input versus native buffer types

[`compas_cgal.types`](/Users/vanmelet/Code/compas_cgal/src/compas_cgal/types.py)
contains dtype aliases such as `FloatNx3` and `IntNx3`. Their `Annotated` shape
metadata is descriptive; Pyright does not enforce it.

Wrappers inconsistently accept nested lists, `Point` objects, raw/unparameterized
arrays, or exact dtype arrays, even when all immediately call `np.asarray`.
The architecture should distinguish:

- broad public coercible input;
- exact native buffer passed to compiled code;
- retained native output.

### Return and plugin mismatch

Some modern operations return `Tessellation`; older APIs return raw NumPy
tuples. Some plugin implementations return NumPy polyline arrays while the
core contract declares nested Python lists. These must be aligned at the core
boundary rather than left as backend-specific static behavior.

### Native stubs

The repository has hand-written `.pyi` files for compiled modules, but no stub
generation or parity check against nanobind exports. Shape and contiguity remain
runtime concerns. Package tests check source-file presence, not installed-wheel
contents or signature agreement.

## Serialization

Core deliberately serializes NumPy arrays and scalars to Python lists and
built-ins. This normalized data contract is separate from retained zero-copy
operation buffers. OCC BRep/NURBS serialization uses largely unparameterized
dictionaries; stable public schemas may benefit from typing, but speculative
`TypedDict` proliferation should be avoided.

## Tooling and CI

- Pyright is the shared checker; no package uses mypy.
- Pyright should be pinned and run through `compas3` for the initiative.
- `compas_occ` needs a first-class Pyright configuration and ratchet to zero.
- Core and CGAL need typed consumer fixtures in addition to source checking.
- Python metadata and CI matrices are inconsistent, especially OCC and the
  framework integration repository.
- Minimum supported NumPy claims are not verified against the current Python
  baseline.
- Built-wheel tests should verify `py.typed`, `.pyi` inclusion, compiled-module
  imports, and external consumer type checking.

## Existing runtime test coverage

Useful existing coverage includes:

- core NumPy JSON arrays/scalars;
- core NumPy transformations and NumPy-backed `Tessellation`;
- CGAL native dtype, contiguity, ownership, triangulation, and meshing output.

Important gaps include:

- Python versus NumPy scalar matrices;
- `float32`/`float64` and `int32`/`int64` inputs;
- contiguous, sliced/non-contiguous, Fortran-order, read-only, and zero-
  dimensional arrays;
- typed consumer fixtures with accepted and expected-error cases;
- OCC NumPy normalization tests;
- native stub/runtime parity and installed-wheel typing tests;
- lowest supported NumPy and current NumPy 2.x CI.

## Architectural decisions required

1. Supported Python, COMPAS, NumPy, and Pyright version baseline.
2. Public numeric scalar policy, including input acceptance and output
   normalization.
3. Core coordinate, mesh, and retained-buffer contracts for NumPy support.
4. Boundary between coercible public inputs and exact native ABI buffers.
5. Shape/dtype guarantees expressed statically versus documented and validated
   at runtime.
6. Plugin signature ownership and cross-repository conformance verification.
7. Backend subclass substitutability and collection variance policy.
8. PythonOCC/SWIG isolation and ignore policy.
9. Native stub generation/parity and PEP 561 distribution policy.
10. NumPy-versus-core-object return conventions.
11. Serialization schema typing scope.
12. Verification and ratcheting strategy for existing OCC errors.

## Principal risks

- Widening annotations beyond actual runtime acceptance.
- Adding runtime conversion only to appease static typing.
- Treating dtype or shape annotations as runtime enforcement.
- Changing list returns to abstract covariant collections solely to silence
  override errors.
- Spreading `Any` from native boundaries into public APIs.
- Shipping inline annotations or stubs that are absent or stale in wheels.
- Attempting to fix all annotations before agreeing on the shared contracts.

## Recommended dependency order

1. Align version/tooling baseline.
2. Decide core scalar and array boundary contracts.
3. Make core aliases and `Tessellation` truthful.
4. Align plugin signatures and backend public wrappers.
5. Normalize CGAL and OCC native boundaries.
6. Establish stub/distribution verification.
7. Ratchet ignores and OCC errors down through small independently tested work
   packages.
