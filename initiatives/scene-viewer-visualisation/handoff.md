# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-13

## Resume here

Current phase: `Local ADR 048 checkpoint committed; ADR 049 Proposed`

The user resumed the initiative on 2026-11-13 and requested that the currently
approved work be wrapped and committed to the corresponding initiative
branches. Accepted implementation through ADR 048 is now committed locally at
the exact revisions below. Core passes 2,306 tests; Viewer passes 672 tests
with two expected offscreen native-OpenGL skips; the framework direct-source
gate passes 16 tests with one expected exact-VCS-metadata skip. Independent
review passes after correcting Data refresh on removal, clearing, and batched
deletion plus the Scene-name tree-only refresh path.

Native ADR 048, scroll, extension-style, displaced-dimension, and Spatial
Layout confirmation remains pending. The Viewer launched for a native ADR 048
check on 2026-11-13, but macOS denied the automation service screen-capture
permission, so no native pass is claimed. Hosted CI has not been refreshed
because the local commits were not pushed. Candidate artifacts remain unrun
and are required only if admission or release needs that compatibility claim.
Do not treat the initiative as fully verified or publish without explicit
approval.

The user also identified that System is a settings surface rather than a peer
session-content domain. Proposed ADR 049 recommends one modeless per-Viewer
**Viewer Settings** window for Camera, Display, and Grid and Units, leaving
Scene, Data, and Annotations in the sidebar. No ADR 049 runtime implementation
is authorized before explicit approval.

The scene foundation, contextual settings, Viewer configuration and tables,
selection, and reversible transformations governed by Accepted ADRs 001–020
are implemented and verified. The architectural watchpoint remains active:
the accepted `Data`/scene-state/extension model is authoritative, but concrete
contrary evidence should be brought back for an explicit amendment rather than
handled through speculative abstractions.

The implemented Phase 3 foundation follows Accepted ADRs 021–028 and 030.
Core owns narrow durable text, arrow, and distance annotation data (ADR 021).
Persistent dimensions snapshot declared unit and precision without implicit
conversion (ADR 022).
Legacy `Tag` and `ArrowOverlay` names and serialized paths are removed without
aliases or legacy decoding (ADR 023). Live distance inspection is transient,
while explicit fixed and associative modes create durable dimensions
(ADRs 024 and 028). Viewer owns one ordered, non-serialized scale/legend layer
(ADR 025), nearest eligible discrete-point acquisition and one-shot
measurement tools (ADR 026), and the editable Units and Measurement
presentation settings with read-only global tolerance (ADR 027). Interactive
acquisition is limited to Point, Mesh-vertex, and Graph-node guides with no
unmarked fallback. ADR 034 lets an otherwise visible Mesh expose measurement
guides without enabling its ordinary vertex glyphs.
Persistent dimensions use ADR 030's always-visible final pass. Accepted ADR
029 moves annotations out of the spatial hierarchy, adds a flat Annotations UI,
and owns a narrow durable dimension style. Accepted ADR 031 exposes the
existing spatial-object deletion command in the default Edit menu while
preserving subtree removal, independent data, transform-history invalidation,
and unresolved associative dimensions. Both implementations pass local package,
documentation, independent review, refreshed package CI, and the exact
source-installed framework gate.

Direct-use feedback shows that the current stacked sidebar resizes unrelated
panels, presents independent spatial and annotation contexts ambiguously, hides
annotation naming, and does not provide consistent background-click or Escape
deselection. Accepted ADR 032 replaces it with stable Scene, Annotations, and
System domains. The implementation, documentation, 441-test Viewer suite,
Ruff, Pyright, strict MkDocs, framework direct-source gate, and independent
review pass. Hosted package and exact source-installed integration checks also
pass.

Direct use then exposed a Qt lifecycle crash when an annotation visibility
checkbox rebuilt and deleted its own emitting tree item, plus repeated
`vertexsize` errors caused by treating an `(int, float)` field as integer-only
when its current value happened to be an integer. Both causes are fixed. The
Viewer now passes 445 tests, Ruff, Pyright, strict MkDocs, independent review,
hosted package CI, and the refreshed framework exact source-installed gate at
the revision below.

