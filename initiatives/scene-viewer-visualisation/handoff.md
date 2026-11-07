# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-07

## Resume here

Current phase: `implementation`

Status: Cross-package reconnaissance and architecture are complete. The user
accepted ADRs 001–007 on 2026-11-07; implementation may begin in dependency
order within the approved initial scope.

Read next:

1. `objective.md`
2. `inventory.md`
3. `proposal.md`
4. `decisions/README.md`

## Decisions and approvals

- Accepted: [ADRs 001–007](decisions/README.md).
- Proposed or unresolved: none.
- Scope boundary: notebook and CAD hosts are compatibility consumers;
  `compas_session` requires an explicit inclusion decision. Do not modify
  package source outside the initial scope, merge, or publish without the
  corresponding approval.

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

## Next tasks

1. Review and approve or revise ADRs 001–007.
2. After approval, create package initiative branches from the recorded bases.
3. Begin Phase 1 compatibility review and indexed-buffer implementation.

## Blockers and approval gates

- Package source implementation is blocked on proposal and ADR approval.
- Adding session, notebook, or host packages to implementation scope requires
  explicit approval.

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
