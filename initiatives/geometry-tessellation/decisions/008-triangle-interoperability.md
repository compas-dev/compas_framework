# Title: How should heterogeneous geometry be adapted and validated as triangle meshes?

## Status

Accepted

## Context

Core `MeshType` is a raw tuple. CGAL and libigl mostly tuple-unpack and
independently coerce NumPy arrays; CGAL geodesics alone accepts `Mesh` through
a local helper. OCC's shell conversion accepts rich `Mesh` and checks
`is_trimesh()`. `Tessellation`, `PolygonalSurface`, and `Mesh` therefore have no
shared triangle-input boundary.

Native operations also require different topology guarantees: some need only
triangle arity, while volume or boolean operations may require closed,
oriented, manifold input.

## Options

1. Require raw `(V, F)` everywhere. This is fast and familiar but structurally
   weak and forces callers to repeat conversion.
2. Require rich `Mesh` everywhere. This gives topology but adds allocation and
   loses zero-copy native-buffer opportunities.
3. Use a runtime protocol over arbitrary triangle providers. This is extensible
   but makes the primary contract less concrete and pushes validation into
   every implementation.
4. Make `Tessellation` the sole public triangle-buffer contract. Continuous
   sources produce it with `tessellate(strategy)` and discrete polygonal
   sources with `triangulated(strategy)`. Do not add a universal conversion
   function or public accepted-input union. Keep raw tuples and NumPy arrays
   behind backend implementation boundaries.

## Recommendation

Choose option 4. Geometry-processing plugin APIs accept `Tessellation`, not a
public union of tuples and rich objects. Callers explicitly use
`tessellate(strategy)` or `triangulated(strategy)` before invoking a plugin;
there is no redundant `to_triangle_mesh()` facade. Core validates
`Tessellation` buffer shape, triangle arity, indices, and finiteness.
Closedness, manifoldness, and orientation remain explicit operation-specific
checks. NumPy dtype and contiguity remain backend-owned internals.

## Consequences

- Existing representations become interoperable through one canonical result
  type and semantically explicit producer operations.
- Already compatible `Tessellation` buffers can retain zero-copy behavior.
- Polygonal inputs may allocate, triangulate, or add vertices; this must be
  documented.
- Public raw tuple inputs are removed from CGAL/libigl high-level operations;
  their internal bindings may still use arrays and tuples.
- CGAL/libigl consolidate repeated conversion while keeping native dtype
  choices local.
- Tests must cover copies/identity, invalid buffers, topology layers, source
  immutability, and cross-representation equivalence.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, and
`compas_framework`.

## Dependencies

- [002 — Mesh representations](002-mesh-representations.md)
- [005 — Output topology](005-output-topology.md)
- [006 — Tessellation API](006-tessellation-api.md)
- [007 — Triangulation operations](007-triangulation-operations.md)
