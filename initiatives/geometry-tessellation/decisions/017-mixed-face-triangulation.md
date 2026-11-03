# Title: How should mixed polygonal collections select face triangulation algorithms?

## Status

Accepted

## Context

`PolygonalSurface.triangulated`, `Mesh.triangulated`, `Mesh.triangulate`, and
`Polyhedron.triangulated` currently apply one leaf `TriangulationStrategy` to
every face.

`DiagonalSplit` passes triangles through and splits quadrilaterals, including
warped quadrilaterals, but rejects faces with five or more vertices.
`EarClipping` handles planar triangles, quadrilaterals, and n-gons, but rejects
all non-planar faces. A single strategy can therefore triangulate a planar
mixed collection only by using ear clipping everywhere; it cannot combine an
explicit quad diagonal policy with ear clipping for general polygons.

A non-planar n-gon does not define a unique continuous surface. Implicitly
projecting it and lifting triangle indices back to the original vertices would
choose an interpretation that the input did not specify. A warped quad is
different when a diagonal is explicitly selected: that diagonal defines one
of two possible piecewise-planar surfaces.

## Options

1. Continue applying one leaf strategy to all faces. This is simple but cannot
   express different quad and n-gon policies.
2. Accept an ordered list of strategies and try them until one succeeds. This
   conflates unsupported face arity with invalid geometry and may conceal a
   non-planarity error.
3. Accept a mapping keyed by face size. This is flexible but unnecessarily
   open-ended, difficult to validate, and awkward to serialize.
4. Introduce a serializable composite strategy with explicit quad and n-gon
   policies and deterministic dispatch by face arity.

## Recommendation

Choose option 4. Introduce:

```python
FaceTriangulation(
    quad=DiagonalSplit("shortest"),
    ngon=EarClipping(),
)
```

Dispatch by face arity:

- fewer than three vertices: raise `ValueError`;
- three vertices: pass through unchanged;
- four vertices: apply `quad`;
- five or more vertices: apply `ngon`.

Initially, `quad` accepts `DiagonalSplit` or `EarClipping`, and `ngon` accepts
`EarClipping`. Leaf strategies remain available for low-level single-face
triangulation, while collection-level operations require
`FaceTriangulation`.

The non-planar contract is explicit:

- triangles are accepted;
- `DiagonalSplit` accepts a warped quad because the chosen diagonal explicitly
  defines its piecewise-planar surface;
- `EarClipping` rejects a warped quad;
- `EarClipping` rejects every non-planar n-gon;
- no triangulation strategy performs implicit projection of non-planar faces.

Planarity initially uses the standard COMPAS tolerance. Strategy-specific
tolerance is deferred until required by a concrete use case. Correct the
low-level `earclip_polygon` documentation so it does not promise a best-fit
projection for non-planar input.

## Consequences

- Mixed triangles, quads, and n-gons can use the appropriate algorithms in one
  atomic collection operation.
- Quad diagonal choice remains explicit and serializable.
- Invalid non-planar polygons cannot be hidden by fallback dispatch.
- Collection operations must stage all face results before mutating a `Mesh`.
- Face winding and existing vertex indices remain unchanged; no vertices are
  inserted initially.
- `PolygonalSurface.triangulated` continues returning `Tessellation`; Mesh and
  Polyhedron return types remain unchanged.
- Existing collection callers using a leaf strategy must wrap their policies
  in `FaceTriangulation`; no compatibility alias is required under ADR 013.
- Tests must cover mixed topology, both quad diagonals, warped quad behavior,
  non-planar n-gon rejection, serialization, and atomic mutation failure.

## Affected packages

`compas`, plus downstream callers in `compas_cgal`, `compas_libigl`,
`compas_model`, and `compas_framework` if searches identify collection-level
leaf-strategy calls.

## Dependencies

- [003 — Strategy objects](003-strategy-objects.md)
- [007 — Triangulation operations](007-triangulation-operations.md),
  superseded in part if this decision is accepted
- [013 — Compatibility](013-compatibility.md)
