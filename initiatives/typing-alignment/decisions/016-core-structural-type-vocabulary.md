# Title: What structural type vocabulary should core and numerical packages share?

## Status

Accepted.

## Context

The accepted numeric-input decisions established that appropriate Python and
NumPy values are first-class inputs, but the current core vocabulary does not
express that contract consistently:

- `TriangleMeshInput` is used for both parameters and results, so its
  direction suffix is false. It also cannot enforce triangle arity.
- `MeshType` is a tuple of vertices and faces, not a `Mesh`. It overlaps
  `TriangleMeshInput`, excludes NumPy arrays, and conflicts lexically with
  several actual `Mesh`-bounded type variables.
- `Coordinate`, `CoordinateType`, and `CoordinateInput`, and their plural
  counterparts, expose overlapping meanings that are not apparent from their
  names or connected to the familiar geometric idea of a point-like value.
- `PolygonalSurface`, `Polyhedron`, `Polygon`, `Polyline`, and `Pointcloud`
  reject suitable NumPy values statically even where their copying runtime
  paths can consume them.
- `PolygonalSurface` and therefore `Polyhedron` additionally reject NumPy
  integer face indices at runtime through a concrete `int` check, despite the
  accepted integral-input contract.
- `compas_cgal` duplicates broad public aliases as `Vertices`, `Faces`, and
  `VerticesFaces`; `compas_libigl` uses both the core aliases and casts around
  `MeshType`. The packages can therefore type the same structural value
  differently.

Measured consumers confirm that CGAL's normal `float64` vertex and `int32`
face result is accepted directly by `Mesh.from_vertices_and_faces` and
`Tessellation`, but rejected by `PolygonalSurface` and `Polyhedron`. Calls that
add `.tolist()` or `cast(...)` conceal this mismatch rather than resolving the
shared contract.

Focused Pyright 1.1.414 experiments through `compas3` show that neither a
single exact indexing protocol nor an iteration-only protocol is sufficient:

- a protocol with `__len__`, `__iter__`, and only
  `__getitem__(int) -> SupportsFloat` rejects `list[float]`, `list[int]`,
  tuples, memoryviews, COMPAS `Point` and `Vector`, and NumPy arrays because
  their real indexing signatures are overloaded or include slices;
- a protocol with only `__len__` and
  `__iter__ -> Iterator[SupportsFloat]` accepts those one-dimensional values,
  but does not prove the indexing and slicing used throughout current geometry
  code; and
- a layered alias combining a rich generic protocol, ordinary `Sequence`, and
  `NumericArray` accepts the same values while typing both integer indexing and
  slicing without pretending a slice is another point.

The successful protocol overloads integer access to its scalar type and slice
access to `Sequence` of that type. The public aliases add `Sequence` and
`NumericArray` branches because built-ins and NumPy arrays need not match the
protocol's exact overload implementation. Under the same checker, the layered
design passed with zero errors for float/int lists, tuples, memoryviews,
one-dimensional float64/int32 arrays, COMPAS `Point` and `Vector`, a nominal
protocol implementation, nested point/index lists, two-dimensional
point/index arrays, three-dimensional point-group arrays, and empty tuple
defaults. The integer-indexed collection protocol also accepts current
`Line`, `Plane`, `Frame`, and overloaded `Polyline` implementations. The probe
verified `point[0]`, `point[:2]`, `float(point[0])`, and
`list(point[:2])` for every coordinate-alias branch.

A further arithmetic probe exposed an important tradeoff. `SupportsFloat`
proves conversion, not direct arithmetic: a consumer cannot safely write
`point[0] * point[0]` without adding conversions that do not exist today.
Using the already approved `RealInput` scalar family preserves current direct
arithmetic for Python and NumPy real scalars. The complete layered alias with
`RealInput` passed lists, tuples, float32/float64 NumPy vectors, nominal point
implementations, indexing, slicing, and direct arithmetic with zero Pyright
errors.

## Options

1. **Keep the current names and add more unions.** This minimizes renaming but
   retains two overlapping mesh-tuple aliases and directionally false names.
