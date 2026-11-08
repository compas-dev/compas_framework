# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-08

## Resume here

Current phase: `integration verification`

ADRs 013–014 are implemented and independently approved in core and Viewer.
They replace the earlier adapter design with hierarchy-only nodes, stable
backend-neutral scene objects, and context-keyed `draw`/`clear` operations.
The refreshed exact-candidate framework gate is green, so the accepted Phase 2
work may resume.

ADRs 015–016 were explicitly approved on 2026-11-08. They authorize contextual
object settings through editable `SceneStateField` entries, narrowly declared
non-state attributes, and runtime-only contextual overrides. Their amendment
supersedes the public `FormField` design and the first uncommitted separate
`EditableAttribute` design. The replacement core and Viewer implementations
are pushed, independently approved, and green in package and exact-candidate
integration CI.

ADRs 017–020 were explicitly approved on 2026-11-08 and implemented in the
required order: ADR 019, ADR 020, ADR 017, then ADR 018. The configured Viewer
identity, schema-2 configuration lifecycle/field cleanup, and lazy Mesh/Graph
element-attribute tables with narrow editing semantics are locally verified
and independently approved. Hosted verification of the refreshed Viewer and
exact framework candidates remains pending.

Architectural watchpoint: the user remains uncertain that the overall
`Data`/scene-state/extension model is the final destination. The current
Accepted ADRs remain authoritative. If implementation produces concrete
evidence that warrants redirection, stop and bring that evidence back for an
explicit amendment or new decision; do not reopen the model speculatively.

Read next:

1. [Implementation plan](implementation-plan.md)
2. [Decision index](decisions/README.md)
3. [Proposal](proposal.md)

## Exact candidates

| Repository | Branch | Exact head | Pull request | Status |
|---|---|---|---|---|
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `8bdb6d6b16ad70c46138445ef3e16eb13882c1c3` plus this evidence update | [7](https://github.com/compas-dev/compas_framework/pull/7) | Refreshed local source gate passed; hosted checks pending |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `314443976a056174ac755e4393059cb37795dda1` | [1540](https://github.com/compas-dev/compas/pull/1540) | Complete hosted matrix passed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `594ed282692e5d5bda15064a3b791eb8bf8499c5` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | ADRs 017–020 locally verified and independently approved; hosted rerun pending for this refreshed head |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed with one local-policy exclusion | Core passed 2,169 tests, Ruff, focused Pyright, strict docs, and independent review. The refreshed Viewer ADR 017–020 implementation passed its local package checks and independent review. Viewer’s ignored local `docs/examples/__temp` directory remains the recorded repository-policy exclusion. |
| Framework integration | Passed locally; hosted pending | The refreshed source gate pins the exact new heads and covers graphics-free discovery, stable scene identity, single-source editable `SceneStateField` declarations, contextual contribution/removal, data-only mutation, serialization exclusion, hierarchy and operation behavior, indexed-buffer round trips, schema-2 configuration, retired-field rejection, and datastructure-sidebar availability. Local source execution passed 5 public contract tests with the exact-install assertion skipped by design; hosted source-installed candidate checks remain pending. |
| Package CI | Partially passed; refreshed Viewer pending | Core passed its full OS/Python matrix, coverage, patch/project coverage, NumPy, metadata, and changelog checks at the pinned head. The previously pinned Viewer head passed its hosted matrix; the refreshed Viewer head still requires hosted verification. |
| Candidate artifacts | Not run | Required before independently built artifact compatibility is claimed. |

The broader `tests/test_package.py` run is locally unavailable because the
active `compas3` editable-import hook resolves `compas_cgal` from
`/private/tmp/compas-cgal-typing-adr017` instead of its checked-out sibling.
This is an environment provenance failure, not a scene-gate failure.

## Next tasks

1. Run hosted package CI for the refreshed Viewer candidate.
2. Run hosted exact-candidate framework integration at the recorded core and
   Viewer heads.
3. Run candidate-artifact verification before claiming independently built
   artifact compatibility.

## Approval gates

- The accepted initial implementation scope is core, Viewer, and framework.
- Adding model, session, notebook, or host packages requires explicit approval.
- Contextual form implementation is complete under Accepted ADRs 015–016.
- Datastructure tables/editing and configuration implementation is complete
  under Accepted ADRs 017–020; hosted verification remains pending.
- Do not merge or publish without explicit approval.
