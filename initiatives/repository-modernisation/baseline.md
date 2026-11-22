# Repository Modernisation Phase 0 Baseline

## Status

Complete on 2026-11-03. Rollback commits and exact Phase 1 debt manifests are
recorded. The dirty `compas_framework` and `compas_session` worktrees have
explicit preservation gates because commits cannot restore their dirty or
untracked user content. This report does not claim that unavailable checks
passed and it does not authorize publishing, deployment, repository-setting
changes, or merges.

## Method

The ten initial repositories were inspected in parallel without installing or
updating dependencies and without editing their worktrees. Checks used the
`compas3` environment and its Python interpreter where feasible:

```text
/Users/vanmelet/miniforge3/envs/compas3/bin/python
```

The observed interpreter was Python 3.12.13. Commands were directed to
temporary output locations when supported. Builds or documentation commands
that necessarily wrote generated files into a repository were not run. Network
inventory and isolated-build failures caused by the restricted audit
environment are reported as environmental limitations, not package failures.

For a clean repository, the recorded commit is the rollback point for
subsequent migration work. A commit is not a complete rollback point for a
dirty repository because it cannot restore modified, deleted, ignored, or
untracked user content. That state is user-owned and must be reconciled or
preserved through a recoverable, owner-approved mechanism before edits begin.

The measured checks can be reproduced from each repository with the `compas3`
interpreter. Commands use the applicable subset of:

```text
python -m pytest -p no:cacheprovider -q
python -m ruff check --no-cache .
python -m ruff format --check --no-cache .
python -m pyright --pythonpath /Users/vanmelet/miniforge3/envs/compas3/bin/python
python -m mkdocs build --strict --site-dir <temporary-directory>
```

OCC's source-only typing capture adds `--outputjson src/compas_occ`. Commands
must be invoked through the explicit `compas3` interpreter path recorded above;
the shortened `python` form is shown only for readability.

## Repository and rollback inventory

| Repository | Profile | Branch | Rollback commit | Worktree |
|---|---|---|---|---|
| `compas` | Pure Python | `remove-future` | `8d2becec9efe92a4d106d9802eeb1bb05812984f` | Clean |
| `compas_occ` | External-runtime hybrid | `c3-upgrade` | `e8ca13092f0768b7ed10d0befda26068b62f77e2` | Clean |
| `compas_cgal` | Native wheel | `c3-upgrade` | `ab7f96acc5011d6758a455c012523b0ab8b54da0` | Clean |
| `compas_framework` | Pure Python plus coordinated native integration | `initiative/geometry-tessellation` | `552929cb7e2b47be9076110334f89bb74e127f1e` (tracked base only; incomplete rollback point) | Dirty before audit; preservation gate required |
| `compas_gmsh` | External-runtime hybrid | `main` | `c16725f12930659e85849640d912717bd0fe9475` | Clean |
| `compas_libigl` | Native wheel | `c3-upgrade` | `70acf990bc0015fc2b27abeae28f9e50f68e4561` | Clean |
| `compas_model` | External-runtime hybrid | `c3-upgrade` | `fdb37df8ee343bbaea5f6420d987e8a4ea468ed3` | Clean |
| `compas_session` | Pure Python | `main` | `4668a20b3820277cd6ba9f7a523c84cf6177acaf` (tracked base only; incomplete rollback point) | Dirty before audit; preservation gate required for untracked `src/compas_session/workflow.py` |
| `compas_shapeop` | Native wheel | `main` | `9f575799747d79348b2661917628408fa84acd09` | Clean; ignored local native source exists |
| `compas_viewer` | Pure Python with Qt/OpenGL/headless extension | `c3-upgrade` | `ff1c81f37b7233c783a5e44f87adf4e8ca583f2a` | Clean |

## Measured quality baseline

Results below are exact observations from this audit. A dash means the check
was unavailable or not run, not that it passed.

