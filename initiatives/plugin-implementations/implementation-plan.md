# Plugin Implementations Implementation Plan

## Status

Architecture complete and ADRs 001–006 **Accepted**. Post-approval Wave 0–1
reconnaissance is complete; implementation and artifact-level verification are
incomplete. No initiative changes have been merged into a target/default
branch or published.

## Dependency graph

```text
typing/geometry contract stability
              |
              v
ADR 001 -> ADR 002
              | \
              v  v
          ADR 003 ADR 004
              \  /
               v
            ADR 005
               |
               v
            ADR 006
               |
               v
        Wave 0 -> Wave 1
```

Repository modernization must provide suitable packaging and artifact checks
before a package can satisfy its final rollout gate.

Initial approval authorizes only Waves 0–1 and the six packages named below.
Later waves require a scope amendment and new approval.

Work is split into three dependency classes:

1. **Independent:** requirement-selection tests, runtime requirements, orphan
   decorator cleanup, stale legacy guidance, and installed/wheel evidence.
2. **Typing/geometry dependent:** shared structural annotation and native-stub
   parity follow Accepted Typing ADRs 016–017. Triangulation and conversion
   signatures follow Accepted Typing ADR 015 and Geometry ADR 022. BRep
   default-value tests additionally follow Accepted Geometry ADR 023. Real
   model/viewer rendering paths follow the specific conversion contracts they
   consume.
3. **Model/viewer design dependent:** base versus Viewer-context registration,
   manual activation helpers, viewer package initialization, and scene
   lifecycle ownership require the corresponding package architecture work.

## Phase 1 — Reference baseline (Wave 0)

In-scope packages: `compas`, `compas_cgal`, `compas_libigl`, and `compas_occ`.

Status: audit complete; source/editable discovery is substantially compliant;
remaining work is listed below.

1. Add core tests for module-name and callable requirement selection,
   non-selection, default behavior, and `PluginNotInstalledError`.
2. Establish reusable assertions for installed metadata, fresh-process
   isolation, parity, delegation, and built artifacts.
3. Correct CGAL contributor guidance and remove obsolete `__all_plugins__`
   instructions where they remain active.
4. Remove decorators from CGAL's three functions without a core pluggable,
   retaining them as direct APIs unless a separate core extension point is
   approved.
5. Make CGAL and libigl requirements identify the actual compiled runtime and
   test registration-but-non-selection when that runtime is unavailable.
6. Add representative real public dispatch and complete lazy-delegation
   coverage for libigl's registered categories.
7. Replace OCC synthetic-only metadata evidence with installed, fresh-process,
   and built-wheel checks while preserving no-OCC discovery.
8. Add built-wheel entry-point metadata, registration-count, isolation, and
   runtime-selection checks for every provider.
9. After Typing ADRs 016–017 are resolved, require exhaustive shared-type,
   wrapper/core annotation, native-stub, and result parity, including OCC's 48
   incomplete curve/surface wrappers. Operation-specific wrappers also follow
   Typing ADR 015 where applicable.
10. After Geometry ADR 022 and Typing ADR 015 are resolved, consolidate OCC's
    BRep conversion hook and verify the final triangulation/BRep extension-point
    names. Add BRep default-value parity only after Geometry ADR 023 is
    resolved.

Exit criteria: all reference packages pass the verification contract that is
applicable to their runtime.

## Phase 2 — Model and viewer (Wave 1)

In-scope packages: `compas_model` and `compas_viewer`.

Status: audit complete; built metadata is correct, model discovery is isolated,
and viewer discovery is graphics-eager. Neither package satisfies the complete
verification contract.

### Model

- remove obsolete `__all_plugins__`;
- decide whether the dormant default-context base registration is intentional
  alongside the discoverable Viewer-context registration; do not describe the
  current collect-all behavior as an equal-priority conflict;
- declare the actual optional viewer requirement and stop swallowing arbitrary
  implementation `ImportError` exceptions;
