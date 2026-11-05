# Typing Alignment

This initiative aligns Python typing across `compas`, `compas_occ`,
`compas_cgal`, and `compas_libigl`, with particular attention to NumPy and
native-library boundaries.

Current phase: **Implementation in progress; exact geometry APIs, core
structural vocabulary, and native-binding completion approved and pending
implementation**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)

ADRs 001–017 and Geometry ADRs 022–023 are approved. Together they define the
exact geometry signatures, layered semantic
`PointLike`/`VectorLike` and neutral `VerticesFaces` vocabulary,
NumPy-compatible core constructors, and complete CGAL/libigl native stub policy
required to finish WP7–WP8. These slices may now proceed in dependency order;
acceptance does not mean that their source or verification work is complete.

Hosted checkpoint evidence is green at the current draft-PR heads:

- core [PR 1539](https://github.com/compas-dev/compas/pull/1539),
  `4973c5fcfc53f0217a5fca20d0765e74b30459e2`;
- OCC [PR 32](https://github.com/compas-dev/compas_occ/pull/32),
  `5a4cf9701007266e517996181c8476488c4030d9`;
- CGAL [PR 81](https://github.com/compas-dev/compas_cgal/pull/81),
  `a46eecab71de5dfea6df7380d2eafb7185cc789a`; and
- libigl [PR 47](https://github.com/compas-dev/compas_libigl/pull/47),
  `86e3f1e0e02d6dc7cf9ad8049ac57c4c7d801877`.

These green checks verify the already-pushed checkpoints. They do not cover the
newly Accepted exact geometry APIs, shared type-vocabulary replacement, or full
CGAL/libigl native-stub completeness contracts, and therefore do not close the
typing initiative.

Known limitation: `compas_cgal` skeletonisation currently produces incorrect
results. Typing, stub, boundary, and packaging checks for that module do not
constitute validation of its geometric output. Correctness requires a separate
investigation and regression fixtures before skeletonisation can be reported as
verified.

`compas_libigl` joined the initiative on 2026-11-05. Its
`initiative/typing-alignment` branch starts from local `c3-upgrade` commit
`70acf99`; the pushed checkpoint includes structural plugin alignment, lazy
plugin discovery, and typed-wheel verification. The next libigl work is the
complete native-stub and public-wrapper contract in Accepted ADR 017.
