# Plugin Implementations Inventory

Inventory date: 2026-11-05. Updated after the approved Wave 0–1 implementation
audit.

## Audited checkpoints

The audit used the following package checkpoints. Concurrent uncommitted CGAL
and libigl typing experiments did not touch the plugin files measured here.

| Package | Branch | Audited checkpoint |
|---|---|---|
| `compas` | `initiative/typing-alignment` | `afc4d31d2501bac2c542f17d4c8b05592e45ee7b` |
| `compas_cgal` | `initiative/typing-alignment` | `a46eecab71de5dfea6df7380d2eafb7185cc789a` |
| `compas_libigl` | `initiative/typing-alignment` | `86e3f1e0e02d6dc7cf9ad8049ac57c4c7d801877` |
| `compas_occ` | `initiative/typing-alignment` | `5a4cf9701007266e517996181c8476488c4030d9` |
| `compas_model` | `c3-upgrade` | `fdb37df8ee343bbaea5f6420d987e8a4ea468ed3` |
| `compas_viewer` | `c3-upgrade` | `ff1c81f37b7233c783a5e44f87adf4e8ca583f2a` |

## Core discovery contract

`compas.plugins.PluginManager.load_plugins` loads explicitly configured
builtin modules and modules declared in the installed `compas.plugins`
entry-point group. The global manager configures only `compas.scene` as a
builtin. It does not scan installed packages and does not read
`__all_plugins__`.

`PluginManager.register_module` inspects a loaded module for decorated
functions. Consequently, `entry_point.load()` imports every declared
registration module during discovery. Any native, GUI, host, scene-adapter, or
implementation import at module scope is therefore an eager discovery cost and
may prevent unrelated plugins from loading.

String requirements are checked with `find_spec` without importing the target.
Selection rejects equal-priority conflicts instead of relying on discovery
order. Call validation verifies argument binding, but discovery alone does not
prove annotation, result, or semantic parity.

Core documentation in `docs/background/plugins.md` already describes the
intended pattern: explicit entry points, lightweight registration modules, and
function-local optional imports.

## Current entry-point packages

| Package | Entry-point modules | Decorated functions | Current state |
|---|---:|---:|---|
| `compas_cgal` | 5 | 11 | Lightweight category modules and function-local implementation imports. |
| `compas_libigl` | 3 | 8 | Lightweight `trimesh`, `intersections`, and `quadmesh` modules; discovery is native-import-free. |
| `compas_occ` | 4 | 131 | Lightweight BRep, curve, surface, and intersection modules guarded by the OCC requirement. |
| `compas_model` | 1 | 2 total, 1 discoverable | Built entry point is isolated, but obsolete legacy registration, silent optional-runtime failure, and an alternate activation path remain. |
| `compas_viewer` | 1 | 4 | Registration functions defer scene imports, but Python first executes an eager package initializer that loads the GUI stack. |

### Measured Wave 0 evidence

Discovery from a clean external working directory in the required `compas3`
environment produced:

| Provider | Installed entry-point modules | Registered plugins | Selected plugins |
|---|---:|---:|---:|
| `compas_cgal` | 5 | 11 | 11 |
| `compas_libigl` | 3 | 8 | 8 |
| `compas_occ` | 4 | 131 | 131 |

Fresh-process discovery did not import backend implementation or native
modules for any of the three providers. Focused source/editable tests passed:
11 core plugin tests, 1 CGAL plugin test, 3 libigl plugin tests, and 11 OCC
plugin tests. These checks do not by themselves establish built-wheel
metadata, isolation, or runtime-unavailability behavior.

### Reference implementation state

CGAL and libigl are the clearest category-oriented references. Both declare
entry points, keep contract imports type-only, and import implementations
inside wrapper bodies. CGAL's adapters currently require only the provider
package rather than the actual compiled module. Three decorated CGAL functions
(`split_mesh_mesh`, `mesh_skeleton`, and `mesh_skeleton_with_mapping`) have no
current core pluggable and therefore belong on the undecorated direct-API path
unless a separately approved core contract is introduced. Active CGAL
contributor documentation still mentions `__all_plugins__`.

Libigl's eight adapters all map structurally to current core extension points,
but none declares a runtime requirement. Its discovery tests cover installed
metadata and selected lazy paths, not unavailable-runtime selection, every
adapter, representative public dispatch per category, or built-wheel
entry-point metadata.

OCC follows the same lazy principle and correctly names `OCC` as the optional
runtime. Its repository tests construct synthetic entry points and check
registration in the current process. The cross-package audit supplied
fresh-process evidence, but the package still lacks its own installed and
built-wheel metadata proof. Exact parity is tested for only eight intersection
wrappers; 48 curve/surface wrappers omit annotations present on their core
pluggables. Final annotation parity depends on the Proposed typing contracts.

### Measured Wave 1 evidence

Wheels built from isolated `git archive` source copies contained the intended
entry points:

- `compas_model = compas_model.plugins`;
- `compas_viewer = compas_viewer.plugins`.

The current editable installations were stale: model exposed no entry point,
while viewer still pointed to `compas_viewer.scene`. Existing tests therefore
do not prove the metadata of the checked-out branches.

Loading the built model entry point in a fresh process registered one plugin
without importing `compas_model.viewer`, `compas_viewer`, PySide6, or OpenGL.
Loading the built viewer entry point imported PySide6, OpenGL, and the complete
viewer scene package because Python executes `compas_viewer.__init__` before
`compas_viewer.plugins`.

