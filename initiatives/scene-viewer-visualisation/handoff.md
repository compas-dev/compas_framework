# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-07

## Resume here

Current phase: `implementation`

Status: ADRs 001–010 are Accepted. Phase 0 core and Viewer source changes are
implemented and independently approved. Viewer package CI and the exact-source
framework integration gate are green; core CI is rerunning after focused patch
coverage tests were added.

Read next:

1. `objective.md`
2. `inventory.md`
3. `proposal.md`
4. `decisions/README.md`

## Decisions and approvals

- Accepted: [ADRs 001–010](decisions/README.md), including ADRs 008–010 on
  2026-11-07.
- Proposed or unresolved: none.
- Scope boundary: `compas_model`, notebook, and CAD hosts are later or
  compatibility consumers; `compas_session` requires an explicit inclusion
  decision. Do not modify package source outside the initial scope, merge, or
  publish without the corresponding approval.

## Working state

| Repository | Branch | Exact head | Pull request | Status |
|---|---|---|---|---|
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | this handoff checkpoint | [7](https://github.com/compas-dev/compas_framework/pull/7) | Exact-source gate green before latest candidate-pin refresh |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `38d2457861ba7122f91d2107ce11e85053105165` | [1540](https://github.com/compas-dev/compas/pull/1540) | Full matrix green; patch coverage rerunning |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `0fd73e9d17481bfcd2d69cf08c4db757a3ab16a5` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Phase 1 indexed-buffer candidate pushed; CI running |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Clean; inspected only |

## Completed at this checkpoint

- Inventoried core scene ownership, transformations, serialization, context
  dispatch, tests, and documentation gaps.
- Inventoried Viewer rendering, indexed-buffer limitations, selection,
  transforms, overlays, state, commands, and extension points.
- Inventoried model projection, render geometry, caching, selection, tests,
  documentation, and Viewer coupling.
- Identified initial and compatibility-only package boundaries.
- Produced the architecture proposal, seven independent Proposed ADRs, and a
  dependency-ordered implementation plan.
- Verified that Viewer ShapeObject state and ModelViewer scene reconstruction
  do not round-trip under the current constructor/settings mechanism.
- Proposed separate serializable node state, runtime adapter binding, durable
  node GUIDs, and explicit serialization fields in ADRs 008–009.
- Accepted ADRs 008–009 and proposed reference-only scene descriptions plus a
  separate future Session aggregation boundary in ADR 010.
- Recorded that the current `compas_model.ModelViewer` is a draft and only
  regression/coupling evidence, not a public contract to preserve.
- Implemented durable reference-only core scene nodes, explicit item binding,
  two-phase runtime-adapter binding, and validated MRO-composed state fields.
- Adapted Viewer durable state, removed legacy settings persistence, fixed
  transient picking-cache lifecycle, and documented separate data binding.
- Resolved all independent core and Viewer review findings.
- Added focused coverage for invalid closed Scene and SceneNode schemas.
- Added and passed an installed exact-source framework gate covering plugin
  discovery, reference-only round trips, explicit rebinding, and transient
  Viewer state exclusion.
- Implemented and independently approved indexed `BufferGeometry`, convenience
  constructors, closed JSON persistence, preserved buffer indices, and
  complete-triangle transparency partitioning.
- Reverified 36 `compas_model` Viewer/controller/plugin compatibility tests
  against the Phase 1 Viewer source without modifying model code.

## Next tasks

1. Collect clean Viewer CI and exact-source framework CI for the Phase 1 head.
2. Close the Phase 1 indexed-buffer exit gate.
3. Begin Phase 2 Viewer state and selection work in dependency order.

## Blockers and approval gates

- Package source implementation is authorized within the accepted initial
  scope.
- Adding model, session, notebook, or host packages to initial implementation
  scope requires explicit approval.

## Verification

Evidence by layer:

| Layer | Status | Evidence |
|---|---|---|
| Local focused checks | Passed | Core scene/glTF: 61 passed, Ruff passed, Pyright 0; Viewer focused: 50 passed, Ruff passed, Pyright 0; independent reviews approved both exact heads. |
| Package CI | Partial | Viewer PR 233 is fully green. Core PR 1540 has a green full OS/Python matrix, coverage, changelog, metadata, and project coverage; patch coverage is rerunning after ten additional schema-validation paths were covered. |
| Framework integration CI | Passed; refresh pending | Framework PR 7 passed contracts and the installed exact-candidate gate; the gate is rerunning against the latest test/workflow-only package heads. |
| Candidate-artifact CI | Not run | Required only before claims about independently built artifacts. |

Run next:

```text
gh pr checks <core-pr> --repo compas-dev/compas
gh pr checks <viewer-pr> --repo compas-dev/compas_viewer
```
