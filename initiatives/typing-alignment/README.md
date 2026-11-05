# Typing Alignment

This initiative aligns Python typing across `compas`, `compas_occ`,
`compas_cgal`, and `compas_libigl`, with particular attention to NumPy and
native-library boundaries.

Current phase: **Implementation in progress; WP7.4–WP7.7 awaiting API
approval**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)

The proposal and ADRs 001–014 are approved. ADR 015 is Proposed and defines the
exact named triangulation functions, aggregate callable, producer controls,
and direct removals required to finish WP7.4–WP7.7. Those work packages remain
blocked until the user approves all exact signatures. Other approved work may
continue.

Known limitation: `compas_cgal` skeletonisation currently produces incorrect
results. Typing, stub, boundary, and packaging checks for that module do not
constitute validation of its geometric output. Correctness requires a separate
investigation and regression fixtures before skeletonisation can be reported as
verified.

`compas_libigl` joined the initiative on 2026-11-05. Its
`initiative/typing-alignment` branch starts from local `c3-upgrade` commit
`70acf99`; the first priority is repairing the remesh-along-isoline hook that
was superseded by the approved structural mesh boundary.
