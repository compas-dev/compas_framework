# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-07

## Resume here

Current phase: `architecture`

Status: ADRs 001–010 are Accepted. Scene is reference-only and a separate
future Session redesign may aggregate data, scenes, settings, and history.
Implementation may proceed within the approved initial scope.

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
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `<commit after architecture checkpoint>` | None | Local initiative documents |
| `compas-dev/compas` | `remove-future` | `99b82a6673ff7d05c1c323c8921135c274993f11` | None | Clean; inspected only |
| `compas-dev/compas_viewer` | `c3-upgrade` | `cf5a5195bda840a511319d6b7201978af68c15e3` | None | Clean; inspected only |
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

## Next tasks

1. Refresh core/Viewer branches, add the Viewer regression, and cover the draft
   ModelViewer failure mode with a minimal core adapter test.
2. Complete Phase 0 before indexed-buffer implementation begins; defer
   `compas_model` controller redesign to a later approved phase.
3. Run the Phase 0 package and framework verification gates.

## Blockers and approval gates

- Package source implementation is authorized within the accepted initial
  scope.
- Adding model, session, notebook, or host packages to initial implementation
  scope requires explicit approval.

## Verification

Evidence by layer:

| Layer | Status | Evidence |
|---|---|---|
| Local focused checks | Passed | Core 53 tests and Viewer 35 tests passed during reconnaissance; inventory documents the commands and warning scope. |
| Package CI | Not run | No package branches changed. |
| Framework integration CI | Not run | No implementation exists yet. |
| Candidate-artifact CI | Not applicable | Architecture documents only. |

Run next:

```text
git diff --check
/Users/vanmelet/miniforge3/envs/compas3/bin/python -m mkdocs build --strict
```
