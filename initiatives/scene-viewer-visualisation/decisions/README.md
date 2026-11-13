# Scene, Viewer, and Visualisation Decisions

ADRs 013–020 are Accepted. ADRs 013–014 supersede the implemented
node/runtime-adapter model of ADR 008, part of ADR 009, and the unaccepted
alternatives in ADRs 011–012. ADR 010 remains Accepted with item references
moved to stable scene objects. ADRs 015–016 authorize contextual object
settings from one normalized mapping: editable `SceneStateField` entries plus
narrowly declared non-state attributes. The earlier `FormField` implementation
has been replaced and verified. ADRs 017–020 authorize lazy datastructure
attribute tables, their editing semantics, configured Viewer identity, and a
configuration lifecycle/field audit. Their implementation is verified locally
and in hosted Viewer and framework CI. ADR 017 is amended to keep the
datastructure inspector out of the default sidebar while preserving opt-in
custom use. ADR 003 is implemented, locally
verified, independently approved, and green in hosted Viewer and refreshed
framework CI. ADR 004 is implemented, locally verified, and independently
approved; refreshed hosted Viewer, core, and framework verification passed.
ADRs 021–031 record the accepted Phase 3 durable annotation ownership, unit
snapshots, clean-break migration, transient/persistent outcomes, overlay
contracts, snapping and acquisition, Viewer measurement presentation,
fixed/associative anchor model, separate annotation collection and UI,
always-visible dimension rendering, and spatial-object deletion behavior.
ADR 032 is Accepted in response to direct-use evidence that the current
stacked sidebar does not provide stable or clearly separated Scene,
Annotations, and System contexts.
ADR 033 is Accepted and authorizes the Details dialog plus independent
Scene-local and Annotations-local splitters. Its approved scroll correction is
implemented and locally verified. ADR 035 is Accepted with its
deterministic world-space layout and initial Spatial Layout details form;
implementation, local verification, and independent review pass.
Accepted ADR 034 adds Mesh-vertex snapping independent of normal glyph visibility; its
implementation, local verification, native OpenGL regression, and independent
review pass.
ADR 036 accepts programmatic,
non-persistent screen-pinned text overlays. Accepted ADRs 037–039 authorize
narrow annotation label backgrounds, contextual deletion, and moving the
existing geometry Add menu under Scene; their implementations, local
verification, and independent review pass.
ADRs 040–042 accept synchronized default-toolbar controls, a Grid and Units
System section with consistent field alignment and no tolerance UI, and
transient selected-object area and volume inspection. Their implementations
are verified locally and in hosted Viewer and framework CI at the recorded
candidate revisions. ADR 040's 2026-11-10 amendment replaces only the View
selector with five state-bound, icon-only buttons and uses event-driven pending
focus restoration. Its local, actual-widget, and native verification passes;
the scripted native probes passed, but the subsequent user retest confirmed
the standard-view buttons and rejected Render Mode dropdown focus. Refreshed
hosted verification remains pending.
ADR 043 accepts one built-in COMPAS Viewer theme with system-following light
and dark variants. It preserves the current appearance values and configuration
schema and limits theme ownership to Qt chrome. Its exact accessible token
table is approved as Viewer-specific styling rather than an organization-wide
brand standard.
ADR 044 accepts validated editing of one selected persistent distance
dimension's unit and 0–15 precision while preserving Grid and Units as defaults
for transient and newly created measurements. Its implementation, local
verification, and independent review pass.
The latest native retest confirms the five standard-view buttons, Camera
population, and general presentation, but rejects Render Mode popup focus.
Approved amendments to ADRs 037 and 040 add label-background editing and replace
the popup/letter-icon composition with semantic render buttons, private fixed
viewport view selection, and existing zoom/capture actions. Accepted ADR 045
changes Viewer's fixed default background to `#D8DDE2` while preserving Core's
white defaults and ADR 043's theme separation. Implementation, local
verification, independent re-review, and user direct use pass; hosted
verification remains pending.

New direct-use feedback produced another coordinated presentation revision,
approved on 2026-11-11. ADR 040 replaces the current viewport list and toolbar render buttons
with one grouped viewport menu and add one measurement menu button. ADR 037
enables scheme-colored backgrounds for newly acquired Viewer dimensions.
Accepted ADR 046 defines scheme-aware Viewer defaults while preserving Core and
explicit/serialized colors; it narrowly amends ADR 043 and would supersede ADR
045's fixed background. It advances Viewer configuration to schema 4 with an
explicit `None` automatic-background marker and defines base/specialized color
precedence for existing supported channels. Implementation and local
verification and native direct use pass; hosted verification remains pending.