### Partial modern packages

`compas_model` still declares `__all_plugins__` entries for obsolete or missing
modules and has two scene-registration implementations. This is not currently
an equal-priority conflict: core's scene registration hook uses
`selector="collect_all"`. The unresolved question is whether the dormant base
registration is intentional alongside the discoverable Viewer-context
registration. The discoverable wrapper declares no requirement, catches every
`ImportError`, and returns silently, so a missing viewer runtime, a broken GUI
dependency, and an implementation defect are indistinguishable. The manual
`ensure_scene_objects_registered` path is an alternate activation mechanism
that must be resolved with model/viewer ownership and core scene lifecycle.

`compas_viewer.plugins` keeps implementation imports inside wrapper bodies,
but the entry-point module is not actually lightweight because the package
initializer eagerly imports `Viewer`, PySide6, OpenGL, renderer, scene, and UI
modules first. Tests use synthetic metadata and import scene code during
collection, so they cannot expose this failure. The package also has a manual
`ensure_scene_objects_registered` path and advertises a COMPAS range beginning
at 2.2 even though exact plugin parity is verified only against COMPAS 3.

Both packages' real scene/render consumers still use stored resolutions,
cached tessellations, strategy objects, or the old `polygonize`/`tessellate`
paths. Their final dispatch evidence depends on Proposed Geometry ADRs 022–023
and Typing ADR 015.

## Legacy-only packages

Current worktrees with `__all_plugins__` but no inspected `compas.plugins`
entry points include:

- host and visualization packages: `compas_notebook`, `compas_rhino`,
  `compas_blender`, `compas_ghpython`;
- geometry and integration packages: `compas_ifc`, `compas_robots`,
  `compas_triangle`, `compas_fd`, `compas_tna`;
- ecosystem packages: `compas_ui`, `compas_cloud`, `compas_dr`,
  `compas_assembly`, `compas_bender`, `compas_dem`, `compas_rui`,
  `compas-Masonry`, `compas-FoFin`, `compas-IGS`, and `compas-RV`.

Archived or parallel checkouts also contain legacy lists, but are not release
targets merely because they exist.

These packages are not all metadata-only migrations:

- notebook scene registration eagerly imports its full adapter set and exposes
  at least one hook absent from current core;
- Rhino and Blender Boolean modules import their host runtimes at module scope
  and target obsolete Boolean hook names;
- host scene modules eagerly import adapter classes;
- `compas_triangle` targets obsolete triangulation hooks and mutates some
  caller inputs;
- `compas_ifc` uses an unsupported decorator option and imports optional viewer
  code too early.

Adding entry points before contract inspection could make incompatible plugins
selectable.

## Existing data contracts

The initiative must preserve the contracts currently established in package
source while tracking approved replacements explicitly:

- triangle algorithms currently use core `TriangleMeshInput` structural
  buffers and general-face operations use `MeshType` where supported; Proposed
  Typing ADRs 016–017 replace both with a coordinated public vocabulary, so
  final parity work must wait for their disposition;
- planar triangulation uses the core planar point/domain hooks and their
  approved result contract;
- OCC implements existing BRep, curve, surface, intersection, tessellation,
  and polygonal-surface contracts;
- viewer, model, notebook, and host plugins register adapters through current
  scene/factory extension points.

Native conversion and process-safety validation belong to implementation
modules, not registration wrappers.

## Test coverage

Strong reusable patterns exist for:

- installed distribution entry-point inspection;
- fresh-process discovery isolation;
- exact registration count and extension-point selection;
- decorator location and signature/default parity;
- representative lazy delegation;
- direct backend and native-boundary behavior.

Common gaps are:

- built-wheel metadata rather than editable-install metadata;
- optional requirement selection and unavailable-backend behavior;
- complete parity across every wrapper;
- conflict checks across packages;
- end-to-end public dispatch per category;
- host-runtime discovery and invocation evidence.

## Documentation state

Core's plugin author guide is a sound canonical baseline. Viewer documents its
entry point and warns against import side effects. CGAL contributor guidance
still recommends `__all_plugins__` in active Markdown and obsolete RST files.
OCC explains using plugins but not the registration architecture. Model,
notebook, Rhino, Blender, and GH Python lack equivalent current author guidance.

## Risks

1. Entry points can activate obsolete or incompatible hooks.
2. Host behavior cannot be inferred from ordinary CPython CI.
3. Multiple collect-all scene registrations can introduce unintended registry
   contents even when they do not create a selection conflict.
4. A requirement must identify the actual optional runtime, not merely the
   plugin package.
5. Moving decorators changes module-qualified diagnostic plugin IDs.
6. Stale documentation can reintroduce removed discovery patterns.

## Recommended waves

The approved initial scope contains only:

1. Wave 0: freeze the standard with core, CGAL, libigl, and OCC.
2. Wave 1: clean up current COMPAS 3 packages model and viewer.

The following remain roadmap candidates rather than current implementation or
completion scope:

3. compatible optional backends after contract inspection;
4. Rhino, GH Python, Blender, and notebook after explicit admission and with
   required host evidence;
5. remaining active ecosystem packages admitted individually.

Each later wave requires an explicit scope amendment and new user approval.
