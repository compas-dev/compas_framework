# Plugin Implementations

This initiative standardizes how COMPAS packages declare, discover, load,
test, and document plugin implementations without introducing a new plugin
system.

Current phase: **Implementation reconnaissance complete; Waves 0–1
implementation incomplete**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)

ADRs 001–006 are **Accepted**. Implementation is authorized only for the six
packages in Waves 0–1. The post-approval audit found that entry-point metadata
and lazy registration are already substantially in place, but runtime
requirements, complete contract parity, built-wheel evidence, and the
model/viewer activation boundaries still have open work.

The approved initial implementation scope is limited to Waves 0–1:
`compas`, `compas_cgal`, `compas_libigl`, `compas_occ`, `compas_model`, and
`compas_viewer`. Optional backends, host integrations, and other ecosystem
packages require a later explicit scope amendment and approval.