| Repository | Tests | Ruff check | Ruff format | Pyright | Strict docs | Build/artifact | Native import |
|---|---|---|---|---|---|---|---|
| `compas` | 2009 passed, 30 failed because installed OCC/CGAL plugins invalidate missing-plugin assumptions | Pass | `src`, tests, and tasks pass; full repository has 17 files to format | 0 errors | Blocked by remote inventory fetch | Not run read-only | N/A |
| `compas_occ` | 95 passed | Pass | focused scope passes; full repository has 37 files to format | 62 errors | Network blocked plus 11 real warnings | Not run read-only | Pass |
| `compas_cgal` | 129 passed, 6 failed | 1 unused import | 30 files to format | 258 errors; environment/import configuration is not authoritative | Blocked by remote inventories | Not run read-only | Pass for sampled ABI3 modules |
| `compas_framework` | 23 passed | Pass | Pass, 85 files checked | 0 errors | Pass | no-isolation sdist/wheel and Twine checks pass; isolated build blocked by DNS | Integration environment present |
| `compas_gmsh` | 1 dummy test passed with source paths; does not exercise Gmsh | Pass | 1 file to format | 10 errors | 4 real Griffe warnings plus 2 network inventory failures | No current artifacts | Gmsh unavailable |
| `compas_libigl` | 41 passed | Pass | Pass, 54 files checked | 215 errors; no authoritative configured scope | Sphinx write requirement blocked read-only audit | Not run read-only | Pass for sampled ABI3 modules |
| `compas_model` | 363 passed, 11 failed, 11 errors | 32 errors | Pass, 166 files checked | 114 errors; no authoritative configured scope | Fails on stale `interactiongraph` reference | Unverified; isolated build blocked by DNS and no-isolation build needed repository writes | Existing environment exercised optional backends, but isolation unverified |
| `compas_session` | 6 passed, 6 sandbox-write failures with `PYTHONPATH=src` | Pass | Pass, 18 files checked | 69 broad-scope errors; no authoritative configured scope | Sphinx write requirement blocked read-only audit | No artifact evidence | N/A |
| `compas_shapeop` | Collection blocked: native extension unavailable | 6 import-order errors | Pass, 22 files checked | 51 errors, 11 warnings; scope includes ignored native sources | Sphinx write requirement blocked read-only audit | No local artifacts | Fail: extension not built/installed |
| `compas_viewer` | 95 passed, 1 failed | Pass | 40 Markdown files to format | 19 errors | Pass | Existing wheel is stale and not evidence for current commit | Qt/OpenGL provisioning not isolated |

## Repository migration surfaces and gates

### `compas`

The Phase 1 manifest is:

- `pyproject.toml`
- new `uv.lock`
- `tasks.py`
- `mkdocs.yml`
- `docs/background/setup.md`
- `docs/background/workflow.md`
- `docs/background/documentation.md`
- `.github/workflows/build.yml`
- `.github/workflows/coverage.yml`
- `.github/workflows/docs.yml`
- `.github/workflows/pr-checks.yml`
- `.github/workflows/prepare-release.yml`
- `.github/workflows/release.yml`
- `.gitignore` only if the accepted lock/build-output policy requires it
- focused test/configuration files needed to isolate pure-core tests from
  installed plugin discovery

The exact Ruff-format debt is:

- `docs/assets/examples/_plotter.py`
- `docs/assets/examples/basics.datastructures.cellnetworks.py`
- `docs/assets/examples/colors_saturation.py`
- `docs/background/code.md`
- `docs/background/dtypes.md`
- `docs/examples/color-maps.md`
- `docs/examples/point-in-box.md`
- `docs/examples/quadmesh-planarisation.md`
- `docs/getting-started/advanced.hashtree.md`
- `docs/getting-started/advanced.serialisation.md`
- `docs/getting-started/basics.colors.md`
- `docs/getting-started/basics.datastructures.cellnetwork.md`
- `docs/getting-started/basics.datastructures.meshes.md`
- `docs/getting-started/basics.datastructures.trees.md`
- `docs/getting-started/basics.datastructures.volmeshes.md`
- `docs/getting-started/basics.visualisation.md`
- `docs/getting-started/first-steps.md`

All 30 contaminated failures are in
`tests/compas/geometry/test_incomplete_geometry_apis.py`. Relevant core dispatch
paths are `src/compas/plugins.py` and `src/compas/geometry/brep/brep.py`; the
installed providers that expose the isolation problem are the sibling paths
`compas_occ/src/compas_occ/plugins/brep.py`,
`compas_occ/src/compas_occ/brep/brep.py`, and
`compas_cgal/src/compas_cgal/plugins/triangulation.py`. The sibling files are
evidence, not `compas` ownership. The main gates are a committed lock, direct
commands, immutable action pins, strict documentation without suppressed
warnings, and a clean core test environment.

