# Title: What structural type vocabulary should core and numerical packages share?

## Status

Proposed.

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
  names.
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

## Recommendation

Choose option 3.

### Naming rules

- A structural `Protocol` has a `Protocol` suffix.
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
| `FloatSequence` protocol | Make its structural role explicit. | `FloatSequenceProtocol` |
| `FloatSequenceType` | Use a neutral alias because current normalization functions may return the original zero-length input. | `FloatSequence` |
| `RawCoordinateType` | Remove; it is unused and narrower than the accepted contract. | None |
| `Coordinate` protocol | Make its structural role explicit. | `CoordinateProtocol` |
| `CoordinateType` | Remove the ambiguous union. | `CoordinateInput` for parameters; a concrete output type for results |
| `PointCoordinates` | Remove the duplicate sequence-only alias. | `CoordinateInput` at accepted boundaries; `tuple[float, float, float]` for a normalized XYZ result |
| `Coordinates` protocol | Make its structural role explicit. | `CoordinatesProtocol` |
| `CoordinatesType` | Remove the ambiguous union. | `CoordinatesInput` for parameters; a concrete output type for results |
| `Indices` protocol | Make its structural role explicit. | `IndicesProtocol` |
| `IndicesCollection` protocol | Make its structural role explicit. | `IndicesCollectionProtocol` |
| `CoordinatesCollection` protocol | Make its structural role explicit. | `CoordinatesCollectionProtocol` |
| `TriangleMeshInput` | Remove the directional and unenforced triangle name. | `VerticesFaces` |
| tuple-valued `MeshType` | Remove the name that conflicts with the actual `Mesh`. | `VerticesFaces` |
| `SphereType` | Rename the raw geometric tuple. | `SphereData` |
| `RayType` | Rename the raw geometric tuple. | `RayData` |
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
class CoordinateProtocol(Protocol): ...
class CoordinatesProtocol(Protocol): ...
class IndicesProtocol(Protocol): ...
class IndicesCollectionProtocol(Protocol): ...
class CoordinatesCollectionProtocol(Protocol): ...

type CoordinateInput = CoordinateProtocol | Sequence[RealInput] | NumericArray
type CoordinatesInput = CoordinatesProtocol | Sequence[CoordinateInput] | NumericArray
type IndicesInput = IndicesProtocol | Sequence[IntegralInput] | IntegerArray
type IndicesCollectionInput = (
    IndicesCollectionProtocol | Sequence[IndicesInput] | IntegerArray
)
type CoordinatesCollectionInput = (
    CoordinatesCollectionProtocol | Sequence[CoordinatesInput] | NumericArray
)

type VerticesFaces = tuple[CoordinatesInput, IndicesCollectionInput]
```

Explicit NumPy union members remain necessary: Pyright does not model a NumPy
array as satisfying the nested indexing protocols reliably. Protocols support
stable duck-typed consumers; they do not replace the array members.

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

### Core constructor matrix

The following owned constructors accept appropriate NumPy inputs because their
existing semantics copy or normalize the supplied values:

| Constructor | Accepted annotation | Ownership and normalization |
|---|---|---|
| `Point`, `Vector` constructor components and `x`/`y`/`z` setters | `RealInput` | Store Python `float` as already performed. |
| `Polyline`, `Polygon`, `Pointcloud` | `CoordinatesInput` | Copy coordinates into owned points. |
| `PolygonalSurface`, `Polyhedron` | `CoordinatesInput`, `IndicesCollectionInput` | Copy coordinates and normalize each non-boolean copied index through the integer-index protocol. |
| `PolygonalSurface.vertices` and `.faces` setters | `CoordinatesInput`, `IndicesCollectionInput` | Apply the same ownership and normalization contract as construction. |
| `Mesh.from_vertices_and_faces` | `CoordinatesInput`, `IndicesCollectionInput` | Preserve its existing broad copying contract. |
| `Tessellation` | its generic coordinate/index buffer bounds | Retain compatible buffers without copying, as already documented. |

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
types and must not redefine `VerticesFaces` or the accepted coordinate/index
families.

## Verification

- Static accepted/error fixtures for Python lists, tuples, custom structural
  objects, NumPy float32/float64 coordinates, and int32/int64 indices.
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

## Approval boundary

This decision is **Proposed**. The public `compas.typing` module, vocabulary
replacement, removal without aliases, constructor annotations, NumPy-integer
widening, and boolean-index rejection require explicit approval before package
source changes.
