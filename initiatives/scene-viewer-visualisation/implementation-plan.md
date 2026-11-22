# Scene, Viewer, and Visualisation Implementation Plan

## Status

Architecture correction implemented and verified. ADRs 013–014 are Accepted
and supersede the adapter model. Accepted ADRs 015–016 govern
`SceneStateField`-backed editability, non-state editable declarations, and
contextual overrides; the superseded implementations were replaced and the
amended contract is independently approved and green in package and
exact-candidate integration CI. Accepted ADRs 017–020 are implemented, locally
verified, and independently approved in their required order: ADR 019, ADR 020,
ADR 017, then ADR 018. Their hosted verification passed. ADR 003 object
selection is now implemented, locally verified, independently approved, and
green in the hosted Viewer matrix and refreshed exact-candidate verification.
ADR 004 transformations, refresh, and undo is implemented, locally verified,
independently approved, and green in refreshed package and exact-candidate
verification. Accepted ADRs 021–028 are implemented, locally verified,
independently approved, and green in Core and Viewer package CI and the
framework exact source-installed gate. Phase 3 source implementation and
integration through ADR 048 are complete. ADR 049 was accepted on 2026-11-14;
its Viewer Settings implementation, local verification, direct-source
integration, and independent re-review pass. Native macOS confirmation and
refreshed hosted CI remain pending. Exact candidate-artifact compatibility
remains a separate, unrun verification layer. ADRs 050–052 are independent
Accepted decisions: ADRs 050–051 govern runtime inspection changes, while ADR
052 governs documentation quality and authorizes no runtime change. Their
implementation, local package and documentation verification, direct-source
integration, and independent review pass in the uncommitted working trees.
Native interaction/visual checks, refreshed hosted CI, and candidate artifacts
remain separately pending.

## Dependency graph

```text
ADR 001 --> ADR 008 --> ADR 009 --> ADR 010
    |
    +--------> ADR 002
    +--------> ADR 003 --> ADR 004

ADRs 001–003 ----------> ADR 005
ADRs 001, 003–005 -----> ADR 006
ADRs 001–010 ----------> ADR 007 rollout gate
```

## Phase 0 — Scene ownership and serialization amendment

Governing ADRs: 001, 008, 009, and 010.

Status: implemented and verified after the Accepted ADR 013–014 correction.

1. Add the verified Viewer round-trip regression and a minimal core adapter
   test covering the constructor-before-attachment failure. Keep the actual
   draft ModelViewer failure as evidence for its later redesign.
2. Audit Scene, SceneObject, Group, Viewer adapters, the draft model adapters,
   and compatibility-only consumers against the proposed node/adapter split.
3. Implement the closed scene node/state schema, durable node GUIDs,
   reference-only descriptions, runtime item bindings, and two-phase
   deserialize/bind lifecycle.
4. Implement explicit MRO-composed extension field declarations; preserve
   unknown namespaced extension state within the new schema.
5. Migrate core and Viewer adapters without serializing caches, selection,
   construction commands, or runtime handles. Use the draft ModelViewer failure
   as external regression evidence, not as behavior to preserve.
6. Document the separate future Session aggregation boundary without adding a
   `SceneBundle`, URI resolver, asset registry, or Session implementation.

Exit gate: the Viewer and minimal-adapter regressions pass; shared item
identity and durable node identity round-trip separately; scenes load without
a visualization backend; runtime adapters bind only after the complete
hierarchy exists; independently loaded items bind without copying; unresolved
references follow ADR 010; local/package quality, typing, docs, and artifact
checks pass.

## Phase 1 — Boundaries and indexed geometry

Governing ADRs: 001, 002, 007, 008, 009, and 010.

Status: implemented and verified.

1. Audit compatibility-only consumers for affected core scene contracts and
   stop for approval if a required core change would break them.
2. Implement indexed `BufferGeometry` and convenience constructors in Viewer.
3. Migrate Viewer adapters and buffer assembly without expanding indexed data.
4. Add performance-regression assertions based on buffer/object counts rather
   than unstable wall-clock thresholds.

Exit gate: package-local source, typing, artifact, rendering-semantic, and
large-indexed-input evidence passes at exact candidate heads.

## Phase 2 — State, selection, and transforms

Governing ADRs: 001, 003, 004, 007, 008, and 009.

Status: ADR 003 object selection is implemented, locally verified, and
independently approved on the verified ADR 013–014 scene foundation. The hosted
Viewer matrix and exact-candidate verification passed. ADR 004 transformations,
refresh, and undo is implemented, locally verified, and independently approved;
hosted package and exact-candidate verification passed.