### `compas_occ`

The Phase 1 manifest is:

- `pyproject.toml`
- new `uv.lock`
- `environment.yml`
- `tasks.py`
- `mkdocs.yml`
- `docs/installation.md`
- contributor/developer command documentation to be created or updated at the
  repository's established documentation location
- `.github/workflows/build.yml`
- `.github/workflows/docs.yml`
- `.github/workflows/pr-checks.yml`
- `.github/workflows/release.yml`
- artifact-install and native-import smoke tests to be added under `tests/`

The exact Pyright debt surface is:

- `src/compas_occ/brep/brepedge.py`
- `src/compas_occ/brep/brepface.py`
- `src/compas_occ/brep/breploop.py`
- `src/compas_occ/brep/brepvertex.py`
- `src/compas_occ/conversions/meshes.py`
- `src/compas_occ/geometry/curves/curve.py`
- `src/compas_occ/geometry/curves/curve2d.py`
- `src/compas_occ/geometry/curves/nurbs.py`
- `src/compas_occ/geometry/surfaces/__temp/extrusion.py`
- `src/compas_occ/geometry/surfaces/__temp/revolution.py`
- `src/compas_occ/geometry/surfaces/nurbs.py`
- `src/compas_occ/geometry/surfaces/surface.py`

Strict-doc warnings originate in `src/compas_occ/brep/brepface.py`,
`src/compas_occ/geometry/surfaces/nurbs.py`, and
`src/compas_occ/conversions/geometry.py`; they surface through
`docs/api/compas_occ.conversions.md`. Inventory configuration is in
`mkdocs.yml`.

The exact formatting debt is `docs/tutorial.md`; the ten Markdown files under
`docs/examples/breps/` named `brep_explorer`, `brep_fillet`,
`brep_from_booleans`, `brep_from_mesh`, `brep_overlap`, `brep_slice`,
`brep_split`, `brep_trim`, `brep_with_hole`, and `brep_with_holes`; the thirteen
files under `docs/examples/curves/` named `curve_closest_parameters_curve`,
`curve_closest_point`, `curve_comparison1`, `curve_comparison2`, `curve_divide`,
`curve_from_circle`, `curve_from_ellipse`, `curve_from_interpolation`,
`curve_from_line`, `curve_from_parameters`, `curve_from_points`,
`curve_joining`, and `curve_segmentation`; and the thirteen files under
`docs/examples/surfaces/` named `__temp/surface_from_extrusion-1`,
`__temp/surface_from_extrusion-2`, `surface_aabb`, `surface_frames`,
`surface_from_fill`, `surface_from_meshgrid`, `surface_from_parameters`,
`surface_from_points`, `surface_intersections_with_line`, `surface_isocurves`,
`surface_jsondata`, `surface_random`, and `surface_spacepoints`, all with the
`.md` suffix. Python metadata, Ruff, Conda, and CI matrices must agree. The
minimal Conda layer must continue to provide PythonOCC explicitly.

### `compas_cgal`

The Phase 1 manifest is:

- `pyproject.toml`
- `uv.lock`
- `pixi.lock`
- `environment.yml`
- `requirements.txt`
- `requirements-dev.txt`
- `requirements-docs.txt`
- `requirements-viz.txt`
- `tasks.py`
- `CMakeLists.txt`
- `mkdocs.yml`
- `.github/workflows/build.yml`
- `.github/workflows/docs.yml`
- `.github/workflows/pr-checks.yml`
- `.github/workflows/release.yml`
- contributor, build, and release documentation at their existing repository
  locations

The test debt is in `tests/test_straight_skeleton_2_extrude.py`,
`src/compas_cgal/straight_skeleton_2.py`, and `tests/test_subdivision.py`. The
Ruff error is in `docs/examples/example_meshing.py`.

