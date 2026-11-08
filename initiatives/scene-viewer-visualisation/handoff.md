# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-08

## Resume here

Current phase: `Phase 3 annotation architecture approval`

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
and independently approved. Their core and Viewer documentation audits are
complete. The refreshed package matrices and exact framework-candidate gate
are green.

ADR 003 object selection is implemented and independently approved. Viewer
state now owns one ordered GUID selection, every viewport/tree/command/settings
path uses it, and scene-local selection mutation APIs and the `Scene.add`
selection input are removed. Selection is intentionally transient and absent
from scene serialization. Local package and exact-source integration checks,
the complete hosted Viewer matrix, and refreshed exact-candidate checks pass.

ADR 004 transformations, refresh, and undo is implemented and independently
approved. One world-space delta is applied atomically to ordered current-scene
targets, converted through captured parent world transformations, and recorded
as one entry in a private Viewer-level undo/redo stack. Geometry, appearance,
transform, and hierarchy refreshes have explicit public operations. Hidden and
item-less groups now participate in runtime buffers so parent transforms remain
valid. Local Viewer, documentation, core scene, and exact-source integration
checks pass. The refreshed core and Viewer package matrices and exact framework
candidate gate also pass.

Phase 3 reconnaissance found that `TextAnnotation` is currently only an alias
for the Viewer-owned serialized `Tag`, while `ArrowOverlay` is actually durable
world-anchored scene content. ADR 023 is Accepted: both obsolete public names
and serialized dtype paths will be removed without aliases or legacy decoding.
ADR 024 is also Accepted: live measurement inspection is transient and does
not mutate Scene, while an explicit persistent mode creates a durable
`DistanceDimension`. ADR 028 is Accepted: one dimension type has independently
fixed or associative anchors; both modes snap, associative mode never silently
falls back, and removed component references become explicitly unresolved.
ADRs 021–022 are Accepted: narrow durable annotation data lives in
`compas.scene`, and persistent dimensions snapshot declared unit and precision
without implicit conversion. ADR 027 is Accepted: one Units and Measurement tab
owns editable Viewer unit/precision presentation and shows global COMPAS
tolerance read-only; snapping, not presentation, governs correctness. Proposed
ADRs 025–026 block implementation.

Architectural watchpoint: the user remains uncertain that the overall
`Data`/scene-state/extension model is the final destination. The current
Accepted ADRs remain authoritative. If implementation produces concrete
evidence that warrants redirection, stop and bring that evidence back for an
explicit amendment or new decision; do not reopen the model speculatively.

Read next:

1. [Implementation plan](implementation-plan.md)
2. [Decision index](decisions/README.md)
3. [Proposal](proposal.md)
4. [Exploratory UI sketch](ui.md)

## Exact candidates

| Repository | Branch | Exact head | Pull request | Status |
|---|---|---|---|---|
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `f4370a4` plus this architecture update | [7](https://github.com/compas-dev/compas_framework/pull/7) | Contracts and exact source-installed candidates passed |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `a4cc38a4f54d147f1ff45e19673b32f089576e2f` | [1540](https://github.com/compas-dev/compas/pull/1540) | Complete hosted matrix, coverage, NumPy, metadata, and documentation checks passed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `a4fe52e51f7254c13df9659f9a61dc22ebbc1daa` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | ADR 004 local checks, review, build, distributions, coverage, policy, and all nine OS/Python quality jobs passed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed with one local-policy exclusion | Viewer passed 289 tests with only the known ignored local `docs/examples/__temp` policy assertion deselected; Ruff, format, Pyright, strict docs, and independent review passed. Core scene tests and strict documentation passed. |
| Framework integration | Passed | The source gate pins core `a4cc38a4f54d147f1ff45e19673b32f089576e2f` and Viewer `a4fe52e51f7254c13df9659f9a61dc22ebbc1daa`. It verifies non-commuting parent/world conversion, undo/redo, history-preserving geometry/appearance refresh, and history-invalidating external transform refresh. Local source execution passed 6 public contract tests with the exact-install assertion skipped by design; Ruff, Pyright, and the direct pin assertion passed. Hosted contracts and exact source-installed candidates passed. |
| Package CI | Passed | Viewer passed build, distributions, coverage, policy, and all nine OS/Python quality jobs. Core passed its complete OS/Python matrix, coverage, NumPy, release metadata, and changelog checks. |
| Candidate artifacts | Not run | Required before independently built artifact compatibility is claimed. |

The broader `tests/test_package.py` run is locally unavailable because the
active `compas3` editable-import hook resolves `compas_cgal` from
`/private/tmp/compas-cgal-typing-adr017` instead of its checked-out sibling.
This is an environment provenance failure, not a scene-gate failure.

## Next tasks

1. Approve or amend ADR 025 scale and legend overlay contracts.
2. Approve or amend ADR 026 supported snapping
   and measurement acquisition.
3. After all Phase 3 ADRs are accepted, split implementation ownership across
   core annotations, Viewer rendering/tools, and framework integration.

## Approval gates

- The accepted initial implementation scope is core, Viewer, and framework.
- Adding model, session, notebook, or host packages requires explicit approval.
- Contextual form implementation is complete under Accepted ADRs 015–016.
- Datastructure tables/editing and configuration implementation is complete
  and verified under Accepted ADRs 017–020.
- ADRs 021–024 and 027–028 are Accepted; Phase 3 source changes remain blocked
  by proposed ADRs 025–026.
- Do not merge or publish without explicit approval.
