# Title: What lightweight triangle representation should COMPAS standardize on?

## Status

Accepted

## Context

Core already assigns different roles to three representations:

- `Tessellation` is an ephemeral, zero-copy-oriented indexed-triangle result
  (`../compas/src/compas/geometry/tessellation.py`).
- `PolygonalSurface` is a serializable lightweight polygon buffer
  (`../compas/src/compas/geometry/polygonal_surface.py`).
- `Mesh` is a serializable mutable half-edge datastructure
  (`../compas/src/compas/datastructures/mesh/mesh.py`).

`Mesh.is_trimesh()` and `Mesh.is_quadmesh()` classify existing topology. No
dedicated `TriangleSurface`, `TriangleMesh`, `QuadMesh`, or
`TessellationResult` type currently exists. The distinct `Tessellation` name
communicates that the object is an ephemeral operation result. It avoids
implying the persistent surface semantics of `PolygonalSurface` or the editable
half-edge topology and serialization contract of `Mesh`.

## Options

1. Add persistent `TriangleMesh` and `QuadMesh` siblings/subclasses of `Mesh`.
   Face arity becomes explicit, but topology, attributes, serialization, keys,
   and algorithms are duplicated or tightly coupled.
2. Add `TriangleSurface` or a compact `TriangleMesh` beside `Tessellation`.
   This may sound specific but creates two nearly identical triangle-buffer
   containers and risks confusion with `PolygonalSurface` or `Mesh`.
3. Replace/rename `Tessellation` as `TriangleMesh`. This aligns the name with
   plugin terminology but wrongly suggests a persistent or topological mesh
   and loses the useful operation-result distinction.
4. Preserve `Tessellation` as the sole ephemeral indexed-triangle result while
   retaining `PolygonalSurface` and `Mesh` in their distinct persistent roles.

## Recommendation

Choose option 4. Retain `Tessellation` as the canonical ephemeral triangle
representation and operation result. Its distinct name is intentional: it
does not imply serialization, persistent surface identity, editable half-edge
topology, or mesh keys/attributes. Preserve its zero-copy vertex/triangle and
same-index attribute semantics. Keep `PolygonalSurface` for persistent polygon
buffers and `Mesh` for rich topology. Do not add `TriangleSurface`,
`TriangleMesh`, `QuadMesh`, or universal `TessellationResult` containers.

## Consequences

- `Tessellation` remains the public zero-copy-oriented ephemeral result.
- Ephemeral triangle buffers, persistent polygon storage, and rich topology
  remain visibly distinct in both naming and behavior.
- Triangle/quad requirements are enforced at conversion or operation
  boundaries rather than by nominal class identity.
- Plugins use `Tessellation` directly rather than depending on a hierarchy.
- Documentation must clearly explain which representation to use.
- Tests must cover representation equivalence and conversion independence.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_model`, and
`compas_framework`.

## Dependencies

- [001 — Terminology](001-terminology.md)