Further direct use produced ADRs 033–039. They cover the resizable
Scene inspector and Details dialog, vertex snapping with ordinary glyphs
hidden, deterministic spatial dimension offsets, screen-pinned viewport text,
label backgrounds, contextual deletion, and moving the existing geometry Add
hierarchy under Scene. ADR 036 is Accepted and implemented with a screen-pinned,
non-persistent, programmatic-first contract. ADRs 037–039 are implemented and
locally verified. ADR 037 advances Core Scene serialization to schema 4 for
durable label backgrounds and padding; ADR 038 makes deletion context-owned;
ADR 039 moves the unchanged geometry hierarchy to **Scene → Add**. Accepted
ADRs 040–042 add synchronized default-toolbar
controls, a Grid and Units System section with consistent two-column field
alignment and no tolerance UI, and transient selected-object area and volume
inspection. The four implemented follow-ups pass 501 Viewer tests, Ruff,
formatting, Pyright, strict MkDocs, independent review, the complete hosted
Viewer matrix, and the exact source-installed framework gate. ADR 034 is now
implemented, locally verified, and independently reviewed. ADR 033 was accepted
on 2026-11-11, implemented, and locally verified. ADR 035 was accepted on
2026-11-11, implemented, locally verified, and independently reviewed.

ADR 043's structural contract is Accepted. The existing `system`, `light`, and
`dark` values remain color-scheme choices for one theme; theme ownership is
limited to Qt chrome and no longer overwrites renderer or content colors. The
repositories provide no authoritative COMPAS palette, so source implementation
uses the explicitly approved Viewer-specific light/dark token table rather than
claiming an organization-wide brand standard.

ADR 043's concrete Viewer-specific light/dark token table and verified WCAG
contrast calculations were approved on 2026-11-10. Implementation is complete
in the Viewer working tree. It adds one private semantic theme,
palette-aware monochrome button icons, and semantic component presentation;
preserves the public appearance configuration; and stops appearance changes
from mutating renderer or content colors. The full 517-test Viewer suite,
Ruff, formatting, Pyright, strict MkDocs, independent review, and the framework
direct-source gate pass. Hosted package CI, native cross-platform captures,
and candidate-artifact verification remain pending.

The settled pre-ADR-034 working tree passes 2,251 Core tests, 545 Viewer tests,
package Ruff and formatting, Viewer Pyright,
focused Core source Pyright, strict Core and Viewer MkDocs, and the refreshed
framework direct-source gate with 15 passes and one expected exact-revision
skip. Full Core Pyright remains unavailable because of two unrelated existing
documentation-example errors (`Tag` import and a VolMesh call). Independent
review passes with no remaining code findings. Native direct use showed that
View combo-popup teardown could still disrupt viewport focus. The accepted
2026-11-10 ADR 040 amendment keeps the Render Mode dropdown and replaces View
with exclusive icon-only Perspective, Top, Front, Right, and Ortho buttons
using the palette-aware P, T, F, R, and O assets. Semantic titles remain
tooltips and accessible names. One event-driven pending restoration waits for
`focusWindowChanged` or a queued readiness check to observe the main window
focused and active with the popup cycle complete; no arbitrary delay or retry
loop is used. Custom text-only, text-plus-icon, and unbound buttons remain
valid; no general widget registry is added. Synchronous viewport injection populates
Camera settings before System-panel sizing, and the initial-collapse
implementation is final. The subsequent user retest confirmed initial Camera
population. The right sidebar cannot collapse below its configured minimum
width.

The 2026-11-10 amendment to ADR 029 changes only newly constructed default
dimension styles from white to magenta. Explicit and serialized colors remain
unchanged, Scene stays at schema 4, and no adaptive or universal contrast
guarantee is claimed.

ADR 034 adds a private measurement-only Mesh-vertex footprint to the active
instance/depth acquisition pass. It does not affect ordinary rendering or add
edge, face, or broader object-type candidates. The user confirms that Mesh
snapping now works properly. The completed ADR 044 tree passes 2,264 Core tests
and 575 Viewer tests plus one expected structured OpenGL skip before the final
toolbar follow-up. The final combined Viewer tree passes 587 plus the same
expected skip. Independent focused review passes 92 Core and 83 Viewer
tests. The actual-widget toolbar/theme focus suite passes 47 tests,
initialization smoke passes 61, and five native macOS toolbar/Camera probes
pass. Ruff, formatting, Viewer Pyright, strict documentation, and diff checks
pass. The framework direct-source gate
passes 15 tests with one expected exact-revision skip. Direct use confirmed
that button interaction had no focus problem before icon-only presentation was
added. The subsequent direct-use retest confirms the standard-view buttons and
Camera fix but rejects Render Mode dropdown focus. Hosted CI and
candidate-artifact verification remain pending.

