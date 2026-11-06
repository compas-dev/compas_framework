# COMPAS Framework

The integration and release package for the main COMPAS framework packages:
`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_gmsh`,
`compas_viewer`, `compas_model`, `compas_shapeop`, and `compas_session`.

In addition to providing one installation target, this repository hosts
full-framework tests, data roundtrips, performance checks, examples, and
documentation.

## Installation

```bash
pip install compas_framework
```

Python 3.12, 3.13, and 3.14 are supported. Some geometry backends have native
dependencies and may be easier to install through conda-forge.

The COMPAS 3 metapackage does not currently provide Rhino, Grasshopper, or
Blender extras. Those bundles will return after their owning packages declare
and verify COMPAS 3 compatibility. Existing COMPAS 2 host integrations remain
available through their package-specific installation instructions, but they
must not be mixed with this COMPAS 3 metapackage.

## Development

Development tooling is locked separately from the framework runtime packages.
Create a pure tool environment without installing native backends:

```bash
uv sync --frozen --only-group dev --no-install-project
uv run invoke check
uv run invoke typecheck
uv run invoke test
uv run invoke docs
```

The lock records the complete published project metadata. Its package sources
are tooling-resolution pins and are separate from the native-integration
candidate manifest. `--only-group dev --no-install-project` installs only
repository tools; it does not install `compas_occ`, `compas_cgal`,
`compas_libigl`, or the other framework runtime packages.

## Documentation

For more information, see the [COMPAS Framework documentation](https://compas.dev/compas_framework).

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/compas-dev/compas_framework/issues).
