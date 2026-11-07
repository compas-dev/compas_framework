# Scene, Viewer, and Visualisation

This initiative aligns backend-neutral scene infrastructure with Viewer
rendering, interaction, state, and UI composition.

Current phase: **architecture amendment proposed; implementation paused**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)
- [Current handoff](handoff.md)

ADRs 001–007 are Accepted. Verified round-trip failures exposed an unresolved
scene-node/runtime-adapter and serialization boundary. Proposed ADRs 008–009
must be approved before Phase 1 begins.

The refined initial package scope is `compas`, `compas_viewer`, and
`compas_framework`. The current `compas_model.ModelViewer` is draft evidence
and a later redesign consumer, not a behavior contract. Session persistence,
notebook visualisation, and CAD-host adapters are compatibility-review
consumers until an approved decision admits them to implementation scope.