1. [Complete] Separate persistent Viewer configuration from transient Viewer
   state.
2. [Complete] Implement the object-selection model and migrate viewport,
   rectangle, tree, commands, renderer settings, and programmatic Viewer APIs.
3. [Complete] Remove scene-owned selection as a second authority and update
   serialization/tests. Keep only the read-only scene-object projection needed
   by rendering.
4. [Complete] Add atomic multi-object transform transactions, categorized
   refresh, and the Viewer-level reversible transaction stack.
5. [Complete] Add the transform-selected command and undo/redo menu operations
   after command/programmatic semantics passed. No transform-input UI was
   invented; visual gizmo design remains a follow-up if it requires new
   choices.

Exit gate: all selection paths share one model; transform/undo tests cover
parents, batches, failures, world/local conversion, cached descendant bounds,
history invalidation, and buffer-update scope. The local gate passed; hosted
package and exact-candidate verification passed.

## Contextual object-settings work

Governing ADRs: 013, 014, 015, and 016.

Status: implemented and independently verified under amended Accepted ADRs
015–016.

Implementation record:

1. Removed the public `FormField` API, item-target bindings, field refresh
   modes, the parallel built-in Viewer field inventory, and the first separate
   `EditableAttribute` implementation.
2. Added `editable` and the optional atomic data-only `update` callback to
   `SceneStateField`, rejecting `update` when the field is not editable.
3. Reserved `__editable_attributes__` for non-state fields, initially `name`
   and `opacity`, and composed both MRO sources through
   `SceneObject.editable_attributes()` without duplicate subclass names.
4. Added graphics-free context contributions that filter, extend, or replace
   entries through the same mapping with exact registry keys, deterministic
   lexical contribution ordering, and conflict errors.
5. Migrated object settings to infer presentation and writability from the
   normalized mapping and current values; represented-item parameters remain
   in `ParameterForm`.
6. Applied default assignment or the optional synchronous data-side callback
   atomically; Viewer conservatively rebuilds/redraws/refreshes after success
   only.
7. Verified source composition, removal, conflicts, rollback, graphics-free
   discovery, serialization exclusion, and multiple contexts.

Exit gate: passed. Durable semantic attributes use `SceneStateField` as their
single source; non-state names are declared once; context plugins only modify the
normalized mapping; Viewer exclusively owns form UI and post-mutation refresh;
core exposes no form or refresh protocol; all applicable core, Viewer, and
framework integration checks pass.

## Viewer identity and configuration lifecycle

Governing ADRs: 019 and 020.

Status: implemented, locally verified, independently approved, and passed in
hosted package and exact-candidate verification.

Implementation record: ADR 019 was completed first. ADR 020 followed because
its schema validation and startup application depend on the accepted identity
contract.

1. Applied validated startup configuration before Qt application/window
   construction and connected title, icon, dimensions, and fullscreen.
2. Retained dataclasses, added path-aware validation, and separated startup
   configuration from transient Viewer state.
3. Implemented the schema-2 field audit and migration/rejection behavior.
4. Verified identity, icons, fullscreen, status bar, every field disposition,
   setup-only mutation semantics, serialization, and typed subclass extension.

Local exit gate: passed. Startup identity and configuration are validated and
effective; removed fields are absent; transient state is not serialized.

## Datastructure attribute tables

Governing ADRs: 006, 017, and 018.

Status: implemented, locally verified, independently approved, and passed in
hosted package and exact-candidate verification after ADRs 019–020 established
configuration and sidebar ownership.

Implementation record:

1. Added lazy Mesh and Graph element-attribute table models using declared
   default mappings and singular domain APIs.
2. Added sidebar tabs only for domains with declared columns, preserved mapping
   insertion order, and omitted sparse undeclared attributes.
3. Added supported scalar delegates, singular setter/unset mutation, effective
   values, local selection, and conservative Viewer refresh.
4. Verified laziness, large/empty structures, value types, reset behavior,
   atomic failure, and excluded first-version features.

Local exit gate: passed. Tables are lazy, declared-domain-driven, Viewer-owned,
and verified without core API changes. The component is opt-in for custom
sidebars after the 2026-11-09 amendment to ADR 017; it is not part of the
built-in sidebar.

The implementation order was ADR 019, ADR 020, ADR 017, then ADR 018.
Configuration work established startup and sidebar visibility ownership before
the tables followed. The architectural watchpoint recorded in the proposal
remains active during integration verification; concrete contrary evidence
must be brought back without inventing a replacement model speculatively.

