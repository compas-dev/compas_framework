# Plugin Implementations Inventory

Inventory date: 2026-11-06. Updated after the approved Wave 0–1 implementation
audit and the subsequent typing/modernization checkpoints.

## Audited checkpoints

The current coordination record uses these pushed candidate or modernization
heads. Counts below were re-inspected from these source checkpoints; hosted
claims are limited to the package evidence recorded by the owning initiative.

| Package | Branch | Audited checkpoint |
|---|---|---|
| `compas` | `initiative/typing-alignment` | `99b82a6673ff7d05c1c323c8921135c274993f11` |
| `compas_cgal` | `initiative/typing-alignment` | `7537d58154f62f38c0b2d4118972d0a326f86c9b` |
| `compas_libigl` | `initiative/typing-alignment` | `710b2b6714839a203fc8a6c62c437c0f6735ba0e` |
| `compas_occ` | `initiative/typing-alignment` | `7fdf2ffb57d1de16308020e14ec626d79e65a034` |
| `compas_model` | `initiative/repository-modernisation` | `83df4167f7ba1539ae205a837e0238afecc0a36b` |
| `compas_viewer` | `initiative/repository-modernisation` | `cf5a5195bda840a511319d6b7201978af68c15e3` |

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
| `compas_cgal` | 4 | 9 | Lightweight category modules, function-local implementation imports, and per-family compiled-module requirements. |
| `compas_libigl` | 3 | 8 | Lightweight `trimesh`, `intersections`, and `quadmesh` modules; discovery is native-import-free, but requirements do not yet name the compiled runtime. |
| `compas_occ` | 4 | 130 | Lightweight BRep, curve, surface, and intersection modules guarded by the OCC requirement. |
| `compas_model` | 1 | 1 | Built entry point is isolated, requires `compas_viewer`, and preserves implementation import failures. |
| `compas_viewer` | 1 | 4 | Lazy package exports make actual entry-point loading Qt/OpenGL-free; implementation imports remain inside wrappers. |

### Measured Wave 0 evidence

The initial clean external-process audit produced:

| Provider | Installed entry-point modules | Registered plugins | Selected plugins |
|---|---:|---:|---:|
| `compas_cgal` | 5 | 11 | 11 |
| `compas_libigl` | 3 | 8 | 8 |
| `compas_occ` | 4 | 131 | 131 |

Fresh-process discovery did not import backend implementation or native
modules for any of the three providers. The later CGAL cleanup intentionally
reduced its entry-point/decorator counts from 5/11 to 4/9, and the OCC contract
consolidation reduced its decorator count from 131 to 130. Therefore the table
above is historical evidence, not the expected count for the current heads.

At the current heads, package tests verify the changed registration contracts,
and framework ADR 021's local native smoke discovers installed CGAL, libigl,
and OCC entry-point modules before exercising representative implementations.
The lightweight source modules are inspected separately. The final
live-candidate run is still required before that cross-package artifact
evidence is complete.

### Reference implementation state

CGAL and libigl are the clearest category-oriented references. Both declare
entry points, keep contract imports type-only, and import implementations
inside wrapper bodies. CGAL now requires the actual compiled module for each
family. `split_mesh_mesh`, `mesh_skeleton`, and
`mesh_skeleton_with_mapping` have no current core pluggable and are retained as
undecorated direct APIs. Active contributor guidance explicitly forbids legacy
`__all_plugins__` discovery.

Libigl's eight adapters map structurally to current core extension points and
now use the approved private hook names and complete native stubs. None yet
declares a compiled-runtime requirement. Its discovery and wheel tests cover
installed metadata and selected lazy paths; unavailable-runtime selection and
the complete per-category public-dispatch matrix remain open.

OCC follows the same lazy principle and correctly names `OCC` as the optional
runtime. Its accepted curve, surface, BRep, and intersection signature/type
corrections are present at the current head. Repository plugin tests still use
synthetic entry points, so package-owned installed and built-wheel discovery
proof remains open even though the framework native smoke supplies
cross-package installed evidence.

### Measured Wave 1 evidence

Current built wheels contain the intended entry points:

- `compas_model = compas_model.plugins`;
- `compas_viewer = compas_viewer.plugins`.

Model's installed consumer verifies the exact wheel entry point, registers one
Viewer-context plugin, proves that `compas_viewer` is absent, and confirms the
requirement prevents selection. Viewer makes its package exports lazy, so
loading the real installed entry point registers four plugins without loading
PySide6, OpenGL, or scene implementation modules. Its build workflow checks
the wheel metadata and repeats graphics-free discovery in a clean wheel
environment.

### Current Wave 1 packages

`compas_model` removes the legacy list and dormant second decorated
registration. Its sole plugin declares `requires=["compas_viewer"]`, performs
implementation imports in the function body, and does not swallow
implementation failures. `ensure_scene_objects_registered` is documented as
an explicit helper for editable/source activation and does not create a second
installed discovery mechanism.

`compas_viewer.plugins` keeps implementation imports inside wrapper bodies,
and the package initializer now exposes Viewer and related public objects
lazily. Source and installed-wheel tests prove that entry-point discovery is
graphics-free. Final initiative evidence still needs the coordinated
model/viewer collect-all registry and lifecycle test.

Both packages' real scene/render consumers still use stored resolutions,
cached tessellations, strategy objects, or the old `polygonize`/`tessellate`
paths. Their final dispatch evidence depends on Accepted Geometry ADRs 022–023
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
  buffers and general-face operations use `MeshType` where supported; Accepted
  Typing ADRs 016–017 replace both with a coordinated public vocabulary, so
  final parity work follows their accepted migration order;
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

Core's plugin author guide is the canonical baseline. Viewer documents its
entry point and warns against import side effects. CGAL and OCC agent guidance
requires explicit entry points and forbids restoring `__all_plugins__`.
Package-level contributor guidance and final migration notes remain uneven;
model, notebook, Rhino, Blender, and GH Python lack equivalent current author
guidance, though only model is in the approved Waves 0–1 scope.

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