The latest direct-use retest confirms the five standard-view buttons, initial
Camera population, and general presentation. Render Mode popup focus still
fails. Investigation shows the current tests force popup hiding and therefore
mask a native macOS close path that never delivers the watched `Hide` event.
Direct use also confirms that stored label backgrounds lack Annotations-detail
controls, white default surfaces lack contrast against the white viewport, and
letter glyphs do not satisfy the intended pictorial icon design. Approved ADR
037 and ADR 040 amendments add background editing and replace the popup/letter
composition with semantic render buttons, a private fixed standard-view list
over the viewport, and the existing Zoom Selected, Zoom Extents, and Capture
View actions. Accepted ADR 045 changes Viewer's fixed default viewport
background to `#D8DDE2` while Core remains white. Implementation, local
verification, direct-source framework integration, and independent re-review
pass. The user confirms the corrected Viewer works well through direct use;
hosted CI and candidate artifacts remain pending. The newer accepted
grouped-control, Details/splitter, palette, and default-background changes are
implemented, locally verified, and confirmed through native direct use.

Direct use also shows that existing dimensions need editable unit and precision
snapshots. Accepted ADR 044 preserves Grid and Units as transient/new-dimension
defaults and adds validated per-dimension Measurement Format controls in the
Annotations details panel. Its approved amendment sets the shared precision
domain to 0–15 inclusive, rejects outside values without clamping or
truncation, keeps explicit labels subject to validation, and rejects existing
data or configuration above 15 without migration or schema changes. Core and
Viewer implementation, documentation, local verification, and independent
review pass.

The Core and refreshed Viewer candidate and framework gate are green at the
revisions below. Viewer restricts acquisition to visible discrete guides,
uses an 18-logical-pixel snap radius, proves the 4 × 3 diagonal equals 5,
renders persistent dimensions above geometry, and removes the Attributes tab
from the default sidebar while retaining opt-in custom use. Local package
verification, independent review, complete Viewer package CI, and the exact
framework source-installed gate pass.

Exact candidate-artifact compatibility has not been run and must not be
inferred from source installation, package builds, or native probes.

Read next:

1. [Implementation plan](implementation-plan.md)
2. [Decision index](decisions/README.md)
3. [Proposal](proposal.md)
4. [Exploratory UI sketch](ui.md)

## 2026-11-11 environment checkpoint

The `compas3` environment contained stale `compas_libigl` editable metadata
pointing to the deleted `/private/tmp/compas-libigl-typing-adr017` checkout.
This was an editable-install path failure, not a Mach-O linkage failure. The
environment was repaired by reinstalling editable from the durable
`/Users/vanmelet/Code/compas_libigl` `c3-upgrade` checkout at
`710b2b6714839a203fc8a6c62c437c0f6735ba0e`.

The import path and `direct_url` now resolve to that durable checkout. All 13
native extension imports pass, and `otool` reports only `libc++` and
`libSystem`. This verifies the repaired local native environment only; it does
not count as candidate-artifact verification.

## 2026-11-11 approved direct-use follow-up

The user confirms the corrected Viewer works well. The approved follow-up adds one
grouped viewport menu for View and View Mode, one measurement menu button in
the toolbar, ADR 033's Details dialog, independent Scene hierarchy/details and
Annotations list/dimension-details splitters, default scheme-colored
backgrounds for newly acquired dimensions, and ADR 046's scheme-aware Viewer
content defaults. Explicit/serialized colors and
Core defaults remain unchanged; existing geometry is not recolored on a live
scheme switch. The user approved these contracts on 2026-11-11; implementation
and local verification pass.

ADR 046 advances Viewer configuration to schema 4 with
`RendererConfig.backgroundcolor: Color | None`; only `None` means automatic,
and every schema-3 concrete value migrates as explicit. Scheme geometry tokens
apply only when both base and the relevant specialized channel are omitted;
an explicit base retains current Core derivation for omitted specialized
channels.