The exact Pyright surface comprises these stubs under `src/compas_cgal/`:
`_booleans.pyi`, `_geodesics.pyi`, `_intersections.pyi`, `_isolines.pyi`,
`_measure.pyi`, `_meshing.pyi`, `_polylines.pyi`, `_reconstruction.pyi`,
`_skeletonization.pyi`, `_slicer.pyi`, `_straight_skeleton_2.pyi`,
`_subdivision.pyi`, `_triangulation.pyi`, and `_types_std.pyi`; these wrappers:
`_tessellation.py`, `booleans.py`, `geodesics.py`, `intersections.py`,
`isolines.py`, `measure.py`, `meshing.py`, `polylines.py`, `projection.py`,
`reconstruction.py`, `skeletonization.py`, `slicer.py`,
`straight_skeleton_2.py`, `subdivision.py`, `triangulation.py`, and `types.py`;
and `plugins/booleans.py`, `plugins/intersections.py`, `plugins/mesh.py`,
`plugins/triangulation.py`, and `plugins/trimesh.py`.

The exact formatting debt is `docs/devguide/contribute.md`,
`docs/devguide/types.md`, and the Markdown files under `docs/examples/` named
`example_boolean_difference_mesh_meshes`, `example_booleans`,
`example_booleans_with_edges`, `example_booleans_with_face_source`,
`example_geodesics`, `example_geodesics_exact`, `example_intersections`,
`example_isolines`, `example_measure`, `example_meshing`,
`example_meshing_dual`, `example_projection`,
`example_reconstruction_pointset_normal_estimation`,
`example_reconstruction_pointset_outlier_removal`,
`example_reconstruction_pointset_reduction`,
`example_reconstruction_pointset_smoothing`,
`example_reconstruction_poisson_surface_reconstruction`,
`example_simplify_polylines`, `example_skeletonization`,
`example_skeletonization_with_mapping`, `example_slicer`,
`example_straight_skeleton_2_extrude`,
`example_straight_skeleton_2_interior_straight_skeleton`,
`example_straight_skeleton_2_interior_straight_skeleton_offset_polygon`,
`example_straight_skeleton_2_interior_straight_skeleton_weighted_offset_polygon`,
`example_straight_skeleton_2_interior_straight_skeleton_with_holes`,
`example_subdivision`, and `example_triangulation`, all with the `.md` suffix.
Documentation inventories are configured in `mkdocs.yml` lines 83–108 and
`requirements-docs.txt`. Competing dependency paths must be reduced to one
authoritative Python path plus visible native provisioning. CGAL, Boost, and
Eigen downloads need integrity verification. Current test, lint, typing,
formatting, and artifact gates are not green.

### `compas_framework`

Migration files are `pyproject.toml`, a new `uv.lock`, `environment.yml`,
`tasks.py`, the build/docs/PR/release workflows, and contributor, testing, and
package documentation. Ordinary pure checks must be separated from an
explicitly provisioned exact-candidate-artifact integration job. Python
metadata and both CI matrices must be reconciled. Existing user-owned worktree
changes must be preserved. The exact pre-existing dirty paths are:

- deleted `.agents/skills/update-docstrings/SKILL.md`
- deleted `.agents/skills/update-type-hints/SKILL.md`
- modified `AGENTS.md`
- untracked `.codex/`
- untracked `initiatives/repository-modernisation/`
- untracked `initiatives/typing-alignment/`

Before any edits in this repository, the owner must choose and verify a
recoverable preservation/reconciliation method for all of these paths. The
tracked commit alone is not an adequate rollback point. This report records
path names and status only; it deliberately does not copy user content.

### `compas_gmsh`

Migration files are `pyproject.toml`, a new `uv.lock`, `tasks.py`,
`environment-linux.yml`, `mkdocs.yml` and omitted pages, all four workflows,
`tests/test_dummy.py`, new runtime tests, and typing corrections in the CSG,
model, and options modules. The primary gate is meaningful Gmsh runtime
coverage and an evidence-based Python/platform matrix; the dummy test cannot
support a migration claim.

### `compas_libigl`

Migration files are `pyproject.toml`, a new `uv.lock`, `environment.yml`,
`requirements-dev.txt`, `tasks.py`, `CMakeLists.txt`, the full Sphinx-to-MkDocs
documentation conversion, all four workflows, contributor/build/release
documentation, and typing-marker/stub and artifact-verification work. The
mutable libigl `main` dependency is a blocking reproducibility defect and must
be replaced by a reviewed immutable revision.

### `compas_model`

