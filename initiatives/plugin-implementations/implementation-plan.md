# Plugin Implementations Implementation Plan

## Status

Architecture complete and ADRs 001–006 **Accepted**. Post-approval Wave 0–1
reconnaissance is complete and source migration is substantially implemented
on the coordinated initiative branches. Remaining selection, artifact, and
cross-package gates are listed below. No initiative changes have been merged
into a target/default branch or published.

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

Status: source migration substantially complete. CGAL uses four lightweight
category modules, actual compiled-module requirements, and nine valid core
plugins; its three orphan direct APIs are no longer decorated. Libigl retains
three lightweight category modules and eight core plugins, but still lacks
explicit compiled-runtime requirements. OCC retains four lightweight modules
and 130 plugins with the accepted signature/type corrections. Exact installed
CGAL/libigl/OCC entry-point discovery and strict wheel typing pass in the local
candidate integration evidence; package-owned evidence remains open. CGAL run
`42231235319` attempt 1 passed every platform's Python 3.12/3.14 wheel-smoke
jobs. The exact live manifest and offline staging are independently reviewed.
The Linux x86-64 CGAL→core→libigl runtime path remains reserved for the
hosted positive because it was not executable locally on Darwin ARM64.

1. Add core tests for module-name and callable requirement selection,
   non-selection, default behavior, and `PluginNotInstalledError`.
2. Establish reusable assertions for installed metadata, fresh-process
   isolation, parity, delegation, and built artifacts.
3. Keep CGAL contributor guidance free of obsolete `__all_plugins__`
   instructions. **Complete.**
4. Keep CGAL's three functions without a core pluggable as undecorated direct
   APIs. **Complete.**
5. Keep CGAL requirements bound to the actual compiled runtime. Add equivalent
   libigl requirements and registration-but-non-selection coverage when that
   runtime is unavailable. **CGAL complete; libigl open.**
6. Add representative real public dispatch and complete lazy-delegation
   coverage for libigl's registered categories.
7. Replace OCC synthetic-only metadata evidence with installed, fresh-process,
   and built-wheel checks while preserving no-OCC discovery.
8. Add built-wheel entry-point metadata, registration-count, isolation, and
   runtime-selection checks for every provider.
9. Require exhaustive shared-type, wrapper/core annotation, native-stub, and
   result parity under Accepted Typing ADRs 015–017. **The approved source
   migration is complete; final installed parity remains part of integration.**
10. Keep the consolidated OCC BRep conversion hook and final triangulation/BRep
    extension-point names aligned with Accepted Geometry ADRs 022–023 and
    Typing ADR 015. **Source migration complete; installed parity open.**

Exit criteria: all reference packages pass the verification contract that is
applicable to their runtime.

## Phase 2 — Model and viewer (Wave 1)

In-scope packages: `compas_model` and `compas_viewer`.

Status: source and package-local artifact migration complete on the current
modernization heads. Model discovery is isolated and requirement-gated; viewer
package initialization is lazy and entry-point discovery is graphics-free.
Both build workflows inspect the wheel entry point and run installed discovery.
The coordinated two-package registry/lifecycle test remains open.

### Model

- keep obsolete `__all_plugins__` removed;
- keep the discoverable Viewer-context registration as the sole plugin while
  retaining the documented `ensure_scene_objects_registered` helper for
  editable/source activation;
- keep the actual optional `compas_viewer` requirement and propagate
  implementation import failures;
- retain installed metadata, wheel, fresh-process isolation,
  unavailable-runtime, and registry-result tests; and
- migrate real geometry/render consumers only after Geometry ADRs 022–023 and
  Typing ADR 015 establish their final conversion APIs.

### Viewer

- keep actual entry-point loading graphics-free, including package-initializer
  execution, while preserving the approved public Viewer import contract;
- keep isolation evidence independent of test-collection scene imports;
- retain the explicit activation helper where source/editable lifecycle needs
  it, without adding a second installed discovery path;
- keep the supported COMPAS range aligned with the verified C3 contract;
- retain installed metadata, wheel, external-process isolation, parity,
  delegation, drawing-semantics, and artifact tests; and
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
