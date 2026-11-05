# Plugin Implementations Inventory

Inventory date: 2026-11-05.

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
| `compas_model` | 1 | 2 total, 1 discoverable | New lightweight module, but obsolete legacy registration and a duplicate scene path remain. |
| `compas_viewer` | 1 | 4 | Lightweight registration with function-local scene imports; verification is incomplete. |

### Reference evidence

CGAL and libigl are the clearest category-oriented references. Both declare
installed entry points, keep contract imports type-only, import implementations
inside wrapper bodies, and test installed metadata plus fresh-process discovery
without native imports. Libigl additionally verifies lazy delegation and
parameter/default parity.

OCC follows the same lazy principle. Its tests construct synthetic entry
points, verify 131 registrations, and prove discovery does not import OCC, but
they do not yet verify the installed distribution metadata as required by its
repository instructions. Signature parity is partial.

### Partial modern packages

`compas_model` still declares `__all_plugins__` entries for obsolete or missing
modules and has two scene-registration implementations. Restoring legacy
scanning would create an equal-priority conflict. Its tests do not verify
installed metadata, discovery isolation, signature parity, or conflicts.

`compas_viewer` uses a lightweight module, but tests use a synthetic entry
point and import scene code during test collection. Installed metadata,
fresh-process graphics-import isolation, and full signature parity are not
verified.

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

The initiative must preserve established contracts:

- triangle algorithms use core `TriangleMeshInput` structural buffers;
- general-face operations use `MeshType` where supported;
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
3. Duplicate scene registrations cause explicit conflicts.
4. A requirement must identify the actual optional runtime, not merely the
   plugin package.
5. Moving decorators changes module-qualified diagnostic plugin IDs.
6. Stale documentation can reintroduce removed discovery patterns.

## Recommended waves

The proposed initial scope contains only:

1. Wave 0: freeze the standard with core, CGAL, libigl, and OCC.
2. Wave 1: clean up current COMPAS 3 packages model and viewer.

The following remain roadmap candidates rather than current implementation or
completion scope:

3. compatible optional backends after contract inspection;
4. Rhino, GH Python, Blender, and notebook after explicit admission and with
   required host evidence;
5. remaining active ecosystem packages admitted individually.

Each later wave requires an explicit scope amendment and new user approval.
