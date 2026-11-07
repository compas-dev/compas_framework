# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-07

## Resume here

Current phase: `integration verification`

ADRs 013–014 are implemented and independently approved in core and Viewer.
They replace the earlier adapter design with hierarchy-only nodes, stable
backend-neutral scene objects, and context-keyed `draw`/`clear` operations.
Phase 2 remains paused until the refreshed exact-candidate framework gate is
green.

Read next:

1. [Implementation plan](implementation-plan.md)
2. [Decision index](decisions/README.md)
3. [Proposal](proposal.md)

## Exact candidates

| Repository | Branch | Exact head | Pull request | Status |
|---|---|---|---|---|
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | current working tree | [7](https://github.com/compas-dev/compas_framework/pull/7) | Gate refresh pending commit and CI |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `d43db206afec36450efbe76b53306ce3bd468076` | [1540](https://github.com/compas-dev/compas/pull/1540) | Stable scene architecture pushed; local checks and independent review passed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `a72b61b777bc3fd448c3d471c48ef7f65334b319` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Stable operation/runtime migration pushed; 161 applicable tests, Ruff, Pyright, and independent review passed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed with one local-policy exclusion | Core focused scene/glTF checks, Ruff, Pyright, strict docs, and independent review passed. Viewer passed 161 applicable tests, Ruff, Pyright, strict docs, and independent review. Viewer’s ignored local `docs/examples/__temp` directory remains the sole excluded repository-policy assertion. |
| Framework integration | Local source gate passed; hosted gate pending | The refreshed gate covers exact revisions, graphics-free discovery, stable semantic types and GUIDs, hierarchy-only nodes, external item rebinding, context-keyed operations without class substitution, transient runtime exclusion, and indexed-buffer round trips. Local source execution passed 3 tests with the exact-install assertion skipped by design. |
| Package CI | Pending refreshed heads | Check PRs 1540 and 233 after the framework gate is pushed. |
| Candidate artifacts | Not run | Required before independently built artifact compatibility is claimed. |

The broader `tests/test_package.py` run is locally unavailable because the
active `compas3` editable-import hook resolves `compas_cgal` from
`/private/tmp/compas-cgal-typing-adr017` instead of its checked-out sibling.
This is an environment provenance failure, not a scene-gate failure.

## Next tasks

1. Commit and push the refreshed framework exact-candidate gate, then verify PR 7.
2. Verify package PR checks for the exact core and Viewer heads and record results by layer.
3. Resume Phase 2 Viewer state and selection only after framework integration is green.

## Approval gates

- The accepted initial implementation scope is core, Viewer, and framework.
- Adding model, session, notebook, or host packages requires explicit approval.
- Do not merge or publish without explicit approval.
