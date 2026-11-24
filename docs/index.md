# COMPAS Framework

`compas_framework` is the integration and release package for the main COMPAS
framework. It provides a single installation target and owns cross-package
verification and release candidate evidence.

The distribution installs `compas`, `compas_occ`, `compas_cgal`,
`compas_libigl`, `compas_gmsh`, `compas_viewer`, `compas_model`,
`compas_shapeop`, and `compas_session`. It does not currently provide Rhino,
Grasshopper, or Blender extras because the published host packages do not yet
declare compatible COMPAS 3 dependencies.

See the [testing strategy](testing.md) for the verified scope and the
[package matrix](packages.md) for coverage by package. Implementation and
package-local examples live in their owning repositories.
