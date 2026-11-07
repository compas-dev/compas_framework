# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-07

## Resume here

Current phase: `implementation`

Status: ADRs 001–010 are Accepted. Phase 0 core and Viewer source changes are
implemented and independently approved locally; clean hosted package CI remains
to be collected before the Phase 0 exit gate is complete.

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
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `ee8c4d8` plus this handoff checkpoint | [7](https://github.com/compas-dev/compas_framework/pull/7) | Clean; pushed draft |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `f878cd102e87e7859030af96c7871a5b3345cf7d` | [1540](https://github.com/compas-dev/compas/pull/1540) | Clean; pushed draft |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `18c87acac907c6d749d95a0e8f56ae2abd021ed2` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Clean; pushed draft |
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

## Next tasks

1. Collect clean package CI on core PR 1540 and Viewer PR 233.
2. Add the smallest framework installed-candidate Phase 0 gate.
3. Close the Phase 0 exit gate, then begin indexed-buffer implementation.

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
| Package CI | Pending | Viewer PR 233 workflows are running; core PR 1540 initially reports no checks. |
| Framework integration CI | Pending | Framework PR 7 contract check is running; installed exact-candidate gate is the next task. |
| Candidate-artifact CI | Not run | Required only before claims about independently built artifacts. |

Run next:

```text
gh pr checks <core-pr> --repo compas-dev/compas
gh pr checks <viewer-pr> --repo compas-dev/compas_viewer
```