## Phase 3 — Annotations and overlays

Governing ADRs: 001–005, 007, and 021–042.

Status: the discrete-only acquisition, 18-pixel attraction, always-visible
persistent-dimension pass, and default-sidebar refinement are verified locally
and in hosted package and exact source-installed integration CI. ADRs 029 and
031 are implemented, independently reviewed, and verified locally across Core,
Viewer, the direct-source framework gate, and refreshed hosted CI. Direct-use
feedback identified a separate sidebar-composition defect; ADR 032 accepts
the replacement. Its implementation, documentation, local verification,
framework direct-source gate, and independent review pass; hosted refreshes
also pass. Interactive confirmation of the existing measurement refinement
remains pending.
ADR 023 provides the clean break with no aliases or legacy decoding. ADR 024
separates transient inspection from
persistent dimensions. ADR 028 defines one dimension type with fixed and
associative anchors, snapping in both UI modes, no silent fallback, and
explicit unresolved references. ADRs 021–022 place narrow durable annotation
data in `compas.scene` and define persistent unit/precision snapshots without
implicit conversion. ADR 025 governs the ordered scale/legend overlay layer.
ADR 026 governs nearest eligible discrete-point acquisition and the one-shot
tool lifecycle. ADR 027 governs Viewer measurement presentation settings and the
Units and Measurement UI. ADR 030 governs the always-visible persistent
dimension pass. ADR 029 governs the approved separate annotation collection,
flat UI, and narrow dimension style. ADR 031 governs discoverable spatial
deletion without expanding history or cascading to annotations.

1. [Complete] Inspect current `Tag`/`ArrowOverlay` serialized behavior and
   approve the clean-break migration in ADR 023.
2. [Complete] Separate transient measurement inspection from persistent
   dimension-annotation outcomes in ADR 024.
3. [Complete] Define fixed and associative persistent dimension anchors in ADR
   028.
4. [Complete] Approve core ownership/schema and persistent unit/precision
   snapshots in ADRs 021–022.
5. [Complete] Approve Viewer unit/precision presentation and read-only global
   tolerance UI in ADR 027.
6. [Complete] Implement world text, arrow, and distance annotation scene
   items and Viewer render objects.
7. [Complete] Implement the approved transient inspection plus fixed/associative
   persistent dimension snapping, preview, cancel, and completion.
8. [Complete] Implement the approved scale and legend screen overlays through
   one Viewer overlay layer.
9. [Complete] Keep overlay dispatch outside the main scene render loop and
   remove the obsolete Viewer annotation implementations.
10. [Complete] Restrict interactive acquisition to visible Point,
    Mesh-vertex, and Graph-node guides with an 18-logical-pixel radius.
11. [Complete] Render persistent distance dimensions in ADR 030's final pass
    without depth testing or depth writes.
12. [Complete and verified] Move persistent annotations out
    of the spatial hierarchy, add a flat Annotations UI, and expose ADR 029's
    narrow durable style.
13. [Complete and verified] Expose the existing
    `viewer.delete_selected` command in the default Edit menu while preserving
    subtree removal, independent data, transform-history invalidation, and
    unresolved associative dimensions.
14. [Complete and verified] Replace the
    mixed stacked sidebar with stable Scene, Annotations, and System domains;
    add explicit annotation details and the approved global deselection
    behavior.
15. [Complete; locally verified and user-confirmed] Remove the inline
    description textbox, add the modal Details dialog, and add independent
    resizable Scene hierarchy/details and Annotations list/dimension-details
    boundaries. [Complete; locally verified] Wrap the Annotations details
    surface in a vertical scroll viewport so shrinking its splitter allocation
    does not compress the form below its natural height.
16. [Complete and verified] Make Mesh vertices measurable
    independently of ordinary vertex-glyph visibility without adding edge or
    face snapping. Broader object-type acquisition follows only after this
    contract is stable and separately approved.
17. [Complete; locally verified and independently reviewed] Add deterministic world-space
    dimension offsets from a captured plane normal, including extension lines,
    explicit unresolved layout behavior, schema-5/entry-schema-2 migration,
    and the atomic single-dimension Spatial Layout details form with an
    explicit Apply boundary. Dragging, construction-plane tools, collision
    avoidance, and multi-edit remain excluded. [Complete; locally verified] Add an
    independently durable extension-line width,
    defaulting new styles to dimension/extension widths `3.0/1.0`, with the
    schema-6 migration that preserves legacy appearance.
