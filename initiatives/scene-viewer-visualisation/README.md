# Scene, Viewer, and Visualisation

This initiative aligns backend-neutral scene infrastructure with Viewer
rendering, interaction, state, and UI composition.

Current phase: **Phase 3 ADR 032 locally verified; hosted refresh pending**.

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

Accepted ADRs 017–020 govern lazy Mesh/Graph element-attribute tables, their
editing semantics, configured Viewer identity, and configuration lifecycle.
They are implemented, locally verified, and independently approved. Hosted
Viewer and framework checks passed. ADR 003 object selection and ADR 004
transformations, categorized refresh, and Viewer-level transform history are
also implemented and fully verified. Accepted ADRs 021–028 and 030 are
implemented for durable Core annotations, Viewer rendering and overlays,
measurement snapping and interaction, unit/precision presentation,
discrete-only point acquisition, and an always-visible persistent-dimension
pass. The latest measurement follow-up is verified in Viewer package CI and the
framework exact source-installed gate. Accepted ADRs 029 and 031 now authorize
the separate annotation collection and UI, narrow durable dimension style, and
discoverable spatial-object deletion. Their Core and Viewer implementations
and refreshed package and exact source-installed framework integration pass.
Direct-use evidence exposed an unstable and ambiguous stacked sidebar, so ADR
032 accepts a three-domain Scene, Annotations, and System replacement. Its
implementation, documentation, local verification, framework direct-source
gate, and independent review pass; hosted package and exact integration
refreshes are pending. Exact candidate-artifact
compatibility has not been run and is not implied by the existing results.

The refined initial package scope is `compas`, `compas_viewer`, and
`compas_framework`. The current `compas_model.ModelViewer` is draft evidence
and a later redesign consumer, not a behavior contract. Session persistence,
notebook visualisation, and CAD-host adapters are compatibility-review
consumers until an approved decision admits them to implementation scope.
