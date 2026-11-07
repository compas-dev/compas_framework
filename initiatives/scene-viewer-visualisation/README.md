# Scene, Viewer, and Visualisation

This initiative aligns backend-neutral scene infrastructure, viewer rendering
and interaction, and model-to-scene integration across the COMPAS framework.

Current phase: **architecture approved; implementation may begin in dependency
order**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)
- [Current handoff](handoff.md)

The proposed initial package scope is `compas`, `compas_viewer`,
`compas_model`, and `compas_framework`. Session persistence, notebook
visualisation, and CAD-host adapters are compatibility-review consumers until
an approved decision admits them to implementation scope.