18. [Complete and verified] Add screen-pinned viewport text as a Viewer
    overlay through the existing programmatic overlay API; do not add an
    incomplete interactive management surface or persistence until their
    ownership is approved.
19. [Complete; local verification passed] Add the narrow optional label
    background and padding presentation fields.
20. [Complete; local verification passed] Dispatch Delete Selected to the active
    Scene or Annotations interaction domain without deleting both selections.
21. [Complete; local verification passed] Move the existing geometry Add
    hierarchy under Scene while retaining measurement acquisition under
    Measure.
22. [Complete and verified] Establish Camera, Display, and Grid and Units
    ownership; remove tolerance from Viewer UI; and align all System form
    fields on one two-column layout.
23. [Complete and verified; amended 2026-11-10] Add the visible-by-default
    Render Mode dropdown and exclusive icon-only Perspective, Top, Front,
    Right, and Ortho buttons synchronized through existing state and commands;
    restore focus through observable window and popup readiness.
24. [Complete and verified] Add transient selection-driven area and
    volume inspection with exact supported transform scaling and explicit
    unsupported cases.

Exit gate: the ADR-029/031 candidate passed local Core, Viewer, documentation,
independent review, refreshed package CI, and exact source-installed framework
integration verification. Durable annotations round-trip and resolve through
fixed and associative anchors; transient
inspection and overlays do not serialize; only visible discrete guides produce
interactive anchors; fixed and associative acquisition do not fall back; and
persistent dimensions remain visible over scene geometry. Direct-use
confirmation of the refined attraction and presentation remains pending.
Independently built exact candidate artifacts were not installed together and
remain a separate unrun layer. The sidebar usability follow-up does not
invalidate those verified storage, rendering, or deletion contracts.

ADR 032's replacement sidebar also passes its local package, documentation,
direct-source integration, independent-review, hosted package, and exact
source-installed integration gates. Direct-use regressions in annotation
visibility refresh and numeric field-type inference are fixed and verified in
hosted Viewer and framework CI. ADRs 036 and 040–042 are implemented and pass
the complete local and hosted Viewer gates plus the exact source-installed
framework gate. ADRs 037–039 are implemented and locally verified. ADR 037
advances Core Scene serialization to schema 4 for durable annotation-label
backgrounds and padding. ADR 034 is implemented, locally verified, and
independently reviewed. ADR 033 was accepted on 2026-11-11, implemented,
locally verified, and user-confirmed. ADR 035 was accepted on 2026-11-11 and
is implemented, locally verified, and independently reviewed. Native direct
use and hosted verification remain pending.

The settled pre-ADR-034 working tree passes 2,251 Core tests, 545 Viewer tests,
package
Ruff and formatting, Viewer Pyright, focused Core source Pyright, strict Core
and Viewer MkDocs, and the framework direct-source gate with 15 passes and one
expected exact-revision skip. Full Core Pyright remains blocked by two
unrelated existing documentation-example errors. Independent review passes.
Native confirmation, refreshed hosted CI, and candidate-artifact verification
remain pending for the pre-ADR-034 changes at this checkpoint.

The completed ADR 044 tree passes 2,264 Core tests and 575 Viewer tests plus one
expected structured OpenGL skip before the final toolbar follow-up. The final
combined Viewer tree passes 587 plus the same expected skip. Independent focused
review passes 92 Core and 83 Viewer tests with no remaining findings.
The actual-widget toolbar/theme focus suite passes 47 tests, initialization
smoke passes 61 tests, and five native macOS toolbar/Camera probes pass. Package
Ruff, formatting, Viewer Pyright, strict Core and Viewer MkDocs, and diff checks pass.
The framework direct-source gate passes 15 tests with one expected
exact-revision skip. The user confirms ADR 034 Mesh snapping works properly and
confirmed that button interaction had no focus problem before the icon-only
presentation was added. Later native direct use confirmed the corrected
render/view controls and Camera population; the grouped-menu amendment then
superseded that interim composition and also passed direct use. Hosted CI and
candidate-artifact verification have not run for these working trees. Broader
object types remain a separate follow-up.

The accepted 2026-11-10 ADR 029 amendment changes only newly constructed
default dimension styles from white to magenta. Explicit and serialized colors
remain unchanged, Scene stays at schema 4, and no universal contrast guarantee
or adaptive recoloring is added. ADR 034's later verification is recorded
separately from this settled baseline.

## Built-in COMPAS Viewer theme

Governing ADR: 043.

Status: structural contract and exact Viewer-specific accessible token table
accepted. Implementation, local package verification, independent review, and
the framework direct-source gate pass. Hosted package, native cross-platform,
and candidate-artifact verification remain pending.

