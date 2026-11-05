# Typing Alignment

This initiative aligns Python typing across `compas`, `compas_occ`,
`compas_cgal`, and `compas_libigl`, with particular attention to NumPy and
native-library boundaries.

Current phase: **Implementation in progress; exact geometry APIs, core
structural vocabulary, and native-binding completion awaiting approval**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)

ADRs 001–014 are approved. ADRs 015–017 and Geometry ADRs 022–023 are Proposed.
Together they define the exact geometry signatures, neutral `VerticesFaces`
vocabulary, NumPy-compatible core constructors, and complete CGAL/libigl native
stub policy required to finish WP7–WP8. Work governed only by accepted decisions
may continue; the proposed slices remain blocked.

Known limitation: `compas_cgal` skeletonisation currently produces incorrect
results. Typing, stub, boundary, and packaging checks for that module do not
constitute validation of its geometric output. Correctness requires a separate
investigation and regression fixtures before skeletonisation can be reported as
verified.

`compas_libigl` joined the initiative on 2026-11-05. Its
`initiative/typing-alignment` branch starts from local `c3-upgrade` commit
`70acf99`; the first priority is repairing the remesh-along-isoline hook that
was superseded by the approved structural mesh boundary.
