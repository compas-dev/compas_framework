# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-08

## Resume here

Current phase: `implementation`

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

ADRs 017–020 were explicitly approved on 2026-11-08. They authorize lazy
Mesh/Graph element-attribute tables, their narrow editing semantics, configured
Viewer identity, and configuration lifecycle/field cleanup. Implement ADR 019,
then ADR 020, followed by ADR 017 and ADR 018 so configuration and sidebar
ownership stabilize before table work.

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
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `fa47dbf358dd7286ea2c37e30092ed73995a4bb8` plus this evidence update | [7](https://github.com/compas-dev/compas_framework/pull/7) | Contracts and exact installed-candidate gate passed |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `314443976a056174ac755e4393059cb37795dda1` | [1540](https://github.com/compas-dev/compas/pull/1540) | Complete hosted matrix passed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `21a45d5352e89bdfab32aea0588532b414bfac87` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Complete hosted matrix passed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed with one local-policy exclusion | Core passed 2,169 tests, Ruff, focused Pyright, strict docs, and independent review. Viewer passed 177 applicable tests, Ruff, Pyright, strict docs, graphics-free discovery, and independent review. Viewer’s ignored local `docs/examples/__temp` directory remains the sole excluded repository-policy assertion. |
| Framework integration | Passed | The refreshed gate pins the exact new heads and covers graphics-free discovery, stable scene identity, single-source editable `SceneStateField` declarations, contextual contribution/removal, data-only mutation, serialization exclusion, hierarchy and operation behavior, and indexed-buffer round trips. Local source execution passed 4 tests with the exact-install assertion skipped by design; hosted contracts and source-installed candidates passed. |
| Package CI | Passed | Core passed its full OS/Python matrix, coverage, patch/project coverage, NumPy, metadata, and changelog checks. Viewer passed build, distributions, coverage, policy, and all nine OS/Python quality jobs. |
| Candidate artifacts | Not run | Required before independently built artifact compatibility is claimed. |

The broader `tests/test_package.py` run is locally unavailable because the
active `compas3` editable-import hook resolves `compas_cgal` from
`/private/tmp/compas-cgal-typing-adr017` instead of its checked-out sibling.
This is an environment provenance failure, not a scene-gate failure.

## Next tasks

1. Implement and verify ADR 019's configured Viewer identity.
2. Implement and verify ADR 020's configuration lifecycle, schema migration,
   and field audit.
3. After configuration/sidebar ownership stabilizes, implement ADR 017 and then
   ADR 018; refresh exact-candidate evidence and run candidate-artifact
   verification before claiming independently built artifact compatibility.

## Approval gates

- The accepted initial implementation scope is core, Viewer, and framework.
- Adding model, session, notebook, or host packages requires explicit approval.
- Contextual form implementation is authorized by Accepted ADRs 015–016.
- Datastructure tables/editing and configuration work are authorized by
  Accepted ADRs 017–020 in the recorded implementation order.
- Do not merge or publish without explicit approval.
