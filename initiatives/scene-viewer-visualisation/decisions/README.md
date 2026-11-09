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
| 022 | [Distance-dimension unit semantics](022-distance-dimension-units.md) | Accepted | 021; 027; 005; 020 |
| 023 | [Clean break for legacy Viewer annotations](023-annotation-clean-break.md) | Accepted | 021; 005 |
| 024 | [Measurement outcomes and persistence](024-measurement-outcomes-and-persistence.md) | Accepted | 005; 021–022; 026 |
| 025 | [Scale and legend overlay contracts](025-scale-and-legend-overlays.md) | Accepted; implementation note added 2026-11-09 | 005–006; 023 |
| 026 | [Measurement interaction and acquisition](026-measurement-interaction-and-acquisition.md) | Accepted; amended 2026-11-09 | 005; 024; 021–022; 003–004; 006; 027–028 |
| 027 | [Viewer measurement settings and UI](027-viewer-measurement-settings.md) | Accepted | 005; 020; 022; 026 |
| 028 | [Fixed and associative dimension anchors](028-dimension-anchor-modes.md) | Accepted | 005; 024; 021; 026 |
| 029 | [Persistent annotation collection and UI](029-persistent-annotation-collection-and-ui.md) | Accepted | 005; 010; 013; 021; 030 |
| 030 | [Always-visible persistent dimension rendering](030-always-visible-dimension-rendering.md) | Accepted | 005; 021; 024; 026; independent of 029 |
| 031 | [Spatial object deletion](031-spatial-object-deletion.md) | Accepted | 003–004; 010; 013; 028; annotation removal governed by 029 |
| 032 | [Three-domain Viewer sidebar](032-three-domain-viewer-sidebar.md) | Accepted; implemented and locally verified | Refines 003, 027, 029, and 031 |

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
direct-source gate, and independent review pass; hosted refreshes are pending.