- resolve or explicitly preserve `ensure_scene_objects_registered` with the
  model/viewer scene-lifecycle design;
- add installed metadata, wheel, fresh-process isolation, parity, lazy
  delegation, unavailable-runtime, and registry-result tests; and
- migrate real geometry/render consumers only after Geometry ADRs 022–023 and
  Typing ADR 015 establish their final conversion APIs.

### Viewer

- make actual entry-point loading graphics-free, including package-initializer
  execution, while preserving the approved public Viewer import contract;
- remove test-collection imports that invalidate isolation evidence;
- resolve or explicitly preserve manual `ensure_scene_objects_registered`
  activation with core scene lifecycle;
- align the supported COMPAS range with the verified C3 plugin contract;
- add installed metadata, wheel, external-process isolation, parity,
  delegation, unavailable-runtime, drawing-semantics, and artifact tests; and
- migrate scene objects away from stored resolution and cached tessellation
  only after the approved geometry conversion contract is implemented.

Coordinate ownership with the model-alignment, viewer-capability,
repository-modernisation, geometry-tessellation, and typing-alignment
initiatives. A coordinated installed test must finally prove both packages'
collect-all registrations together.

## Deferred roadmap

The following phases are not authorized by initial approval and do not affect
initial completion. Each requires an explicit scope amendment and new approval.

### Candidate Wave 2 — Compatible optional backends

For each candidate package:

1. confirm active ownership and supported COMPAS version;
2. compare every legacy hook to current core;
3. migrate incompatible contracts before enabling entry points;
4. add lightweight registration modules and remove legacy discovery;
5. satisfy the verification contract.

Triangle and IFC require known contract work before metadata migration.

### Candidate Wave 3 — Host integrations

Migrate Rhino, GH Python, Blender, and notebook independently. Separate host
imports from registration, align hooks, and define the host-runtime validation
command and evidence in each repository. Required host evidence is a completion
gate. If it is unavailable, the admitted package remains incomplete and must
not be reported as passing.

### Candidate Wave 4 — Remaining ecosystem

Maintain an active-package inventory. Admit one owned and compatible package at
a time through explicit approval. Archived duplicates are excluded unless
explicitly promoted to release targets.

## Per-package task template

1. Inspect metadata, legacy list, decorated functions, direct APIs, imports,
   requirements, tests, and docs.
2. Record contract mismatches before editing.
3. Assign exclusive ownership of metadata, registration modules,
   implementations, tests, and docs.
4. Implement only approved contract-preserving changes.
5. Run focused tests, full feasible tests, Ruff, formatting, Pyright, strict
   docs, built artifact checks, and host tests where required.
6. Request independent review.
7. Resolve findings and rerun affected checks.
8. Update initiative status without merging or publishing.

## Integration checks

- discover the coordinated installed package set in a fresh process;
- assert extension-point uniqueness or approved priority relationships;
- prove unavailable optional packages do not block unrelated discovery;
- exercise representative real public dispatch in every migrated category;
- inspect wheels rather than relying only on editable installs;
- keep generated artifacts in temporary directories.

## Completion criteria

- ADRs 001–006 are Accepted;
- all six in-scope packages—`compas`, `compas_cgal`, `compas_libigl`,
  `compas_occ`, `compas_model`, and `compas_viewer`—satisfy their approved
  work packages;
- all in-scope plugin providers use explicit entry points only;
- discovery does not import implementation or optional runtime modules;
- wrappers exactly conform to stable core contracts;
- direct APIs are documented and non-divergent;
- applicable source, wheel, typing, and documentation gates pass;
- active documentation contains no `__all_plugins__` guidance;
- final independent cross-package review has no unresolved findings.

Optional backends, host integrations, and other ecosystem packages are not
initial completion criteria. Once admitted through a later scope amendment,
all applicable gates—including required host evidence—must pass.