1. [Approved] Use ADR 043's COMPAS Viewer-specific palette rather than claim an
   authoritative organization-wide brand standard.
2. [Approved] Adopt ADR 043's semantic light/dark tokens and contrast criteria.
3. [Complete] Implement a private Viewer theme module while preserving the existing
   `system`, `light`, and `dark` configuration values and schema 3.
4. [Complete] Remove appearance-driven renderer-background mutation and verify that all
   renderer and content colors retain their existing ownership.
5. [Complete] Reconcile component-local presentation, including the System-section
   heading refinement, without adding a public theme framework.
6. [Partial] Offscreen behavior, package quality, documentation, independent
   review, and exact-source framework integration pass. Native rendering on
   macOS, Windows, and Linux remains pending.

Exit gate: the approved palette and contrast evidence are recorded; runtime
switching and system-following behavior pass; explicit viewport/content colors
survive appearance changes; native captures cover both variants on supported
platforms; and all applicable verification layers are reported without
inference.

## Persistent-dimension format editing

Governing ADR: 044.

Status: accepted; implemented, locally verified, and independently reviewed.

1. [Complete] Add atomic validated `DistanceDimension.unit` and `.precision`
   properties with one 0–15 precision domain and without changing serialized
   fields or Scene schema.
2. [Complete] Apply the same 0–15 domain to Viewer configuration and
   selected-dimension Measurement Format controls, keeping them separate from
   entry style and hidden for unsupported selection states.
3. [Complete] Refresh only the affected annotation while preserving identity, anchors,
   style, selections, Viewer defaults, hierarchy, and spatial buffers.
4. [Complete] Verify 0 and 15 boundaries, rejection without clamping at -1
   and 16, explicit-label precedence without relaxed validation, editor Escape,
   default snapshot behavior, existing-data/config rejection, package quality,
   documentation, and framework integration.

Exit gate: existing dimensions are safely editable without retroactive default
propagation or unit conversion, and all applicable verification layers are
recorded.

## Phase 4 — Public Viewer operations

Governing ADRs: 001, 003–007.

Status: partially satisfied by the implemented selection, transform,
measurement, annotation, overlay, menu, and documentation work. Audit the
remaining example and custom-dock scope before adding more API.

1. Add public refresh, history, command/menu, dock, annotation, and overlay
   operations required by approved Viewer-owned features.
2. Add direct script examples for indexed buffers, selection, transforms,
   measurements, overlays, and one custom dock.
3. Update core and Viewer documentation using repository skills and
   current MkDocs-compatible NumPy style.

Exit gate: Viewer-owned tools and components use public Viewer operations and
package-local tests/docs/artifacts pass.

## Later phase — compas_model redesign

The current `ModelViewer` is a draft and is not migrated as a compatibility
exercise. A later approved design may replace its controller, hierarchy
projections, selection, caching, and UI composition. It should consume proven
core Scene and Viewer contracts where they fit, and propose additions only for
new demonstrated requirements.

## Phase 5 — Framework integration and review

Governing ADR: 007.

1. [Complete] Verify installed core Scene and Viewer behavior at exact
   candidates; keep the separate plugin initiative's model/viewer lifecycle
   gate independent.
2. [Complete] Install exact candidate revisions and exercise the approved cross-package
   runtime and typing contracts.
3. [In progress] Core and Viewer package CI, refreshed framework CI, and
   independent code/documentation review passed. Exact candidate-artifact
   verification has not run; decide whether it is applicable before admission.
4. [In progress] Findings are resolved and the handoff records evidence by
   layer. Explicit merge approval remains pending.

Exit gate: all applicable verification layers pass at recorded exact heads;
required unavailable evidence remains an explicit blocker.

## Approved direct-use presentation correction

Governing decisions: approved amendments to ADRs 037 and 040, plus Accepted
ADR 045.

Status: implementation, local verification, direct-source framework
integration, independent re-review, and user direct-use confirmation pass.
Hosted CI and candidate-artifact verification remain pending.

1. [Complete; locally verified] Add selected-annotation controls for
   enabling, coloring, and padding the already supported optional label
   background.
2. [Complete; locally verified] Replace the failing default Render
   Mode popup with four exclusive semantic cube-icon buttons; replace the
   P/T/F/R/O toolbar group with a private fixed viewport control for
   Perspective, Top, Front, Right, and Ortho; and add command-backed Zoom
   Selected, Zoom Extents, and Capture View toolbar buttons.