2. **Define nominal `TriangleMesh` and `QuadMesh` classes.** This makes arity
   visible but adds representations that duplicate `Tessellation`,
   `PolygonalSurface`, and `Mesh`, and still does not describe raw arrays.
3. **Use one core-owned structural vocabulary with explicit protocol, input,
   and concrete-result names.** Express face arity as an operation invariant,
   and make owning core constructors accept the same supported numerical
   inputs.
4. **Use `numpy.typing.ArrayLike` everywhere.** This is concise but promises
   coercions and scalar/object forms that many geometry APIs do not support.

Within option 3, `RealInput` describes the Python and NumPy numeric scalars on
which existing consumers perform arithmetic directly. `SupportsFloat` would
describe a broader conversion capability but require new `float(...)` calls,
casts, or ignores throughout those consumers. The recommendation chooses
`RealInput`: annotations follow existing runtime behavior and must not create
runtime work solely to satisfy static typing.

## Recommendation

Choose option 3.

### Naming rules

- A public duck-typed boundary uses a familiar semantic name with a `Like`
  suffix. The name describes the argument's geometric role, not a nominal
  runtime category.
- A reusable structural interface uses a `Protocol` suffix. It exists to
  express operations and runtime duck membership; it is not an input gate.
- An `Input` suffix is used only for a value accepted at a call boundary, not
  for a result or bidirectional interchange value.
- A neutral structural tuple is named for its contents, not for a COMPAS class
  that it is not.
- A concrete returned representation is annotated concretely rather than with
  a broader accepted-input alias.
- Raw geometric tuples use a `Data` suffix rather than a generic `Type`
  suffix.

The coordinated migration is:

| Current name | Decision | Replacement |
|---|---|---|
| `FloatSequence` protocol and `FloatSequenceType` union | Preserve a neutral role for quaternion and generic linear-algebra inputs without duplicating the coordinate protocol. | `FloatSequenceLike`; use `PointLike` or `VectorLike` where the argument has that semantic role, and an exact type for concrete results |
| `RawCoordinateType` | Remove; it is unused and narrower than the accepted contract. | None |
| runtime-checkable `Coordinate` | Retain one technical structural capability with truthful index/slice operations. | `CoordinateProtocol[T_co]` |
| `CoordinateType`, `CoordinateInput`, `PointCoordinates` | Replace ambiguous coordinate names according to geometric argument role. | `PointLike` or `VectorLike`; exact outputs remain explicit tuples/lists |
| runtime-checkable `Coordinates` | Retain the collection capability required by existing equality guards. | `PointsProtocol` |
| `CoordinatesType`, `CoordinatesInput` | Use one NumPy-aware collection alias. | `PointsLike` |
| `Indices`, `IndicesInput` | Separate the technical row protocol from the public NumPy-aware alias. | `IndicesProtocol`, `IndicesLike` |
| `IndicesCollection`, `IndicesCollectionInput` | Name the nested structural role rather than its container. | `IndexGroupsProtocol`, `IndexGroupsLike` |
| `CoordinatesCollection`, `CoordinatesCollectionInput` | Name collections of point groups explicitly. | `PointGroupsProtocol`, `PointGroupsLike` |
| `TriangleMeshInput` | Remove the directional and unenforced triangle name. | `VerticesFaces` |
| tuple-valued `MeshType` | Remove the name that conflicts with the actual `Mesh`. | `VerticesFaces` |
| `SphereType` | Rename the raw center/radius tuple and make its payload explicit. | `SphereData = tuple[PointLike, RealInput]` |
| `RayType` | Rename the raw origin/direction tuple and make its semantic roles explicit. | `RayData = tuple[PointLike, VectorLike]` |
| `RayMeshHit` | Keep; it is neutral and descriptive. | `RayMeshHit` |

`RealInput`, `IntegralInput`, `NumericArray`, `FloatingArray`, `IntegerArray`,
`Float64Array`, and `Int32Array` remain. Their names accurately distinguish
accepted scalars from concrete array representations.

### Authoritative structural aliases

Core owns the common vocabulary in the public `compas.typing` module. Package
code and integrations import shared aliases from that module; they do not
import the private `compas._typing` path. After every in-scope import migrates,
remove `_typing.py` directly without re-exports or a forwarding shim.

