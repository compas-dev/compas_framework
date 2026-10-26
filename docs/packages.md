# Package Matrix

| Package | Framework role |
| --- | --- |
| `compas` | Core data structures, geometry, plugins, and serialization |
| `compas_occ` | Open CASCADE geometry backend |
| `compas_cgal` | CGAL algorithms and geometry processing |
| `compas_libigl` | libigl algorithms and geometry processing |
| `compas_gmsh` | Gmsh meshing integration |
| `compas_viewer` | Interactive visualization |
| `compas_model` | Shared AEC model data structure |
| `compas_shapeop` | ShapeOp constraint solving |
| `compas_session` | Session management for COMPAS workflows and tools |

Compatibility is established by the framework test suite and released as one
versioned dependency set.

## Optional host integrations

| Extra | Packages | Host |
| --- | --- | --- |
| `rhino` | `compas_rhino`, `compas_ghpython` | Rhino and Grasshopper |
| `blender` | `compas_blender` | Blender |
| `hosts` | All three host-integration packages | Rhino, Grasshopper, and Blender |