3. [Complete; locally verified] Resolve the default white-surface/white-viewport contrast by
   changing Viewer's fixed default viewport background to `#D8DDE2`. Core's
   default surface color remains white.

Exit gate: native interaction confirms immediate viewport orbit, pan, and zoom
after every render/view choice; toolbar, viewport control, menu, System panel,
and public API stay synchronized without recursive commands; label-background
edits persist and refresh only the affected annotation; icons pass light/dark,
high-DPI, accessibility, and provenance checks; and all applicable package,
documentation, integration, native-platform, and candidate-artifact layers are
reported separately.

Local evidence: the full Viewer suite passes 596 tests with one expected
offscreen OpenGL skip; six focused corrected-contract tests and independent
re-review pass; Ruff, formatting, configured Pyright, strict MkDocs, and
`git diff --check` pass. The direct-source framework gate passes 15 tests with
one expected exact-VCS-metadata skip. User direct use passes; hosted CI and
candidate artifacts remain unverified.

## Approved compact controls, splitters, and scheme-aware content follow-up

Governing decisions: Accepted ADR 033, accepted ADR 037 and ADR 040
amendments, accepted ADR 043 amendment, and Accepted ADR 046 superseding ADR
045.

Status: implemented, locally verified, independently reviewed, and confirmed
through native direct use. Native confirmation of the later
Annotations-details scroll correction and hosted verification remain pending.

1. [Complete; locally verified] Replace current viewport and toolbar view/render controls with one
   private grouped viewport menu, and add one default measurement menu button
   using existing commands.
2. [Complete; locally verified] Remove the inline object description, add the modal Details
   snapshot, and add independent resizable Scene hierarchy/details and
   Annotations list/dimension-details splitters.
3. [Complete; locally verified] Apply the approved exact light/dark Viewer content tokens at
   creation time and enable matching backgrounds for Viewer-created distance
   dimensions, without changing Core defaults or explicit/serialized colors.
   Advance Viewer configuration to schema 4 with
   `RendererConfig.backgroundcolor: Color | None`; migrate every schema-3
   concrete background as explicit and use `None` only for the new automatic
   viewport.

Exit gate: native interaction proves grouped-menu focus and synchronization;
measurement start/cancel paths and Details snapshots pass; exact light/dark
captures match the approved palette; explicit and serialized presentation is
unchanged; existing objects are not recolored on scheme switches; and all
applicable package, documentation, framework, hosted, and artifact layers are
reported separately.

## Approved editable parametric-shape resolution

Governing decision: Accepted ADR 047.

1. [Complete; locally verified] Expose existing durable `u` and `v`
   scene-state fields only for Shape and Surface producers that consume them.
2. [Complete; locally verified] Validate whole integers atomically with producer-specific minima
   and Capsule's even-V requirement; reject invalid edits without refresh.
3. [Complete; locally verified] Rebuild only the affected object's tessellation, buffers, bounds,
   renderer, and Scene details; verify persistence and unchanged analytic
   geometry, selection, and unrelated objects.
4. [Complete; locally verified] Route `show`, `show_points`, `show_lines`,
   `show_surfaces`, opacity, point size, and line width through one selected
   object settings-texture update and one redraw. Verify that unchanged tree
   content causes no tessellation, global buffer rebuild, or Scene tree rebuild.
5. [Complete; locally verified] Use **Show wireframe**, **Wireframe color**, and
   **Wireframe width** for ShapeObject and SurfaceObject forms. Keep MeshObject
   and GraphObject edge wording and retain every durable field/API name.

Color edits remain on the current appearance-data refresh path. Optimizing
that path is not part of this amendment. `u` and `v` remain topology edits and
retain the approved rebuild path.

No new resolution field, alias, schema version, adaptive LOD, global default,
or backend tessellation contract is authorized by this proposal.

Core passes 2,306 tests. Viewer passes 656 tests with two expected offscreen
native-OpenGL skips for renderer snapping and shape resolution. Ruff,
formatting, Pyright, strict documentation builds, framework integration (15
passes and one exact-VCS skip), diff checks, and independent review pass. An
exact native macOS Torus U 16-to-64 subprocess passed with valid OpenGL. Native
direct use confirms the Qt emitter-lifetime crash fix, responsive off/on
wireframe toggling at Torus U resolution 64, and the wireframe wording. The
scroll and extension-style paths still require native direct user retesting;
hosted CI and candidate artifacts remain pending. The settings-only refresh
and wireframe wording amendment also passes independent review.

## Accepted referenced Data domain

