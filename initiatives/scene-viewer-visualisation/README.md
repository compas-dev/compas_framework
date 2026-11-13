# Scene, Viewer, and Visualisation

This initiative aligns backend-neutral scene infrastructure with Viewer
rendering, interaction, state, and UI composition.

Current phase: **Accepted implementation through ADR 048 is complete, locally
verified, and independently reviewed. Native ADR 048/scroll/layout/style
confirmation, hosted verification, and candidate artifacts remain pending.
ADR 049 is Proposed and not implemented.**

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
implementation, documentation, local verification, independent review,
hosted package CI, and the exact source-installed framework gate pass. Two
direct-use regressions in annotation visibility refresh and numeric field
editing are fixed and verified in hosted Viewer and framework CI. Further
direct use has produced ADRs 033–039 for a resizable Scene inspector,
hidden-glyph vertex snapping, spatial dimension layout, viewport text,
annotation label backgrounds, contextual deletion, and moving the existing
geometry Add hierarchy under Scene. ADR 036 accepts the programmatic-first
screen-text overlay. ADRs 037–039 are implemented, locally verified, and
independently reviewed.
Accepted ADRs 040–042 add synchronized toolbar controls, a coherent Grid and
Units System section with consistent field alignment, and transient
selected-object area and volume inspection. ADRs 033–035 are implemented,
locally verified, and independently reviewed. ADRs
036 and 040–042 are implemented
on the Viewer initiative branch and pass the
complete local and hosted Viewer gates plus the exact source-installed
framework gate. Exact candidate-artifact compatibility has not been run and
is not implied by the existing results.

The 2026-11-11 approved follow-up replaces the current view/render controls
with one grouped viewport menu, adds one measurement menu button, removes the
inline object-description textbox in favor of a modal Details snapshot, and
adds independent Scene and Annotations splitters. Accepted ADR 046 advances
Viewer configuration to schema 4 and owns the exact scheme-aware viewport and
creation-time content defaults; Core, explicit, and serialized colors remain
unchanged. Newly acquired Viewer dimensions receive the accepted scheme-aware
label backgrounds. Implementation, local verification, independent review, and
native direct use of the grouped controls, Details dialog, splitters, palette,
and dimension backgrounds pass. Native confirmation of the later
Annotations-details scroll correction remains pending, as does hosted
verification.

ADR 043 accepts a built-in COMPAS Viewer theme with system-following light and
dark variants. It keeps the existing appearance configuration, limits the
theme to Qt chrome, and preserves independently owned viewport and content
colors. Its exact accessible palette tokens were approved on 2026-11-10 as
Viewer-specific styling rather than an organization-wide brand standard.
Implementation, the Viewer suite, Ruff, formatting, Pyright,
strict MkDocs, independent review, and the framework direct-source gate pass.
Hosted package CI, native cross-platform captures, and candidate-artifact
verification remain pending.

ADR 037 adds durable optional label backgrounds and logical-pixel padding to
text and distance annotations, advances Core Scene serialization to schema 4,
and gives screen-text overlays equivalent transient fields. ADR 038 makes
Delete Selected context-owned without crossing spatial and annotation
selections. ADR 039 moves the unchanged geometry hierarchy to **Scene → Add**.
The amended toolbar keeps the Render Mode dropdown and replaces the native View
combo popup with exclusive icon-only Perspective, Top, Front, Right, and Ortho
buttons using palette-aware P, T, F, R, and O assets. Semantic titles remain
tooltips and accessible names. One event-driven pending focus request restores
the renderer only after the main window is focused and active and the popup
cycle is complete; no arbitrary delay or retry loop is used. The buttons use
the existing command and state path; custom text-only, text-plus-icon, and
unbound buttons remain supported, and no general widget registry is
introduced. Synchronous
viewport injection populates Camera settings before System-panel sizing, and
the Camera section's initial-collapse implementation is final. Direct use
confirmed initial Camera population and the corrected controls. The right
sidebar cannot collapse below its configured minimum width.

The 2026-11-10 amendment to ADR 029 changes only newly constructed default
dimension styles from white to magenta. Explicit and serialized colors remain
unchanged, Scene stays at schema 4, and no universal contrast behavior is
claimed. The final tree passes 2,264 Core tests. Viewer passes 575 tests plus one
expected structured OpenGL skip before the final toolbar follow-up; the final
combined Viewer tree passes 587 plus the same expected skip. Independent focused
review passes 92 Core and 83 Viewer tests. The actual-widget
toolbar/theme focus suite passes 47
tests, initialization smoke passes 61, and five native macOS toolbar/Camera
probes pass. Ruff,
formatting, Viewer Pyright, strict documentation, and diff checks pass. The
framework direct-source gate passes 15 tests with one expected exact-revision
skip. The user confirmed ADR 034 Mesh snapping works properly and confirmed
that button interaction had no focus problem before the icon-only presentation
was added. Later native direct use confirmed the corrected render/view controls
and Camera population; the grouped-menu amendment then superseded that interim
composition and also passed direct use. Hosted CI and candidate artifacts have
not run for these working trees. Broader acquisition object types remain a
separate follow-up.

Accepted ADR 044 adds validated Coordinate Unit and Display Precision controls
for exactly one selected persistent distance dimension while preserving Grid
and Units as defaults for transient and newly created measurements. Its
approved amendment sets one Core and Viewer precision domain of 0–15 inclusive:
outside values raise `ValueError` without clamping or truncation, explicit
labels do not relax validation, and existing data or configuration above 15 is
rejected without migration or a schema change. Validated Core properties and
Viewer Measurement Format controls are implemented, locally verified, and
independently reviewed under the verification baseline above.

The refined initial package scope is `compas`, `compas_viewer`, and
`compas_framework`. The current `compas_model.ModelViewer` is draft evidence
and a later redesign consumer, not a behavior contract. Session persistence,
notebook visualisation, and CAD-host adapters are compatibility-review
consumers until an approved decision admits them to implementation scope.