In Python 3.12 notation, the relevant shape is conceptually:

```python
@runtime_checkable
class CoordinateProtocol[T_co](Protocol):
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[T_co]: ...

    @overload
    def __getitem__(self, key: int) -> T_co: ...

    @overload
    def __getitem__(self, key: slice) -> Sequence[T_co]: ...

type FloatSequenceLike = (
    CoordinateProtocol[RealInput]
    | Sequence[RealInput]
    | NumericArray
)
type PointLike = FloatSequenceLike
type VectorLike = FloatSequenceLike

@runtime_checkable
class PointsProtocol(Protocol):
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[PointLike]: ...
    def __getitem__(self, key: int) -> PointLike: ...

class IndicesProtocol(Protocol):
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[SupportsIndex]: ...
    def __getitem__(self, key: int) -> SupportsIndex: ...

type PointsLike = PointsProtocol | Sequence[PointLike] | NumericArray
type IndicesLike = IndicesProtocol | Sequence[SupportsIndex] | IntegerArray

class IndexGroupsProtocol(Protocol):
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[IndicesLike]: ...
    def __getitem__(self, key: int) -> IndicesLike: ...

class PointGroupsProtocol(Protocol):
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[PointsLike]: ...
    def __getitem__(self, key: int) -> PointsLike: ...

type IndexGroupsLike = (
    IndexGroupsProtocol | Sequence[IndicesLike] | IntegerArray
)
type PointGroupsLike = (
    PointGroupsProtocol | Sequence[PointsLike] | NumericArray
)
type VerticesFaces = tuple[PointsLike, IndexGroupsLike]
type SphereData = tuple[PointLike, RealInput]
type RayData = tuple[PointLike, VectorLike]
```

`FloatSequenceLike`, `PointLike`, and `VectorLike` deliberately have the same
accepted structure without duplicate protocol bodies. `FloatSequenceLike` is
the neutral name for quaternions and generic linear-algebra inputs. The
semantic aliases make signatures such as
`Plane(point: PointLike, normal: VectorLike)` read according to geometry
semantics; they do not create nominally distinct runtime categories, and a
point does not structurally reject a vector or vice versa.

The coordinate slice overload returns `Sequence[T_co]`, not `PointLike` or
`VectorLike`. A two-component slice is not semantically a point or vector, and
recursively typing it as one causes false structural failures. Collection
protocols are defined only with the integer access used by current common
consumers. Lists and tuples still expose slicing through their concrete
`Sequence` branch, but the shared `PointsLike` contract does not promise
slicing for every custom point collection. No speculative `Like` hierarchy is
added.

Neither `Sequence` nor current NumPy typing encodes coordinate arity or array
rank in these aliases. One-dimensionality and required component count remain
operation contracts enforced by existing constructor or native-boundary
behavior. The aliases do not authorize a separate eager validation pass.

Explicit NumPy union members remain necessary for nested matrices and higher
collections: Pyright does not model them as satisfying the nested iterable
protocols reliably. Protocols support stable duck-typed consumers; they do not
replace the array members or justify nominal runtime checks.

### Runtime preservation

`RealInput` is the shared point/vector element contract because it supports the
arithmetic current consumers already perform. Implementations continue using
those values directly. They must not add `float(...)`, `np.asarray(...)`,
copies, validation passes, casts, or ignores merely to make an annotation
type-check.

An individual constructor or setter may use `SupportsFloat` only when its
existing implementation already calls `float(...)` on that parameter and the
annotation is documenting that established behavior. `Point` and `Vector`
constructor components and their `x`/`y`/`z` setters are the initial examples:
they already store `float(value)`. Such a local scalar annotation does not
broaden the element contract of `FloatSequenceLike`, `PointLike`, or
`VectorLike`. Any broader runtime acceptance or new normalization requires a
separate explicit behavior decision.

