# Plugin Implementations Implementation Plan

## Status

Architecture complete; implementation is **blocked pending approval** of ADRs
001–006.

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

## Phase 1 — Reference baseline (Wave 0)

In-scope packages: `compas`, `compas_cgal`, `compas_libigl`, and `compas_occ`.

1. Add core tests for module-name and callable requirement selection,
   non-selection, default behavior, and `PluginNotInstalledError`.
2. Establish reusable assertions for installed metadata, fresh-process
   isolation, parity, delegation, and built artifacts.
3. Correct CGAL contributor guidance and remove obsolete RST guidance where it
   remains active.
4. Replace OCC synthetic-only metadata tests with installed and built-artifact
   evidence while preserving its no-OCC discovery proof.
5. Reverify libigl and CGAL without rewriting their approved architecture.

Exit criteria: all reference packages pass the verification contract that is
applicable to their runtime.

## Phase 2 — Model and viewer (Wave 1)

In-scope packages: `compas_model` and `compas_viewer`.

### Model

- remove obsolete `__all_plugins__`;
- inventory and resolve the duplicate scene registration path;
- preserve current scene registration semantics;
- add installed metadata, isolation, parity, delegation, conflict, and artifact
  tests.

### Viewer

- preserve its lightweight module;
- remove test-collection imports that invalidate isolation evidence;
- add installed metadata, fresh-process GUI isolation, parity, delegation, and
  artifact tests.

Coordinate ownership with the model-alignment and viewer-capability
initiatives.

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
