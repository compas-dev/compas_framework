# Title: What terminology should govern geometry discretization APIs?

## Status

Accepted

## Context

The objective requires consistent distinctions among sampling, discretization,
polygonization, tessellation, triangulation, refinement, remeshing, and
simplification. Current APIs mix related terms:
`Surface.compute_tessellation()` produces triangles,
`Mesh.to_vertices_and_faces(triangulated=True)` converts polygonal faces, and
`Mesh.quads_to_triangles()` mutates topology. These operations have different
inputs, guarantees, and mutation behavior.

Relevant existing code includes
`../compas/src/compas/geometry/surfaces/surface.py`,
`../compas/src/compas/datastructures/mesh/mesh.py`, and
`../compas/src/compas/geometry/trimesh/remeshing.py`.

## Options

1. Preserve current terminology independently in each subsystem. This avoids
   migration but perpetuates ambiguity across packages.
2. Use “tessellation” as an umbrella for every triangle-producing operation.
   This is simple but erases the distinction between approximating continuous
   geometry and partitioning existing polygonal domains.
3. Adopt the proposal's normative vocabulary. Sampling evaluates points;
   discretization is the broad umbrella for finite representations;
   polygonization discretizes a surface as connected polygonal faces;
   tessellation produces the canonical ephemeral triangular result;
   triangulation partitions existing discrete domains/faces; refinement,
   remeshing, and simplification describe changes to existing discretizations.

## Recommendation

Adopt option 3. Reserve resolution for counts, deflection for kernel-specific
approximation controls, quality for mesh targets, and tolerance for numerical
comparison and cleanup. Documentation must distinguish requested targets,
estimated errors, and guaranteed bounds.

The accepted operation terms are:

- **Discretization** is the broad category for representing continuous
  geometry with finite samples or connected elements.
- **Polygonization** is a surface discretization producing a persistent
  `PolygonalSurface` with connected polygonal faces.
- **Tessellation** is the canonical surface operation producing an ephemeral
  triangular `Tessellation`.
- **Triangulation** partitions existing discrete faces, domains, or point sets
  into triangles.

The operation-oriented `polygonize`/`tessellate` pair avoids mixing
`to_polygonal_surface` conversion naming with `to_tessellation` operation-result
naming. `to_mesh()` remains an explicit conversion of an existing discrete
representation into half-edge `Mesh`.

## Consequences

- New public names and docs gain a consistent semantic basis.
- Existing names that contradict the vocabulary are replaced rather than kept
  as permanent aliases. This is intentionally breaking.
- Tests must assert operation semantics, including mutation and vertex
  insertion, rather than only output face counts.
- All package documentation must use the same glossary.
- API docs must present `polygonize` and `tessellate` as operations and
  `to_mesh` as a representation conversion.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_gmsh`,
`compas_model`, and `compas_framework`.

## Dependencies

None.