The completed follow-up replaces the view list and toolbar render buttons with
the grouped viewport menu, adds the measurement toolbar menu, implements the
Details dialog and independent Scene/Annotations splitters, advances Viewer
configuration to schema 4 with the accepted palette, and enables the accepted
new-dimension backgrounds. The final Viewer suite passes 621 tests with one
expected offscreen OpenGL skip and exits cleanly. Independent review passes,
including popup and Escape lifecycle coverage. Ruff, formatting, configured
Pyright with zero errors, strict MkDocs with only the informational Material
end-of-life notice, and `git diff --check` pass. The direct-source framework
gate passes 15 tests with one expected exact-VCS-metadata skip.

On 2026-11-11 the user confirmed through native direct use that the grouped
viewport menu, measurement menu, Details dialog, independent splitters,
scheme-aware palette, and default dimension backgrounds work correctly. The
final custom View/View Mode menu-arrow alignment, non-overlap, and pressed-state
stability also pass direct use.

ADR 035 implementation uses an explicit **Apply Layout** boundary so tabbing
can preserve partial Spatial Layout drafts; invalid Apply and Escape restore
durable values without refresh, while Reset is immediate. Scene schema 5 uses
`SceneAnnotation` entry schema 2 because nested entries decode before the
parent Scene version is available. Versioned entries require `layout`; only
legacy unversioned schema-4 entries may omit it for binding-time migration.
Core and Viewer implementation, documentation, local verification, the
direct-source framework gate, and independent review pass. Native direct use
of ADR 035 remains pending.

Direct use then showed that shrinking the Annotations details splitter
compresses the form rather than scrolling it. The approved ADR 033 correction
uses a vertical scroll viewport whose content retains its natural size and
spacing. Its implementation and local verification pass. The user also
approved thinner extension lines. The accepted ADR 029/035 amendment keeps the existing main-line default
`3.0`, adds `extension_line_width=1.0` for new styles, and preserves schema-5
appearance through Scene schema 6, annotation-entry schema 3, and
dimension-style schema 2 migration, with the legacy extension width copied
from `line_width`. Implementation and local verification pass.

The user also requested editable resolution for parametric-shape
representations. Accepted ADR 047 reuses Core's durable `u` and `v` fields
(default `16`) and exposes only axes consumed by the represented producer. It
adds no field, alias, or schema version. Producer-specific integer validation
and one-object tessellation/buffer/bounds refresh are implemented, locally
verified, and independently reviewed. An exact native macOS subprocess changed
a Torus U resolution from 16 to 64 with a valid OpenGL context. The later
interactive crash was traced to Qt emitter lifetime and fixed. Direct user
retesting of that fix and the scroll, style, and resolution paths remains
pending.

The user subsequently approved ADR 047's settings-only refresh and wireframe
wording amendment. For ShapeObject and SurfaceObject, `show`, `show_points`,
`show_lines`, `show_surfaces`, opacity, point size, and line width must update
one object settings texture and request one redraw, without tessellation,
global buffer rebuild, or Scene tree rebuild unless displayed tree content
changed. `u` and `v` retain topology rebuilds; colors retain their current
appearance-data path. Shape/Surface forms use **Show wireframe**, **Wireframe
color**, and **Wireframe width**; Mesh/Graph retain edge wording. Durable names
do not change. Implementation, local verification, and independent review
pass. Native direct use on 2026-11-11 confirms that a Torus at U resolution 64
toggles **Show wireframe** off and on responsively, accepts the wording, and
preserves the resolution crash fix.

The user also requested access to represented data independently from the
Scene tree. Accepted ADR 048 adds a fourth read-only **Data** sidebar domain as
a GUID-deduplicated projection of spatial and annotation references. It shows
bound and unresolved items and opens modal read-only details, including lazy
Mesh/Graph attribute tables. It does not own, persist, load, resolve, edit, or
delete data. The user approved this narrow first step on 2026-11-11 and
implementation, local verification, and independent review pass. The final
sidebar order is Scene, Data, Annotations, System. Review confirms one immediate
Data refresh and no renderer refresh for direct object/reference additions,
selection preservation while the GUID remains referenced, safe shared
inspection without arbitrary `__data__`, and isolation of individual attribute
exceptions. The active Scene is the initial inventory source; a future Session
ADR may replace or extend it with unattached or multi-scene data without making
Viewer the owner.

## Exact candidates