Accepted ADR 047 exposes the existing durable parametric-shape `u` and `v`
resolution only for producers that consume those axes. It adds no field,
alias, or schema version; implementation and local verification pass. Its
accepted settings-only refresh amendment routes visibility, opacity, point
size, and line width through one object settings-texture update and redraw,
while `u` and `v` retain topology rebuilds. Shape and Surface forms use
wireframe wording; Mesh and Graph retain edge wording. Durable names do not
change. Amendment implementation, local verification, and independent review
pass. Native direct use confirms responsive wireframe toggling at Torus U
resolution 64, accepts the wording, and confirms the crash remains fixed.
Accepted ADR 048 adds a read-only Viewer **Data** domain as a flat projection
of Scene-referenced item GUIDs. It does not own, serialize, load, or edit data;
implementation, local verification, and independent review pass. The final
sidebar order is Scene, Data, Annotations, System. Unattached and multi-scene
data remain in the separately deferred Session scope, which may later replace
or extend the inventory source without making Viewer an owner.
Proposed ADR 049 responds to the information-architecture distinction between
the Scene, Data, and Annotations content domains and System settings. It would
leave exactly those three content tabs in the sidebar and move Camera, Display,
and Grid and Units into one Viewer-owned modeless settings window. It is not
implemented and requires explicit approval.

