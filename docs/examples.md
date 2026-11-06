# Framework Verification Guide

`compas_framework` is a metapackage: its main contract is the coordinated set
of packages recorded in its distribution metadata. This page routes maintainers
to checks owned by the framework and its packages. It is not an independent
executable example. Only the files named by the ordinary quality configuration
are currently Ruff-checked, Pyright-checked, or executed.

## Distribution metadata

[`tests/test_distribution_artifacts.py`](https://github.com/compas-dev/compas_framework/blob/main/tests/test_distribution_artifacts.py)
inspects the built wheel and source distribution without importing native
libraries. It verifies the coordinated runtime dependencies, supported Python
range, absence of development dependencies and removed host extras, and
required package files.

Run it only against artifacts built from the same checkout by setting
`COMPAS_FRAMEWORK_DIST_DIR` to their temporary output directory. The local
`uv run invoke build` command builds the current working tree rather than only
committed `HEAD` content.

## Core geometry conversions

Core COMPAS owns continuous-to-discrete conversion. The current public path is
`to_polygonal_surface()` or `to_tessellation()` with producer-specific,
keyword-only resolution controls where required. A `Box`, for example, uses
`Box.to_tessellation()` and needs no nominal strategy object or native backend.

See the version-matched [COMPAS geometry documentation](https://compas.dev/compas/latest/api/generated/compas.geometry.html)
and its checked examples for executable usage.

## Structural algorithm boundaries

Triangle-processing plugins accept the approved structural vertices/faces
boundary. They do not require callers to construct a `Tessellation` merely to
pass raw Python or NumPy buffers. Named planar Delaunay operations and aggregate
polygon triangulation callables replace nominal triangulation flags.

The owning package documentation provides executable direct-backend and public
plugin-dispatch examples:

- [COMPAS CGAL](https://compas.dev/compas_cgal/latest/)
- [COMPAS libigl](https://compas.dev/compas_libigl/latest/)
- [COMPAS OCC](https://compas.dev/compas_occ/latest/)

## Pending native integration fixtures

[`tests/test_native_geometry_backends.py`](https://github.com/compas-dev/compas_framework/blob/main/tests/test_native_geometry_backends.py)
and
[`tests/test_geometry_tessellation_integration.py`](https://github.com/compas-dev/compas_framework/blob/main/tests/test_geometry_tessellation_integration.py)
are pending geometry and typing candidate-integration fixtures. They are
outside the ordinary Ruff, Pyright, and runtime gates and are not authoritative
proof of the accepted target contracts.

They are not used as the candidate gate. The installed-artifact contracts in
`.github/candidates` exercise the approved current boundaries without source
checkout fallbacks. Until a reviewed live manifest and successful hosted run
exist, do not cite either fixture set as positive candidate evidence.
