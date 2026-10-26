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

Host integrations are available as extras:

```bash
pip install "compas_framework[rhino]"
pip install "compas_framework[blender]"
pip install "compas_framework[hosts]"
```

Python 3.12 or newer is required. Some geometry backends have native
dependencies and may be easier to install through conda-forge.

## Documentation

For more information, check out the online documentation here: [COMPAS Framework docs](https://compas.dev/compas_framework)

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/compas-dev/compas_framework/issues).
