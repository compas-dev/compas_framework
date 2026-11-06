# Plugin Implementations

This initiative standardizes how COMPAS packages declare, discover, load,
test, and document plugin implementations without introducing a new plugin
system.

Current phase: **Waves 0–1 source migration substantially implemented;
coordinated artifact and remaining selection/parity gates incomplete**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)

ADRs 001–006 are **Accepted**. Implementation is authorized only for the six
packages in Waves 0–1. Subsequent modernization and typing work completed the
CGAL registration cleanup, the model optional-runtime boundary, graphics-free
viewer discovery, built-wheel metadata checks, and substantial wrapper/type
parity. Remaining initiative work includes the core requirement-selection
matrix, libigl's explicit compiled-runtime requirements, package-owned OCC
built-wheel discovery evidence, the coordinated model/viewer registry test,
and the final installed cross-package review.

The approved initial implementation scope is limited to Waves 0–1:
`compas`, `compas_cgal`, `compas_libigl`, `compas_occ`, `compas_model`, and
`compas_viewer`. Optional backends, host integrations, and other ecosystem
packages require a later explicit scope amendment and approval.
