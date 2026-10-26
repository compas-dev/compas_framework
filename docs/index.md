# COMPAS Framework

`compas_framework` is the integration and release package for the main COMPAS
framework. It provides one tested installation target and a home for workflows
that cross package boundaries.

The distribution installs `compas`, `compas_occ`, `compas_cgal`,
`compas_libigl`, `compas_gmsh`, `compas_viewer`, `compas_model`,
`compas_shapeop`, and `compas_session`. Rhino, Grasshopper, and Blender
integrations are available as optional extras.

This repository focuses on framework-level plugin discovery, data roundtrips,
performance checks, examples, and documentation. Implementations owned by one
package remain in that package's repository.