Every alternative of `RealInput` must remain statically assignable to
`SupportsFloat`. Therefore a scalar obtained from a one-dimensional
`PointLike` or `VectorLike` can be passed directly to an existing normalizing
scalar API—for example, `point.x = point_like[0]`—without a call-site
conversion, cast, or ignore. Any future expansion of `RealInput` must preserve
this invariant or require a separate explicit decision.

### Static capability and runtime membership

`CoordinateProtocol` and `PointsProtocol` are `@runtime_checkable` only because
existing public equality behavior and tests use structural coordinate and
coordinate-collection membership. Runtime guards use the corresponding
unparameterized protocol, never `PointLike`, `VectorLike`, or `PointsLike`:
the semantic aliases are static unions, not runtime allow-lists. Constructors,
numerical wrappers, and native adapters must not add protocol membership gates.

Runtime protocol membership checks method presence, not overload signatures or
element types. Lists, tuples, NumPy vectors, and COMPAS `Point`/`Vector` retain
their current duck behavior because all are indexable and iterable. Core
`Point` and `Vector` explicitly declare `CoordinateProtocol[float]` conformance
so their intended relationship is checked rather than inferred accidentally;
their existing integer and slice overloads satisfy the measured protocol.

Runtime protocol checks cannot inspect iterator element types. Equality still
uses its existing length and component-comparison behavior; the protocol alone
does not turn invalid elements into a validated geometric value. Focused tests
pin current `False` and exception outcomes for
`Point`, `Vector`, `Plane`, `Line`, `Frame`, and `Polyline` equality with
ordinary sequences, COMPAS objects, iterable-only ducks, invalid iterables,
and NumPy values.

Iterable-only and indexing-only ducks do not satisfy the complete runtime
protocol. Migration fixtures record whether each remains dynamically usable by
a particular operation through Python's ordinary fallback behavior; neither is
silently promoted to the shared static contract.

### Indexed-consumer migration

Migration is not a mechanical annotation rename. WP8.1 inventories every
consumer of the removed coordinate aliases that subscripts its operand.

- Use the rich protocol's integer and slice operations where current code
  genuinely indexes. Prefer iteration, unpacking, or `zip` where that already
  expresses the operation more directly and preserves behavior.
- Do not introduce another operation-specific coordinate protocol merely to
  avoid an accurate `PointLike`/`VectorLike` annotation, and do not hide a
  mismatch with `Any`, a cast, or an ignore.
- Preserve currently tested runtime duck behavior unless a separate approved
  contract explicitly removes it. Static aliases need not enumerate every
  object that Python can consume dynamically.

Each changed consumer has accepted static fixtures, runtime duck fixtures,
and an expected-error case. The migration may alter implementation mechanics
only where tests prove the observable values, order, exceptions, mutation, and
allocation contract remain unchanged.

`VerticesFaces` is the sole public structural vertices/faces interchange
alias. It is suitable for both arguments and results. Whether its faces are
triangles, quads, or arbitrary polygons is an operation contract documented
and checked at the boundary that requires that invariant; the current Python
and NumPy type systems cannot enforce row length here. Do not add synonymous
`VerticesTriangles`, `TriangleMeshData`, or `MeshLike` aliases.

Core owns the primitive `Float64Array` and `Int32Array` aliases but does not own
an ABI-specific vertices/faces tuple. A native package may define an internal
`VerticesFacesNumpy = tuple[Float64Array, Int32Array]` alias when that exact
pair is repeatedly returned. Such an alias describes concrete package output;
it is not a competing public input vocabulary or a new geometry
representation.

### Input and output policy

Public Python and plugin parameters use the narrowest applicable core input
or structural alias. They do not use backend-local copies of those aliases.

Results state what is actually returned:

- a normalized Python result uses `float`, `int`, `list[...]`, or an exact
  tuple of those values;
- a retained or native NumPy result uses `Float64Array`, `Int32Array`, or an
  exact package-local array tuple;
- a result intentionally permitted to vary between compatible Python and
  NumPy structural buffers uses `VerticesFaces`;
- sparse matrices and heterogeneous tuples use their actual library and
  element types, not `NDArray` or `Any`.

Using a broad accepted-input alias as a result annotation is allowed only when
the public contract deliberately permits every representation in that union.
It is not a shortcut for an unknown native return type.

