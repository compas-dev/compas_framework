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
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `0fe8f4a` plus this evidence update | [7](https://github.com/compas-dev/compas_framework/pull/7) | Exact-source contracts and installed-candidate gate passed |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | runtime candidate `d43db206afec36450efbe76b53306ce3bd468076`; test-only head `41e51713352` | [1540](https://github.com/compas-dev/compas/pull/1540) | Codecov patch/project, coverage, build, and NumPy checks passed; remaining matrix rerun pending |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `a72b61b777bc3fd448c3d471c48ef7f65334b319` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Complete hosted matrix passed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed with one local-policy exclusion | Core focused scene/glTF checks, Ruff, Pyright, strict docs, and independent review passed. Viewer passed 161 applicable tests, Ruff, Pyright, strict docs, and independent review. Viewer’s ignored local `docs/examples/__temp` directory remains the sole excluded repository-policy assertion. |
| Framework integration | Passed | The refreshed gate covers exact revisions, graphics-free discovery, stable semantic types and GUIDs, hierarchy-only nodes, external item rebinding, context-keyed operations without class substitution, transient runtime exclusion, and indexed-buffer round trips. Local source execution passed 3 tests with the exact-install assertion skipped by design; hosted contracts and source-installed candidates passed. |
| Package CI | Viewer passed; core rerun in progress | Viewer build, coverage, policy, distribution, and all nine OS/Python quality jobs passed. Core's Codecov patch/project, coverage, build, and NumPy checks passed after focused closed-schema tests raised expected patch coverage from 85.59% to 86.10%; the remaining matrix jobs are rerunning. |
| Candidate artifacts | Not run | Required before independently built artifact compatibility is claimed. |

The broader `tests/test_package.py` run is locally unavailable because the
active `compas3` editable-import hook resolves `compas_cgal` from
`/private/tmp/compas-cgal-typing-adr017` instead of its checked-out sibling.
This is an environment provenance failure, not a scene-gate failure.

## Next tasks

1. Confirm the remaining core PR 1540 matrix rerun completes green.
2. Resume Phase 2 Viewer state and selection work from the verified stable-scene foundation.
3. Run candidate-artifact verification before claiming independently built artifact compatibility.

## Approval gates

- The accepted initial implementation scope is core, Viewer, and framework.
- Adding model, session, notebook, or host packages requires explicit approval.
- Do not merge or publish without explicit approval.
