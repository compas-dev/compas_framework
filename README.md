# COMPAS Framework

The integration and release package for the main COMPAS framework packages:
`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_gmsh`,
`compas_viewer`, `compas_model`, `compas_shapeop`, and `compas_session`.

This repository owns the metapackage, cross-package verification, and release
candidate evidence. Individual package APIs and examples live in their owning
repositories.

## Installation

```bash
pip install compas_framework
```

The metapackage targets Python 3.12, 3.13, and 3.14. Complete runtime
installation across the target matrix still needs hosted verification. Some
geometry backends also require native libraries. See the
[package matrix](docs/packages.md) for current verification coverage.

The COMPAS 3 metapackage does not currently provide Rhino, Grasshopper, or
Blender extras. Those bundles will return after their owning packages declare
and verify COMPAS 3 compatibility. Existing COMPAS 2 host integrations remain
available through their package-specific installation instructions, but they
must not be mixed with this COMPAS 3 metapackage.

## Development

Development tooling is locked separately from the framework runtime packages.
Create a pure tool environment without installing native backends:

```bash
uv sync --locked --only-group dev --no-install-project
uv run --no-sync invoke check typecheck test docs
```

The lock records the complete published project metadata. Its package sources
are tooling-resolution pins and are separate from the native-integration
candidate manifest. `--only-group dev --no-install-project` installs only
repository tools; it does not install `compas_occ`, `compas_cgal`,
`compas_libigl`, or the other framework runtime packages.

The COMPAS Hub tracks cross-package initiative plans and handoffs. In the
local COMPAS workspace, start at `Hub/initiatives/README.md`.

## Documentation

For more information, see the [COMPAS Framework documentation](https://compas.dev/compas_framework).

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/compas-dev/compas_framework/issues).
