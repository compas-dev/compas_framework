# Plugin Implementations

This initiative standardizes how COMPAS packages declare, discover, load,
test, and document plugin implementations without introducing a new plugin
system.

Current phase: **Architecture — awaiting approval**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)

ADRs 001–006 are **Proposed**. No package implementation is authorized until
the user explicitly approves the proposal and its decisions.

The proposed initial implementation scope is limited to Waves 0–1:
`compas`, `compas_cgal`, `compas_libigl`, `compas_occ`, `compas_model`, and
`compas_viewer`. Optional backends, host integrations, and other ecosystem
packages require a later explicit scope amendment and approval.
