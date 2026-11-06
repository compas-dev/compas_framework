# Typing Alignment

This initiative aligns Python typing across `compas`, `compas_occ`,
`compas_cgal`, and `compas_libigl`, with particular attention to NumPy and
native-library boundaries.

Current phase: **Source implementation complete at the coordinated candidate
heads; exact installed integration and the protected hosted positive remain
open**.

- [Objective](objective.md)
- [Inventory](inventory.md)
- [Proposal](proposal.md)
- [Architecture decisions](decisions/README.md)
- [Implementation plan](implementation-plan.md)

ADRs 001–017 and Geometry ADRs 022–023 are approved. Together they define the
exact geometry signatures, layered semantic
`PointLike`/`VectorLike` and neutral `VerticesFaces` vocabulary,
NumPy-compatible core constructors, and complete CGAL/libigl native stub policy
required for WP7–WP8. The source slices are implemented without adding
typing-only runtime conversions; final completion still depends on exact
installed-candidate evidence.

Current draft-PR heads are:

- core [PR 1539](https://github.com/compas-dev/compas/pull/1539),
  `99b82a6673ff7d05c1c323c8921135c274993f11`;
- OCC [PR 32](https://github.com/compas-dev/compas_occ/pull/32),
  `7fdf2ffb57d1de16308020e14ec626d79e65a034`;
- CGAL [PR 81](https://github.com/compas-dev/compas_cgal/pull/81),
  `7537d58154f62f38c0b2d4118972d0a326f86c9b`; and
- libigl [PR 47](https://github.com/compas-dev/compas_libigl/pull/47),
  `710b2b6714839a203fc8a6c62c437c0f6735ba0e`.

Core, OCC, and libigl have complete green hosted evidence at those heads. CGAL
passes its source and local installed-wheel typing contracts. Hosted run
`42224203204` completed with Linux and both macOS wheel smoke passing, but
Windows 3.12 and 3.14 failed installed `--verifytypes` with
`No py.typed file found` and zero symbols. A corrected fresh successful run is
required.

WP7.4–WP7.7 and WP8.1 are source-complete. CGAL WP8.2 and libigl WP8.3 reach
the approved native-stub/public-wrapper contract; libigl is hosted green and
CGAL awaits that corrected hosted result. Framework draft
[PR 2](https://github.com/compas-dev/compas_framework/pull/2) implements the
WP8.4 exact-artifact mechanism and passes its credential-free contracts, but
the live four-package manifest awaits the successful CGAL artifact. The final
trusted positive also requires the separately configured protected GitHub App
environment. Until those steps pass, WP8.4 and WP6 remain open and the typing
initiative is not complete.

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
