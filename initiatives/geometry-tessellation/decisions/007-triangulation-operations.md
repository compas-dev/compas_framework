# Title: What should the mutating and non-mutating triangulation APIs be?

## Status

Accepted

## Context

Current discrete triangulation policies differ. Non-mutating
`Mesh.to_vertices_and_faces(triangulated=True)` uses `(a, c)` for quads and a
centroid fan for n-gons. Mutating `Mesh.quads_to_triangles()` uses `(b, d)`.
`PolygonalSurface.triangles` uses Earcut for non-triangular faces. These
algorithms differ in mutation, diagonal, vertex insertion, and source-index
preservation.

## Options

1. Keep only conversion flags and the existing mutating special case. This
   preserves compatibility but does not provide a coherent operation model.
2. Make `triangulate()` non-mutating, following some geometry libraries. This
   conflicts with the common COMPAS pattern of past-tense non-mutating names.
3. Add mutating `triangulate(strategy=...)` and non-mutating
   `triangulated(strategy=...)`, with explicit strategies such as fixed
   diagonal, shortest diagonal, and Earcut.
4. Pick one universal triangulation algorithm. This would silently change
   established topology and performance.

## Recommendation

Choose option 3 with one strict convention: `triangulate(strategy)` mutates and
returns `None`, while `triangulated(strategy)` leaves the source unchanged and
returns `Tessellation`. Mutable topological types expose both; non-mutable types
expose only `triangulated`. Existing conversion flags and
`quads_to_triangles()` are removed rather than retained as parallel APIs.

Face triangulation strategies inherit `compas.data.Data` through a common
`TriangulationStrategy` base:

```python
class TriangulationStrategy(Data):
    pass


class DiagonalSplit(TriangulationStrategy):
    diagonal: Literal["shortest", "02", "13"] = "shortest"


class EarClipping(TriangulationStrategy):
    pass
```

`DiagonalSplit` accepts triangular and quadrilateral faces. Triangles pass
through unchanged. For quads, `"02"` and `"13"` select the corresponding
vertex-index diagonals. `"shortest"` compares geometric diagonal lengths and
uses `"02"` for an exact tie, making the result deterministic.

`EarClipping` accepts planar polygonal faces, preserves the input vertices, and
does not insert Steiner points. Invalid or nonplanar faces raise an error. It
uses the standard COMPAS tolerance for geometric comparisons; tolerance is not
a strategy field.

Mutation transfers source face attributes to generated faces. It does not
promise preservation of face keys. Vertex keys are preserved unless a strategy
explicitly permits vertex insertion; neither initial face strategy inserts
vertices.

## Consequences

- Mutation becomes explicit and consistent with COMPAS conventions.
- Existing implicit diagonal and centroid-fan defaults are not preserved as an
  API constraint; the selected strategy defines the behavior explicitly.
- Face attributes and provenance need defined transfer behavior for mutation.
- Generated mutable faces inherit source face attributes, while face-key
  preservation is explicitly not guaranteed. The initial strategies preserve
  vertex keys because neither inserts vertices.
- Tests must cover both explicit diagonals, shortest-diagonal ties, triangle
  pass-through, n-gons, planarity failures, standard tolerance behavior,
  attributes, key guarantees, source immutability, and invalid strategy/face
  combinations.
- Documentation must separate domain triangulation (Earcut/Delaunay) from
  topology-local face splitting.
- Existing callers of `triangulated=True`, `.triangles`, and
  `quads_to_triangles()` require source changes.

## Affected packages

`compas`, `compas_model`, and `compas_framework`; plugin packages consume the
resulting triangle representation.

## Dependencies

- [001 — Terminology](001-terminology.md)
- [002 — Mesh representations](002-mesh-representations.md)
- [005 — Output topology](005-output-topology.md)
