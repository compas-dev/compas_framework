# Typing Alignment

This initiative aligns Python typing across `compas`, `compas_occ`,
`compas_cgal`, and `compas_libigl`, with particular attention to NumPy and
native-library boundaries.

Current phase: **Complete for the approved source, distribution, and installed
integration scope**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)

ADRs 001–017 and Geometry ADRs 022–023 are approved. Together they define the
exact geometry signatures, layered semantic
`PointLike`/`VectorLike` and neutral `VerticesFaces` vocabulary,
NumPy-compatible core constructors, and complete CGAL/libigl native stub policy
required for WP7–WP8. The source slices and exact installed-candidate evidence
are complete without adding typing-only runtime conversions.

Current draft-PR heads are:

- core [PR 1539](https://github.com/compas-dev/compas/pull/1539),
  `99b82a6673ff7d05c1c323c8921135c274993f11`;
- OCC [PR 32](https://github.com/compas-dev/compas_occ/pull/32),
  `7fdf2ffb57d1de16308020e14ec626d79e65a034`;
- CGAL [PR 81](https://github.com/compas-dev/compas_cgal/pull/81),
  `bb3624e714719d543c61768320d91811ba96cc6c`; and
- libigl [PR 47](https://github.com/compas-dev/compas_libigl/pull/47),
  `710b2b6714839a203fc8a6c62c437c0f6735ba0e`.

All four packages have complete green hosted evidence at those heads. CGAL run
`42231235319` attempt 1 passed quality, minimum/current NumPy, sdist, every
platform wheel build, and all Python 3.12/3.14 wheel-smoke jobs.

WP7.4–WP7.7 and WP8.1 are source-complete. CGAL WP8.2 and libigl WP8.3 reach
the approved native-stub/public-wrapper contract and are hosted green.
Framework draft
[PR 2](https://github.com/compas-dev/compas_framework/pull/2) implements the
WP8.4 exact-artifact mechanism and live manifest at
`f719e505c990004b60ee23fa5c2446fa4f2ae2dd`. Schema/semantic validation,
exact hashes, offline revalidation and staging, versions, installed plugin/OCC
behavior, strict exact-wheel typing, and all 54 focused contract/tooling checks
pass locally.

The framework build, docs, candidate-contract/actionlint, package, and release
metadata workflows are green at that head. Protected run
[`42246941037`](https://github.com/compas-dev/compas_framework/actions/runs/42246941037)
also passes exact artifact retrieval and secret-free Linux execution: all four
required installed runtime contracts pass without skips, including the
CGAL→core→libigl and OCC paths, and the external typing consumer reports zero
errors and warnings. WP8.4 and final WP6 are therefore complete. `main` remains
untouched.

Known limitation: `compas_cgal` skeletonisation currently produces incorrect
results. Typing, stub, boundary, and packaging checks for that module do not
constitute validation of its geometric output. Correctness requires a separate
investigation and regression fixtures before skeletonisation can be reported as
verified.

`compas_libigl` joined the initiative on 2026-11-05. Its
`initiative/typing-alignment` branch starts from local `c3-upgrade` commit
`70acf99`; the current hosted-green checkpoint includes structural plugin
alignment, lazy plugin discovery, complete native stubs and public wrappers,
and installed-wheel verification under Accepted ADR 017.
