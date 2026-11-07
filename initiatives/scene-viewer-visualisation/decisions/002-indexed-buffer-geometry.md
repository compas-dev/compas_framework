# ADR 002: Indexed Viewer Buffer Geometry

## Status

Accepted.

## Context

Viewer can batch geometry efficiently but its general `BufferGeometry`
requires expanded line and triangle vertices. This duplicates arrays and makes
callers manually expand vertices plus edges or triangles. Core numerical APIs
already accept structural Python and NumPy buffers, and Viewer-specific GPU
layout should not become a compulsory core geometry representation.

## Options

1. Add one Viewer-owned shared-vertex indexed `BufferGeometry` contract and
   convenience constructors.
2. Put a GPU-oriented buffer type in core.
3. Require `Tessellation`, `PolygonalSurface`, or `Mesh` for every input.
4. Preserve expanded arrays and add only helper functions that duplicate them.

## Recommendation

Choose option 1. Use shared `vertices` plus optional point, edge, and triangle
index channels. Provide:

```python
BufferGeometry.from_points(vertices)
BufferGeometry.from_vertices_and_edges(vertices, edges)
BufferGeometry.from_vertices_and_triangles(vertices, triangles)
```

Accept structural Python sequences and NumPy arrays. Normalize once to Viewer
dtypes and check rank, column count, and index bounds. Preserve indices through
the buffer manager and do not create one scene object per primitive.

Keep styling on scene objects. Do not add a universal render geometry to core
or make this contract an input to geometry algorithms.

## Consequences

- Large edge and triangle datasets avoid Python-object and vertex-expansion
  overhead.
- Viewer adapters gain one common path for indexed geometry.
- Geometry with independent point/line/triangle vertex pools must combine
  them into one vertex table with offset indices at the Viewer boundary.
- Per-channel or per-primitive color arrays beyond current behavior require
  evidence and a separate refinement rather than speculative fields.

## Compatibility

The existing expanded `points`, `lines`, and `faces` constructor is replaced
in a coordinated Viewer change. Examples and adapters migrate together; no
parallel deprecated constructor is proposed.

## Verification

- Test list and NumPy inputs, exact shapes/dtypes, bounds, empty channels, and
  input non-mutation.
- Assert indices remain indexed in CPU/GPU assembly.
- Exercise large input without per-edge or per-triangle scene objects.
- Compare rendering semantics with current points, lines, and faces.

## Affected packages

`compas_viewer`, `compas_model`, and `compas_framework`.

## Dependencies

- [ADR 001](001-ownership-boundaries.md)
- Accepted structural numerical-input decisions from typing alignment