Representative semantic signatures use the aliases consistently:

```python
class Plane:
    def __init__(self, point: PointLike, normal: VectorLike) -> None: ...

class Line:
    def __init__(self, start: PointLike, end: PointLike) -> None: ...

class Frame:
    def __init__(
        self,
        point: PointLike,
        xaxis: VectorLike,
        yaxis: VectorLike,
    ) -> None: ...
```

The same role rule applies to functions: positions, locations, and vertices
use `PointLike`; directions, normals, axes, and translations use `VectorLike`.
This is documentation and static intent, not runtime discrimination.

### Core constructor matrix

The following owned constructors accept appropriate NumPy inputs because their
existing semantics copy or normalize the supplied values:

| Constructor | Accepted annotation | Ownership and normalization |
|---|---|---|
| `Point`, `Vector` constructor components and `x`/`y`/`z` setters | `SupportsFloat` | Document their existing `float(value)` storage normalization; no new conversion is introduced. |
| `Plane` and its point/normal setters | `PointLike`, `VectorLike` | Copy point and normal into owned core objects. |
| `Line` and its start/end setters | `PointLike`, `PointLike` | Copy start and end into owned points. |
| `Frame` and its point/xaxis/yaxis setters | `PointLike`, `VectorLike`, `VectorLike` | Copy origin and axes into owned core objects. |
| `Polyline`, `Polygon`, `Pointcloud` | `PointsLike` | Copy coordinates into owned points. |
| `PolygonalSurface`, `Polyhedron` | `PointsLike`, `IndexGroupsLike` | Copy coordinates and normalize each non-boolean copied index through the integer-index protocol. |
| `PolygonalSurface.vertices` and `.faces` setters | `PointsLike`, `IndexGroupsLike` | Apply the same ownership and normalization contract as construction. |
| `Mesh.from_vertices_and_faces` | `PointsLike`, `IndexGroupsLike` | Preserve its existing broad copying contract. |
| `Tessellation` | its generic coordinate/index buffer bounds | Retain compatible buffers without copying, as already documented. |

Quaternion and generic linear-algebra functions that currently use
`FloatSequenceType` migrate to `FloatSequenceLike`, not to a geometric alias.
Functions returning a concrete normalized list say `list[float]`; the few
zero-length normalization paths that deliberately return their original input
may retain `FloatSequenceLike` as the result until that runtime contract is
separately changed.

The `PolygonalSurface` index correction is an approved runtime contract change
if this ADR is accepted: reject Python and NumPy booleans as face indices, and
otherwise use the integer-index protocol while performing the existing
ownership copy. Python and NumPy integral scalars are accepted and stored as
Python `int`. Do not add a separate eager validation/conversion pass. Preserve
existing shape, bounds, failure, and mutation behavior unless another accepted
contract explicitly changes it.

Copying and normalization preserve vertex order, face order, index order, face
winding, and source values apart from the stated scalar representation change.
They never sort, deduplicate, triangulate, or repair topology.

Constructors that retain buffers continue to document identity, ownership,
and mutation. Constructors that own Python values normalize once as part of
their existing copy. No conversion is added merely to satisfy Pyright.
Corresponding public setters or mutators are widened only when they already
share the same verified runtime normalization path; unrelated mutation APIs
are not broadened speculatively.

## Compatibility and migration

This is a coordinated C3 breaking migration. Add `compas.typing`, migrate core
and every in-scope integration, then remove the superseded aliases and
`compas._typing` directly. Do not leave aliases, re-exports, forwarding modules,
or parallel package-local public vocabularies.

The tuple-valued `MeshType` is distinct from local type variables bounded by
the actual `Mesh`; those local type variables may remain but should use a less
ambiguous name such as `MeshT` when touched.

CGAL and libigl may retain package-local aliases for genuinely package-specific
heterogeneous results. Such aliases are built from the core primitive array
types and must not redefine `VerticesFaces` or the accepted point/index
families.

## Verification

- Static accepted/error fixtures for Python lists, tuples, custom structural
  objects, NumPy float32/float64 coordinates, and int32/int64 indices.
