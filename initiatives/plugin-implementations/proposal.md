# Plugin Implementations Proposal

## Summary

Standardize packages on the current core plugin manager, explicit
`compas.plugins` entry points, lightweight category registration modules,
function-local implementation imports, and a common verification contract.
Do not add another registry, compatibility scanner, or wrapper-generation
system.

## Recommended architecture

### Authoritative discovery

Installed packages declare plugin modules only through PEP 621 metadata:

```toml
[project.entry-points."compas.plugins"]
package_trimesh = "package.plugins.trimesh"
```

Remove `__all_plugins__` after every legacy contract has been inspected, the
package requires a compatible COMPAS version, and replacement entry points and
tests are complete. Core must not restore legacy package scanning.

### Lightweight category modules

Use category-oriented registration modules, for example:

```text
src/package/plugins/
├── __init__.py
├── intersections.py
├── scene.py
└── trimesh.py
```

These modules import the decorator at runtime, import contract types only under
`TYPE_CHECKING`, define decorated wrappers, and import implementations inside
wrapper bodies. They perform no native, GUI, host, scene-adapter,
implementation, or registration-side-effect import during discovery.

Categories, rather than build artifacts, define module boundaries. Very small
packages may use one lightweight module when that remains clearer than a
directory.

### Wrapper contract

Every wrapper matches its core extension point in domain, category, name,
parameters, kinds, defaults, accepted structural inputs, return contract, and
documented failure behavior. Wrappers delegate. Native conversion and
process-safety validation remain in implementation modules.

The initiative does not change geometry representations, tessellation versus
triangulation, approximation controls, or scene registries. Those contracts
remain owned by their existing initiatives.

### Direct implementation APIs

Useful direct backend APIs may remain public, but they are undecorated, do not
register through import side effects, and do not maintain a divergent second
high-level contract. Clearly named low-level native APIs may retain genuinely
low-level results when documented as such.

### Optional runtimes

Registration succeeds without optional runtimes. `requires` identifies the
actual selectable runtime. Use a module-name requirement where `find_spec` is
sufficient and a callable only when presence does not prove availability.
Do not use the plugin package itself as a proxy for a different runtime.

Selection and invocation keep current core behavior. When nothing is
selectable, the core default or `PluginNotInstalledError` remains authoritative.
Ordinary implementation failures propagate after selection.

## Verification contract

Every migrated package verifies:

1. exact installed `compas.plugins` entry-point names and values;
2. fresh-process registration count and extension-point set;
3. absence of implementation, native, GUI, and host modules after discovery;
4. decorators only in registration modules;
5. full parameter, default, annotation, and result parity;
6. representative lazy delegation per registration module;
7. unavailable-runtime registration and non-selection behavior;
8. at least one real public dispatch per category;
9. direct implementation and native-boundary behavior separately;
10. built-wheel metadata and discovery isolation;
11. host-runtime evidence for every admitted host package. Missing host
    evidence is an incomplete gate, not a passing limitation.

Generated files use isolated temporary directories.

## Initial implementation scope

Approval of this proposal would authorize only Waves 0–1 and exactly these six
packages:

- `compas`
- `compas_cgal`
- `compas_libigl`
- `compas_occ`
- `compas_model`
- `compas_viewer`

Waves 2–4 are roadmap candidates. Adding any optional backend, host
integration, or other ecosystem package requires an explicit scope amendment
and new user approval. They are not part of the initial completion criteria.

## Initial rollout

### Wave 0 — Reference baseline

Affected packages: `compas`, `compas_cgal`, `compas_libigl`, and `compas_occ`.

- make the core author guide canonical;
- add missing core requirement-selection tests;
- freeze the reusable verification contract;
- remove stale CGAL guidance;
- strengthen OCC from synthetic to installed-metadata verification;
- avoid rewriting already correct references.

Typing alignment must stabilize relevant core signatures first.

### Wave 1 — Current COMPAS 3 packages

Affected packages: `compas_model` and `compas_viewer`.

- remove model's obsolete legacy list;
- resolve duplicate model scene registration;
- add installed metadata, isolation, parity, and conflict tests;
- add installed metadata and graphics-import isolation to viewer;
- preserve scene registry behavior.

Coordinate these edits with the model-alignment and viewer initiatives.

## Deferred roadmap — not authorized by initial approval

### Wave 2 — Compatible optional backends

Inspect contracts before adding metadata. Triangle requires triangulation
contract migration. IFC requires decorator and optional-viewer cleanup. Other
packages enter only after activity, ownership, and compatibility are confirmed.

### Wave 3 — Host integrations

Affected packages: Rhino, GH Python, Blender, and notebook.

Separate lightweight registration from host implementations, align current
core hooks, and require host-specific verification. If the required host
evidence cannot run, the admitted package remains incomplete and unverified.

### Wave 4 — Remaining ecosystem

Migrate active packages individually. Do not silently include archived or
duplicate checkouts. Every package requires explicit admission.

## Documentation

Core owns the canonical author guide. Package documentation describes only
package-specific runtimes and implementations. Examples show entry-point
metadata, lightweight wrappers, function-local imports, actual requirements,
and direct versus dispatched usage. Remove active guidance recommending
`__all_plugins__` and note plugin-ID changes as diagnostic changes.

## Alternatives

### Keep `__all_plugins__`

Rejected. Core does not read it, and restoring scanning creates competing
paths and import side effects.

### Point metadata at implementations

Rejected. Discovery eagerly imports optional and native runtimes.

### One monolithic module everywhere

Viable only for very small packages. Category modules are the default because
they provide clearer ownership and isolation without one file per function.

### One entry point per native extension

Rejected. Registration follows core categories, not build artifacts.

### Generate wrappers or metadata

Rejected. Generation adds machinery and obscures signatures and imports.

### Centralize third-party implementations in core

Rejected. It couples core to optional package releases and runtimes.

### Decorate and re-export direct APIs

Rejected. It still imports implementations during discovery and blurs the
registration boundary.

## Compatibility implications

- Migrated branches require COMPAS 3 before legacy discovery is removed.
- Moving decorators changes module-qualified plugin IDs; these are diagnostic,
  not stable public APIs, but changelogs should note the change.
- Direct imports remain valid.
- Equal-priority duplicates must be resolved explicitly.
- Incompatible legacy hooks require contract migration before metadata.
- No compatibility shims or duplicate registration paths are proposed.

## Approval boundary

ADRs 001–006 are Proposed. Implementation must not begin until the user
approves the proposal and decisions.