| Repository | Branch | Verified revision | Pull request | Status |
|---|---|---|---|---|
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `fd09874eb92157e48d0c5e960078d80d58660115` | [7](https://github.com/compas-dev/compas_framework/pull/7) | Local contracts and direct-source integration passed; commit not pushed |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `9f4db763d2de0dd9bcddabd29e63bb047ac20385` | [1540](https://github.com/compas-dev/compas/pull/1540) | Local verification and independent review passed; commit not pushed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `0f263f15899b85633d5de038bec59ed8504b1142` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Local verification and independent review passed; commit not pushed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed | Core passes 2,306 tests. Viewer passes 672 tests with two expected offscreen native-OpenGL skips. Focused final review passes 74 Viewer tests. Core and Viewer Ruff and formatting, Viewer Pyright, focused changed-source Core Pyright, strict documentation builds, and `git diff --check` pass. Full Core Pyright still reports only the two unrelated existing documentation-example errors for the removed `Tag` import and a missing VolMesh argument. |
| Native interactive probes | ADR 047 passed; ADR 048 pending | An exact native macOS high-resolution Torus probe passed with valid OpenGL. Direct use on 2026-11-11 confirms responsive **Show wireframe** off/on toggling at Torus U resolution 64, the grouped controls, Camera population, splitters, palette, and dimension backgrounds. The 2026-11-13 ADR 048 launch could not be inspected because macOS denied the automation service screen-capture permission. Data, scroll, extension-style, displaced-dimension, and Spatial Layout confirmation remains pending. |
| Package CI | Stale | Core PR 1540 and Viewer PR 233 are green only for earlier published revisions. The local candidate commits above have not been pushed, so hosted package CI has not run for them. |
| Framework integration | Local passed; hosted stale | The direct-source gate passes 16 tests with one expected exact-VCS-metadata skip; its Pyright check has zero errors. Framework PR 7 is green only for an earlier published revision. |
| Candidate artifacts | Not run; conditional | No compatibility claim is made for independently built candidate artifacts. Run this layer before artifact admission or release if that claim is required. |

## Next tasks

1. Approve, amend, or reject Proposed ADR 049's modeless Viewer Settings
   surface before any runtime implementation.
2. Obtain native direct-use confirmation of ADR 048's Data tab and the pending
   scroll, extension-style, displaced-dimension, and Spatial Layout paths.
3. With explicit publish approval, push the three local candidate commits and
   refresh Core, Viewer, and framework hosted CI; run candidate artifacts only
   if admission or release requires that layer.

ADR 044 has no remaining architecture approval gate.

ADR 043's accepted content-palette amendment has no remaining architecture
gate.

## Approval gates

- ADR 033's Details dialog and independent Scene/Annotations splitters are
  Accepted and implemented; its scroll correction is implemented and locally
  verified, with native user retesting pending.
  ADR 035's deterministic layout and initial
  Spatial Layout UI are Accepted, implemented, locally verified, and
  independently reviewed; native and hosted verification remain pending.
- ADR 029/035's independent extension-line-width amendment and coordinated
  Scene-schema-6/entry-schema-3/style-schema-2 migration are implemented and
  locally verified; native user retesting remains pending.
- ADR 047's existing-field parametric-shape resolution UI is implemented,
  locally verified, independently reviewed, and native user-confirmed. Its
  settings-only refresh and wireframe wording amendment is likewise native
  user-confirmed with responsive toggling at Torus U resolution 64.
- ADR 048's read-only active-Scene Data domain is implemented, locally
  verified, and independently reviewed; native user direct use and hosted
  verification remain pending. Session aggregation, unattached data, and
  multiple-scene inventory require a separate ADR and approval; Viewer remains
  non-owning.
- ADR 049 is Proposed. Its modeless per-Viewer settings window, three-domain
  content sidebar, clean composition/API migration, and verification contract
  require explicit approval before implementation.
- ADR 037's Annotations-details amendment, ADR 040's toolbar/viewport
  amendment, and ADR 045's `#D8DDE2` Viewer background are Accepted.
- ADR 037's default-background amendment, ADR 040's grouped-control amendment,
  ADR 043's content amendment, and ADR 046 are Accepted.
- Adding model, session, notebook, or host packages requires explicit approval.
- Session aggregation and Viewer new/open/save conveniences remain future work.
- Do not merge or publish without explicit approval.