- A focused Pyright protocol matrix covering lists of float/int, tuples,
  memoryviews, COMPAS `Point`/`Vector`, one-dimensional NumPy arrays, nested
  Python points, and NumPy point matrices. It proves the rich protocol plus
  `Sequence`/`NumericArray` union, usable scalar/index and sequence/array slice
  unions for `point[0]` and `point[:2]`, unchanged direct arithmetic, and
  nominal `Point`/`Vector` conformance. It does not claim exact scalar
  inference for an unshaped NumPy branch and retains error fixtures for the
  rejected single-signature and iteration-only alternatives.
- A focused Pyright scalar-handoff matrix proving that the complete
  `RealInput` union and representative Python `int`/`float` and NumPy
  integer/floating values satisfy `SupportsFloat`, and that
  `point.x = point_like[0]` plus the corresponding representative `Vector`
  setter assignment require no conversion, cast, or ignore. Point/vector
  element access in this fixture is subject to the one-dimensional operation
  contract; it does not infer shape from the unshaped `NumericArray` alias.
- Static fixtures for `Plane(PointLike, VectorLike)`, `Line(PointLike,
  PointLike)`, and `Frame(PointLike, VectorLike, VectorLike)` using Python,
  COMPAS, and NumPy values.
- Runtime structural-membership and equality fixtures for lists, tuples,
  NumPy vectors, COMPAS objects, iterable-only, indexing-only, and invalid
  ducks, including the existing `isinstance` behavior through unparameterized
  protocols.
- An indexed-consumer inventory proving that every removed coordinate alias is
  migrated to a semantic alias or exact result type without casts or ignores.
- Runtime matrices for contiguous, Fortran-order, sliced, non-contiguous,
  read-only, and empty arrays, with source non-mutation and explicit boolean
  index rejection.
- Direct construction of `Point`, `Vector`, `Polyline`, `Polygon`,
  `Pointcloud`, `PolygonalSurface`, `Polyhedron`, `Mesh`, and `Tessellation`
  from applicable CGAL/libigl results without `.tolist()` or `cast`.
- Assignment of supported NumPy scalars and buffers through the corresponding
  verified `Point`, `Vector`, and `PolygonalSurface` public setters.
- Exact inferred result assertions for Python, NumPy, sparse, and mixed tuple
  results.
- Repository-wide absence checks for every removed alias and package-local
  duplicate, including private `compas._typing` imports.
- Constructor checks that preserve vertex, face, and index order and face
  winding exactly.
- Core and cross-package Pyright, relevant runtime tests, Ruff, formatting,
  strict documentation, installed-wheel consumers, and `git diff --check`.

## Consequences

- Public names describe structures rather than call direction or nonexistent
  geometry classes.
- Core becomes the single dependency direction for shared numerical types.
- Appropriate NumPy results flow directly into equivalent core constructors.
- Triangle and quad invariants remain explicit runtime/operation contracts,
  not nominal classes or misleading aliases.
- The intentional NumPy-integral widening and boolean-index rejection are
  visible and tested rather than hidden behind `.tolist()` calls.

## Affected packages

`compas`, `compas_cgal`, `compas_libigl`, `compas_occ` where it imports the
shared aliases, and `compas_framework` integration fixtures.

## Dependencies

- [002 — Numeric and array inputs](002-numeric-array-inputs.md)
- [003 — Array guarantees](003-array-guarantees.md)
- [004 — Tessellation buffers](004-tessellation-buffers.md)
- [005 — Native normalization](005-native-normalization.md)
- [008 — Return normalization](008-return-normalization.md)
- [012 — Structural triangle-mesh boundaries](012-structural-triangle-mesh-boundaries.md)

## Decision

Approved on 2026-11-05. Core owns one public structural vocabulary with
semantic `PointLike` and `VectorLike` roles, NumPy-aware collection aliases,
and neutral `VerticesFaces` interchange. Misleading and overlapping names are
removed without aliases. The rationale is to make static types describe
existing duck-typed runtime behavior, including direct Python/NumPy handoff,
without adding conversions, validation, casts, or nominal input gates merely
for typing.