Governing decision: ADR 048, accepted on 2026-11-11. Implementation, local
verification, and independent review pass.

1. [Complete] Add a fourth read-only Data sidebar domain
   projecting one row per distinct Scene-referenced item GUID in deterministic
   first-reference order.
2. [Complete] Keep Data selection local; show bound/unresolved status and all
   referring objects/annotations without implicit resolution or ownership.
3. [Complete] Add a modal read-only Data Details snapshot and reuse lazy
   Mesh/Graph tables read-only; verify refresh without data or buffer mutation.

No unattached storage, Session aggregate, loading/resolution, editing,
deletion, search, persisted selection, or modeless inspector is authorized.
The active Scene is the initial inventory source. Replacing or extending it
with an unattached or multi-scene Session aggregate requires a separate ADR;
Viewer must not become the aggregate owner.

The ADR 048 checkpoint sidebar order is Scene, Data, Annotations, System.
Accepted ADR 049 replaces that System placement with a separate Viewer Settings
window. ADR 048 review confirms that direct `add_object` and `add_reference`
calls cause one immediate Data refresh and no renderer refresh, selection is
preserved while its GUID remains referenced, generic inspection does not use
arbitrary `__data__`, and an
individual attribute exception is isolated. Final review also verifies exactly
one Data refresh after selected and unselected spatial or annotation removals,
scene clearing, and batched spatial deletion, without extra renderer work.
Viewer passes 672 tests with two expected offscreen OpenGL skips; the framework
direct-source gate passes 16 tests with one expected exact-VCS skip. Ruff,
formatting, Pyright, strict MkDocs, and diff checks pass. Native direct use,
hosted CI, and candidate artifacts remain pending.

## Accepted Viewer Settings surface

Governing decision: ADR 049, accepted on 2026-11-14. Implementation, local
verification, direct-source integration, and independent re-review pass.

1. [Complete; locally verified] Keep exactly Scene, Data, and Annotations in
   the built-in content sidebar and preserve Data's read-only behavior plus
   Scene/Annotations contextual deletion.
2. [Complete; locally verified] Move Camera, Display, and Grid and Units into
   one initially hidden, reusable, modeless Viewer Settings window owned by
   each Viewer. Refresh the existing controls on open and keep window
   visibility, geometry, scrolling, and focused section transient.
3. [Complete; locally verified] Add **View → Viewer Settings…**, route Camera
   Settings through the same window, and expose
   `viewer.ui.settings.show(section)` with `viewer.settings_items` and
   `default_settings_items()` as the single composition path.
4. [Complete; locally verified] Accept typed keyword-only `sidebar_items` and
   `settings_items` iterables on the first process-local `Viewer(...)`
   construction, shallow-copy them before UI construction, use defaults when
   omitted, and document that later constructor calls or list mutation do not
   live-recompose the singleton UI.
5. [Complete; locally verified] Remove the System sidebar identifier,
   `focus_system_section`, and the old settings composition path without
   aliases. Preserve renderer, measurement, state, configuration, and refresh
   semantics.
6. [Complete locally; native confirmation pending] Verify reuse, refresh
   scope, close-to-hide and owner teardown, editor-local Escape,
   settings-window Escape isolation, keyboard and accessibility behavior,
   styling, sizing, scrolling, the end-to-end tutorial and executable
   examples, and the framework direct-source contract.

Exit gate: package tests, Ruff, formatting, Pyright, strict MkDocs,
direct-source framework integration, independent review, and the applicable
native lifecycle checks pass at recorded exact revisions. Hosted and
candidate-artifact evidence remain separate verification layers.

Local evidence: the full Viewer suite passes 689 tests with two expected
offscreen OpenGL skips. Independent focused Viewer/UI/documentation review
passes 130 tests; its one singleton-lifecycle wording finding was corrected.
A later low-severity missing public singleton regression was resolved with a
permanent focused test. Clean follow-up review passes that targeted test and
the 16-test settings module with Ruff, formatting, and diff checks and reports
no findings. The
documentation-example suite passes 17 tests, including effective settings
composition and the opt-in Attributes inspector. Ruff, formatting, Pyright
with zero errors, strict Viewer and framework MkDocs, `git diff --check`, and
the framework direct-source gate with 16 passes and one expected exact-revision
skip all pass. Native macOS modeless focus, high-DPI, and direct-use
confirmation remains pending. Hosted CI is stale until the working trees are
committed and pushed; candidate artifacts remain unrun and conditional on an
admission or release claim.

## Accepted Scene and Data inspection completion

Governing decisions: Accepted ADRs 050 and 051.