| ADR | Decision | Status | Dependencies |
|---|---|---|---|
| 001 | [Ownership and state boundaries](001-ownership-boundaries.md) | Accepted | Geometry 022/024; Plugin 002 |
| 002 | [Indexed Viewer buffer geometry](002-indexed-buffer-geometry.md) | Accepted | 001; Typing structural inputs |
| 003 | [Viewer state and object selection](003-viewer-state-and-selection.md) | Accepted; implemented, local verification passed | 001 |
| 004 | [Transformations, refresh, and undo](004-transform-refresh-undo.md) | Accepted; implemented and verified | 001, 003 |
| 005 | [Annotations, measurements, and overlays](005-annotations-and-overlays.md) | Accepted, amended by 024/028 | 001, 002, 003 |
| 006 | [Public Viewer integration facade](006-viewer-integration-facade.md) | Accepted | 001, 003, 004, 005 |
| 007 | [Initial scope and verification](007-scope-and-verification.md) | Accepted | 001–006; Plugin 005 |
| 008 | [Serializable scene nodes and runtime adapters](008-scene-nodes-and-runtime-adapters.md) | Superseded by 013–014 | 001; verified round-trip regressions |
| 009 | [Explicit scene-state serialization fields](009-scene-state-fields.md) | Superseded in part by 013 | 008 |
| 010 | [Scene description, item bindings, and aggregation boundary](010-scene-description-and-item-bundling.md) | Accepted | 008, 009 |
| 011 | [Node-first scene construction and adapter lifetime](011-node-first-scene-adapters.md) | Superseded before acceptance | 008; 010 |
| 012 | [Explicit node-backed adapter state](012-explicit-node-backed-adapter-state.md) | Superseded before acceptance | 011 |
| 013 | [Hierarchy-only nodes and stable scene objects](013-hierarchy-nodes-and-stable-sceneobjects.md) | Accepted | Supersedes 008/009 placement; preserves 010 |
| 014 | [Context-keyed scene operation plugins](014-context-keyed-scene-operations.md) | Accepted | 013; replaces backend class registration |
| 015 | [Editable scene-object attributes](015-contextual-scene-form-contributions.md) | Accepted, amended | 013; respects 014 |
| 016 | [Contextual editable-attribute overrides and mutation](016-scene-form-field-bindings.md) | Accepted, amended | 015; respects 014 |
| 017 | [Lazy datastructure element-attribute tables](017-lazy-datastructure-attribute-tables.md) | Accepted; amended 2026-11-09 | 006; sidebar coordination |
| 018 | [Datastructure element-attribute editing](018-datastructure-attribute-editing.md) | Accepted | 017; 006/016 refresh ownership |
| 019 | [Configured Viewer identity](019-configured-viewer-identity.md) | Accepted | Independent |
| 020 | [Viewer configuration lifecycle and field audit](020-viewer-config-lifecycle-and-audit.md) | Accepted | 019; sidebar coordination with 017–018 |
| 021 | [Durable annotation ownership and schema](021-durable-annotation-ownership.md) | Accepted | 005; 010; 013–014; 028 |
| 022 | [Distance-dimension unit semantics](022-distance-dimension-units.md) | Accepted; amended by 044 on 2026-11-10 | 021; 027; 005; 020 |
| 023 | [Clean break for legacy Viewer annotations](023-annotation-clean-break.md) | Accepted | 021; 005 |
| 024 | [Measurement outcomes and persistence](024-measurement-outcomes-and-persistence.md) | Accepted | 005; 021–022; 026 |
| 025 | [Scale and legend overlay contracts](025-scale-and-legend-overlays.md) | Accepted; implementation note added 2026-11-09 | 005–006; 023 |
| 026 | [Measurement interaction and acquisition](026-measurement-interaction-and-acquisition.md) | Accepted; amended 2026-11-09 | 005; 024; 021–022; 003–004; 006; 027–028 |
| 027 | [Viewer measurement settings and UI](027-viewer-measurement-settings.md) | Accepted | 005; 020; 022; 026 |
| 028 | [Fixed and associative dimension anchors](028-dimension-anchor-modes.md) | Accepted | 005; 024; 021; 026 |
| 029 | [Persistent annotation collection and UI](029-persistent-annotation-collection-and-ui.md) | Accepted; extension-line-width amendment implemented and locally verified | 005; 010; 013; 021; 030; coordinates with 035 |
| 030 | [Always-visible persistent dimension rendering](030-always-visible-dimension-rendering.md) | Accepted | 005; 021; 024; 026; independent of 029 |
| 031 | [Spatial object deletion](031-spatial-object-deletion.md) | Accepted | 003–004; 010; 013; 028; annotation removal governed by 029 |
| 032 | [Three-domain Viewer sidebar](032-three-domain-viewer-sidebar.md) | Accepted; implemented and verified | Refines 003, 027, 029, and 031 |
| 033 | [Resizable Scene inspector and Details dialog](033-scene-inspector-details.md) | Accepted; scroll correction implemented and locally verified | Narrowly amends 032 |
| 034 | [Mesh-vertex snapping independent of vertex glyphs](034-hidden-vertex-snapping.md) | Accepted; implemented and independently reviewed | Amends 026; preserves 028 |
| 035 | [Distance-dimension spatial layout](035-distance-dimension-spatial-layout.md) | Accepted; extension-line-width amendment implemented and locally verified | Extends 021, 028–030; preserves 022 |
| 036 | [Viewport text ownership and persistence](036-viewport-text-ownership-and-persistence.md) | Accepted; programmatic, non-persistent initial scope | Extends 005 and 025; optional use of 037 |
| 037 | [Optional annotation label backgrounds](037-annotation-label-backgrounds.md) | Accepted; default-background amendment implemented and locally verified | Extends 021 and 029 |
| 038 | [Contextual Delete Selected](038-contextual-delete-selected.md) | Accepted; implemented and independently reviewed | Amends 032; preserves 029 and 031 primitives |
| 039 | [Scene-owned Add menu](039-scene-add-menu.md) | Accepted; implemented and independently reviewed | Consistent with 001, 013, 024, and 026 |
| 040 | [Default toolbar view shortcuts](040-default-toolbar-view-shortcuts.md) | Accepted; grouped viewport/measurement-menu amendment implemented and locally verified | Extends 006; amends 020 default visibility |
| 041 | [Grid and Units System section](041-grid-and-units-system-section.md) | Accepted; implemented and verified | Amends 027 and 032; preserves 020 |
| 042 | [Selected area and volume inspection](042-selected-area-and-volume-inspection.md) | Accepted; implemented and verified | Uses 003–004; extends 006 and 024; coordinates with 027/041 |
| 043 | [Built-in COMPAS Viewer theme](043-built-in-compas-viewer-theme.md) | Accepted; content-palette amendment implemented and locally verified | Preserves 019–020; covers 032, 040–041; amended by 046 |
| 044 | [Editing persistent distance-dimension format](044-editing-persistent-dimension-format.md) | Accepted; amended 2026-11-10, implemented and independently reviewed | Amends 022, 029, 032; clarifies 027, 041 |
| 045 | [Default viewport and content contrast](045-default-viewport-content-contrast.md) | Accepted baseline; superseded by implemented ADR 046 | Preserves 043; superseded by 046 |
| 046 | [Viewer scheme-aware content palette](046-viewer-content-palette.md) | Accepted; implemented and locally verified | Amends 043; supersedes 045; coordinates with 037 |
| 047 | [Editable parametric shape resolution](047-editable-parametric-shape-resolution.md) | Accepted; implemented, locally verified, independently reviewed, and native user-confirmed | Uses 002, 004, 015–016 |
| 048 | [Referenced Data domain](048-referenced-data-domain.md) | Accepted; implemented, locally verified, and independently reviewed | Preserves 001, 010, 013; reuses 017; extends 032 |
| 049 | [Viewer Settings surface](049-viewer-settings-surface.md) | Proposed; approval required | Amends 032 and 041; preserves 038, 040, 043, 046, and 048 |

