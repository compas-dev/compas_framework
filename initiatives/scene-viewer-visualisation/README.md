# Scene, Viewer, and Visualisation

This initiative aligns backend-neutral scene infrastructure with Viewer
rendering, interaction, state, and UI composition.

Current phase: **editable-attribute and contextual-form implementation**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)
- [Current handoff](handoff.md)

The stable scene architecture correction in Accepted ADRs 013–014 is
implemented and verified: nodes are hierarchy-only, durable scene objects are
stable, and backend operations are context-keyed. Amended Accepted ADRs
015–016 now govern `SceneStateField`-backed editability, narrowly declared
non-state editable attributes, and Viewer-owned contextual forms. Scene
remains reference-only, and optional aggregation is reserved for a separate
future Session design.

Proposed ADRs 017–020 cover lazy Mesh/Graph element-attribute tables, their
editing semantics, configured Viewer identity, and configuration lifecycle.

The refined initial package scope is `compas`, `compas_viewer`, and
`compas_framework`. The current `compas_model.ModelViewer` is draft evidence
and a later redesign consumer, not a behavior contract. Session persistence,
notebook visualisation, and CAD-host adapters are compatibility-review
consumers until an approved decision admits them to implementation scope.