Status: accepted on 2026-11-14; implementation, local verification,
direct-source integration, and independent review pass. The decisions remain
independent.

### ADR 050 — read-only Data item inspection

1. [Complete locally] Retain the existing Data
   identity/reference header and add one ordered read-only tab surface
   containing Parameters, General Attributes, then the applicable Mesh or Graph
   component-domain tables.
2. [Complete locally] Limit General Attributes to the
   ordered public `Datastructure.attributes` mapping; preserve ADR 017's lazy
   declared-column, effective-value, and sparse-omission behavior for component
   tables.
3. [Complete locally] Preserve metadata-only unresolved
   items, shared-item deduplication, selection independence, failure isolation,
   and no mutation, resolution, ownership, serialization, or refresh side
   effect.
4. [Complete locally] Add focused Viewer tests,
   direct-source framework integration assertion, and Viewer tutorial/example
   coverage distinguishing general attributes, component attributes, and safe
   parameters.

### ADR 051 — Scene Object Details and settings boundary

1. [Complete locally] Expand one-object Object Details into
   ordered Identity, General Scene State, Type-Specific Scene State, and
   Represented Item Parameters sections.
2. [Complete locally] Derive type-specific rows only from
   declared `scene_state_fields()` in namespace/field order, including editable
   and noneditable values, and read each value through its declared attribute.
3. [Complete locally] Preserve unresolved-object inspection,
   per-value failure isolation, and the current multiple-selection
   count/type/name snapshot. Do not inspect arbitrary properties, extension
   payloads, or adapter caches.
4. [Complete locally] Keep Object Settings as the sole
   editing surface and prove that Details adds no setter, mutation, renderer
   rebuild, or UI refresh path. Add representative SceneObject tests,
   direct-source integration, and Viewer tutorial/example coverage.

No Core API, schema, serialization, compatibility alias, or migration change
is planned. Editable Data, a generic inspection registry, additional
datastructure types, and a second Scene editing surface require separate future
approval.

Local exit gate: the complete Viewer suite passes 705 tests with two expected
offscreen native OpenGL skips. Ruff, formatting, Pyright with zero errors,
strict Viewer and framework MkDocs, `git diff --check`, and the framework
direct-source gate with 16 passes and one expected exact-revision skip pass.
Independent review finds the ADR 050–051 runtime clean. Native, refreshed
hosted, and artifact evidence remains separately pending.

## Accepted executable Viewer documentation and examples

Governing decision: Accepted ADR 052.

Status: accepted on 2026-11-14; implementation and local verification pass in
the uncommitted Viewer working tree.

1. [Complete locally] Maintain one end-to-end tutorial backed
   by one authoritative runnable script under `docs/examples/`.
2. [Complete locally] Audit focused category-level coverage
   for Scene/content and inspection boundaries, Viewer Settings/configuration,
   selection/transforms/refresh, measurements/annotations, serialization,
   overlays, dynamic workflows, and optional geometry backends.
3. [Complete locally] Keep public and touched APIs on
   MkDocs-compatible NumPy docstrings and Python 3.12 annotations; run Ruff and
   Pyright over all authoritative Python examples.
4. [Complete locally] Maintain representative headless
   smoke/contract checks, focused doctests where applicable, strict MkDocs and
   link/snippet validation, and `git diff --check`.
5. [Complete locally] Label optional/native requirements and
   report native visual, interaction, focus, scrolling, and high-DPI checks
   separately from headless evidence.
6. [Complete locally] Reconcile every claim with implemented,
   verified behavior. Return runtime gaps to their owning ADR rather than
   changing code under the documentation decision.

Local exit gate: the documentation-example suite passes 20 tests; all
authoritative examples pass Ruff, formatting, and Python 3.12 Pyright; strict
MkDocs and `git diff --check` pass. Independent review findings on annotation
serialization coverage and scope wording were corrected and revalidated.
Native and optional-backend evidence remains explicitly separate. Acceptance
of ADR 052 did not itself implement ADR 050 or 051.

## Deferred work requiring new approval

- sub-object or domain-component selection;
- ancestor/descendant group-transform semantics and advanced gizmos;
- angular, radial, area, or snapping measurement systems;
- a general overlay/plugin registry;
- console, terminal, Python/shell execution, assistant services, credentials,
  or remote transports;
- `compas_session` reactive-state integration; and
- `compas_session` aggregation of data, one or more scenes, settings, and
  history, including optional Viewer new/open/save conveniences;
- notebook, Rhino, Grasshopper, Blender, or other backend migrations.
