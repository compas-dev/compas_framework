# Title: Should `Mesh.triangulated()` preserve the mesh representation?

## Status

Proposed.

## Context

Accepted ADR 007 and Typing ADR 015 currently make every aggregate
`triangulated(...)` operation return an ephemeral `Tessellation`. The user has
provided new evidence that this is wrong for `Mesh`: COMPAS mutating and
past-tense non-mutating pairs normally preserve the owning type, and converting
a rich half-edge datastructure to `Tessellation` discards its concrete class,
keys, attributes, defaults, and editable topology.

This issue is specific to `Mesh`. `Polygon`, `PolygonalSurface`, `Polyhedron`,
and `PlanarRegion` do not have the same paired rich-topology mutation contract.

## Options

1. Keep `Mesh.triangulated(...) -> Tessellation` for uniform aggregate results.
2. Make `Mesh.triangulated(...) -> Self` while leaving the other aggregate
   results unchanged.
3. Change every aggregate to return its own representation.
4. Add `TriangleMesh`, `Mesh.to_tessellation`, or another parallel conversion
   API.

## Recommendation

Choose option 2:

```python
def triangulate(
    self,
    triangulator: Triangulator | None = None,
) -> None: ...

def triangulated(
    self,
    triangulator: Triangulator | None = None,
) -> Self: ...
```

The non-mutating method is semantically equivalent to:

```python
result = self.copy()
result.triangulate(triangulator)
return result
```

An omitted triangulator and explicit `None` both use
`triangulate_polygon`. A supplied duck-typed callable is the only customization
path. Algorithm-specific arguments remain bound with tools such as
`functools.partial`.

Keep these existing return contracts:

```python
Polygon.triangulated(...) -> Tessellation
PolygonalSurface.triangulated(...) -> Tessellation
Polyhedron.triangulated(...) -> Tessellation
PlanarRegion.triangulated() -> Tessellation
```

Do not add `TriangleMesh`, `QuadMesh`, `Mesh.to_tessellation`,
`to_vertices_and_triangles`, or another alias. Triangle arity remains a
predicate on an ordinary `Mesh`.

## Preservation contract

The returned mesh:

- has the same concrete type, expressed by `Self`;
- is independent from the source and follows standard `Data.copy()` identity
  semantics, including a new GUID;
- preserves mesh attributes and default vertex, edge, and face attributes;
- preserves vertex keys and vertex attributes;
- preserves attributes on pre-existing edges, while new diagonals receive
  defaults;
- preserves existing triangular faces, including their keys and attributes;
- replaces each non-triangular face with triangles inheriting that face's
  attributes;
- makes no promise about keys or iteration order of generated faces;
- satisfies `is_trimesh()`; and
- leaves the source unchanged.

The mutating method applies the same topology and attribute rules in place,
returns `None`, and stages and validates every replacement before modifying the
mesh. It does not invoke the custom triangulator for already-triangular faces.

## Structural consumer path

Numerical consumers explicitly extract the accepted structural boundary:

```python
triangle_mesh = mesh.triangulated()
vertices, triangles = triangle_mesh.to_vertices_and_faces()
```

When an actual ephemeral representation is required, construction remains
explicit:

```python
tessellation = Tessellation(vertices=vertices, triangles=triangles)
```

No implicit conversion is introduced.

## Consequences

- The past-tense Mesh operation preserves the information that defines a
  Mesh.
- Raw numerical backends continue to accept structural buffers directly.
- Existing consumers expecting a `Tessellation` must extract vertices/faces or
  explicitly construct one.
- The other aggregate return contracts remain stable and require independent
  evidence before any later change.

## Superseded clauses if accepted

- ADR 007's universal `triangulated(...) -> Tessellation` clause is superseded
  for `Mesh` only.
- ADR 022's discrete-geometry paragraph is clarified so `Mesh.triangulated`
  is representation-preserving while the other accepted aggregate results
  remain `Tessellation`.
- Typing ADR 015's shared aggregate return signature is split into the `Mesh`
  signature above and the unchanged signatures for the other aggregates.
- ADR 002 remains authoritative that `Tessellation` is the sole ephemeral
  indexed-triangle representation; not every operation producing triangle
  topology must return it.

## Verification

- Verify `Self` typing and preservation of a concrete Mesh subclass.
- Verify source independence, new identity, and source immutability.
- Verify omitted/`None` equivalence, arbitrary callables, and
  `functools.partial`.
- Verify existing triangle keys, split-face attribute inheritance, mesh and
  default attributes, vertex data, source-edge data, and new diagonal defaults.
- Verify atomic failure for invalid callback output.
- Verify raw tuple extraction and explicit `Tessellation` construction.
- Verify unchanged `Tessellation` returns for the other aggregates.
- Migrate and test glTF, volume, CGAL, libigl, model, examples, typing fixtures,
  and documentation.

## Affected packages

`compas`, `compas_cgal`, `compas_libigl`, `compas_model`, and
`compas_framework`. No current OCC or viewer call site requires a source
change, but integration tests must protect the unchanged aggregate contracts.

## Dependencies

- [002 — Mesh representations](002-mesh-representations.md)
- [007 — Triangulation operations](007-triangulation-operations.md)
- [022 — Operation concepts and conversion boundaries](022-operation-terminology-and-producer-boundaries.md)
- Typing ADR 015 — exact triangulation and discretization APIs