ADRs 008–010 were accepted on 2026-11-07. ADR 010 refines ADR 008's item store
into non-owning runtime bindings and keeps aggregation outside Scene. A
redesigned Session is the likely aggregate under separate future approval.
ADRs 015–016 were accepted and amended on 2026-11-08. Durable semantic fields
declare editability on their existing `SceneStateField`; only non-state
attributes use `__editable_attributes__`. Context overrides remain runtime-only,
and public `FormField`, item-target, and core refresh-hook semantics are removed.
ADRs 017–020 were accepted on 2026-11-08 and implemented in the required order
ADR 019, ADR 020, ADR 017, then ADR 018 so configuration and sidebar ownership
were established before the attribute tables were added. Local verification,
independent review, and hosted Viewer and framework checks passed. ADR 003 now
has one Viewer-owned ordered object selection, with all interaction paths
migrated and scene-local mutation APIs removed. Local verification,
independent review, the hosted Viewer matrix, and refreshed framework checks
passed. ADR 004 now provides atomic world-space multi-object transforms, four
explicit refresh categories, and a private Viewer-level reversible transform
transaction stack. Local verification and independent review passed; refreshed
hosted Viewer, core, and framework checks passed.
ADRs 021–028 were accepted on 2026-11-08. Durable annotations live
in `compas.scene` and load without Viewer. Persistent dimensions snapshot the
declared Viewer unit and precision without implicit conversion. `Tag`,
`ArrowOverlay`, their aliases, and their serialized dtype paths are removed
rather than preserved through a compatibility layer. Viewer distinguishes live
transient inspection from persistent dimension annotation; persistent
completion creates one `DistanceDimension` with independently fixed or
associative anchors. Both UI modes use snapping, associative acquisition never
silently falls back, and removed components make anchors explicitly unresolved.
ADR 027 adds one Units and Measurement tab with editable Viewer unit and display
precision plus read-only global COMPAS tolerance. It neither restores the old
root unit nor mutates global tolerance; snapping governs correctness.
ADR 025 adds one ordered Viewer overlay layer, a camera-target scale bar, and
an ordered categorical legend without serialization or picking. Its
2026-11-09 implementation note records the transparent widget canvas used to
keep transient painting outside the OpenGL renderer. ADR 026 adds one
nearest-eligible-discrete-point query and one-shot transient and persistent
tool lifecycles. Its 2026-11-09 amendment exposes the hovered object's discrete
point palette, a distinct click winner, and the retained first anchor.
Direct-use refinement adds bright square markers, an 18-logical-pixel radius,
and same-object footprint depth qualification. Only visible Point,
Mesh-vertex, and Graph-node guides are eligible; every invisible line, edge,
face, and surface target is disabled. ADR 030 keeps persistent dimensions
visible in a separate final render pass. ADRs 029 and 031 were accepted on
2026-11-09. ADR 029 moves durable annotations out of the spatial hierarchy,
adds a flat Annotations UI, and separates semantic annotation data from a
narrow durable dimension style. ADR 031 exposes existing spatial deletion
through the default Edit menu while preserving subtree, independent-data,
history-invalidation, and unresolved-association behavior. Their implementation
and refreshed hosted verification passed. Direct-use evidence subsequently
showed that the shared splitter and mixed detail surfaces make the sidebar
unstable and ambiguous. Accepted ADR 032 records the approved three-domain
replacement. Its implementation, documentation, local verification, framework
direct-source gate, independent review, hosted package CI, and exact
source-installed framework gate pass.
