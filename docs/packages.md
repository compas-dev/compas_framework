# Package Matrix

The geometry-tessellation interfaces are a coordinated COMPAS 3 change. A
released package participating in these interfaces must require `compas>=3`;
mixing these releases with COMPAS 2 is unsupported.

| Package | Framework role | Geometry-tessellation release requirement |
| --- | --- | --- |
| `compas` | Core representations, strategies, operations, and plugin contracts | `>=3` |
| `compas_occ` | Open CASCADE geometry backend | `compas>=3`; provides `Deflection` BRep approximation |
| `compas_cgal` | CGAL algorithms and geometry processing | `compas>=3`; implements authoritative triangulation and selected triangle-processing plugins |
| `compas_libigl` | libigl algorithms and geometry processing | `compas>=3`; implements authoritative selected triangle-processing plugins |
| `compas_model` | Shared AEC model data structure | `compas>=3`; exposes geometry as `Tessellation` where triangle processing is required |
| `compas_framework` | Cross-package integration and release verification | `compas>=3`; verifies the synchronized package set |
| `compas_gmsh` | Gmsh meshing integration | No alignment change: Gmsh mesh generation is not continuous-geometry tessellation |
| `compas_viewer` | Interactive visualization | Consume coordinated COMPAS 3 geometry representations according to its declared dependency |
| `compas_shapeop` | ShapeOp constraint solving | No geometry-tessellation API role |
| `compas_session` | Session management for COMPAS workflows and tools | No geometry-tessellation API role |

Compatibility is established by the framework test suite and released as one
versioned dependency set.

The table intentionally does not predict package release numbers. Each package
may have a different next major version, but its dependency metadata must express
the same `compas>=3` baseline before coordinated publication.

## Geometry-tessellation release checklist

- [ ] Select and record the release version for every participating package.
- [ ] Require `compas>=3` consistently in project metadata, lock files, wheel
  tests, and documentation examples.
- [ ] Build artifacts for the same supported Python and platform matrix, including
  the OCC, CGAL, and libigl native dependencies.
- [ ] Verify public plugin entry points dispatch through core COMPAS APIs; do not
  document backend adapters as competing high-level APIs.
- [ ] Run the framework integration and roundtrip suites against the exact package
  versions selected for release.
- [ ] Run native-backend tests and record unavailable backends as explicit skips,
  not passes.
- [ ] Build each package's documentation and run its executable examples or static
  example checks.
- [ ] Verify the migration guide and changelogs use `polygonize`, `tessellate`,
  `triangulate`, refinement, and remeshing consistently.
- [ ] Confirm enriched tessellation provenance/error results remain deferred and
  are not advertised as implemented.
- [ ] Confirm `compas_gmsh` remains outside this API alignment; do not add a
  superficial tessellation-strategy mapping.
- [ ] Tag, publish, or merge only after explicit release approval.

## Optional host integrations

| Extra | Packages | Host |
| --- | --- | --- |
| `rhino` | `compas_rhino`, `compas_ghpython` | Rhino and Grasshopper |
| `blender` | `compas_blender` | Blender |
| `hosts` | All three host-integration packages | Rhino, Grasshopper, and Blender |