Migration files are `pyproject.toml`, a new `uv.lock`, `environment.yml`,
`tasks.py`, `mkdocs.yml`, the stale interactiongraph reference, contributor and
testing documentation, all four workflows, the PR template, duplicate/debt
tests, viewer fixtures, and production typing-contract files. Coal, OCC, and
Viewer jobs must remain explicit. Existing test, Ruff, Pyright, strict-doc, and
artifact-build debt must be resolved before the gates become blocking.

### `compas_session`

Migration files are `pyproject.toml`, both requirements files, a new `uv.lock`,
`tasks.py`, all four workflows, the Sphinx/RST documentation tree, a new
`mkdocs.yml`, README/contributor instructions, and possibly `.gitignore`.
The untracked `src/compas_session/workflow.py` must be reconciled with its owner
before edits. A recoverable, owner-approved preservation point for that file is
required because the tracked commit cannot restore it. Tests need a writable
temporary-path contract rather than writing under the repository.

### `compas_shapeop`

Migration files are `pyproject.toml`, both requirements files,
`environment.yml`, a new `uv.lock`, `CMakeLists.txt`, `tasks.py`, all four
workflows, the Sphinx-to-MkDocs documentation conversion, build/release docs,
native and ABI tests, and artifact verification. The declared Python 3.9+
support conflicts with a `cp312` stable ABI and other Python baselines. That
contract must be resolved before workflow migration. Eigen needs integrity
verification, and the ignored local native tree is not a reproducible source.

### `compas_viewer`

Migration files are `pyproject.toml`, a new `uv.lock`, `tasks.py`, `mkdocs.yml`,
all six workflows, scene objects using obsolete COMPAS tessellation APIs,
associated tests, and contributor/build/headless-test documentation. The
mutable COMPAS Git branch installed by CI must be replaced by accepted bounds
or exact candidate artifacts. Qt/OpenGL packages and headless behavior must
remain visible rather than hidden in a generic profile.

## Cross-cutting blockers

1. No audited repository has a satisfactory committed development lock; CGAL's
   existing lock contradicts its project metadata.
2. Invoke and `compas_invocations2` remain canonical in most repositories.
3. Workflows widely use moving action tags, obsolete actions, broad or implicit
   permissions, and token-based publication.
4. Most release paths rebuild or do not prove promotion of the exact tested
   artifacts.
5. Python metadata, Ruff targets, CI matrices, native ABI settings, and actual
   dependency availability disagree in several repositories. ShapeOp is the
   most severe case.
6. Strict documentation is not a demonstrated green gate for most packages.
   Remote inventories also require a controlled network-aware verification
   environment.
7. Pyright is green only for `compas` and `compas_framework`; several other
   results are broad unconfigured scans and require authoritative scopes before
   debt can be fixed and made blocking.
8. Native and optional-runtime provisioning is not reproducibly verified for
   Gmsh, ShapeOp, Model, Viewer, or release artifacts.
9. `compas_framework` and `compas_session` contain pre-existing user-owned
   worktree state that must not be overwritten.

## Environmental limitations

- Restricted network access blocked remote documentation inventories and
  isolated build-dependency downloads.
- Read-only audit rules prevented Sphinx autosummary and build backends from
  generating files inside repositories.
- Phase 0 did not install, update, publish, deploy, or change repository
  settings.
- Missing Gmsh and ShapeOp native runtimes are recorded as unavailable, not as
  passing skips.
- Existing installed sibling plugins contaminated the nominally pure `compas`
  test run; Phase 1 must establish isolated and integration test modes.

## Phase 1 readiness

Phase 0 is complete: it has produced the required measured baseline, exact
Phase 1 debt manifests, and rollback commits. The dirty `compas_framework` and
`compas_session` worktrees have explicit preservation gates that must close
before their later migration phases. This does not block Phase 1, which may
begin with separate owners for `compas`, `compas_occ`, and `compas_cgal`.
Before editing:

1. preserve the recorded rollback commits and confirm each worktree state;
2. assign non-overlapping repository ownership;
3. keep `compas_framework` and `compas_session` user changes out of Phase 1 and
   do not edit either repository until its preservation gate is closed;
4. establish authoritative direct commands and writable temporary build output;
5. resolve failures within each reference repository before enabling new
   blocking gates; and
6. do not change repository settings, publish, deploy, or merge without further
   explicit approval.
