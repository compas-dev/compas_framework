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
and in hosted Viewer and framework CI. ADR 003 is implemented, locally
verified, independently approved, and green in hosted Viewer and refreshed
framework CI. ADR 004 is implemented, locally verified, and independently
approved; refreshed hosted Viewer, core, and framework verification passed.

| ADR | Decision | Status | Dependencies |
|---|---|---|---|
| 001 | [Ownership and state boundaries](001-ownership-boundaries.md) | Accepted | Geometry 022/024; Plugin 002 |
| 002 | [Indexed Viewer buffer geometry](002-indexed-buffer-geometry.md) | Accepted | 001; Typing structural inputs |
| 003 | [Viewer state and object selection](003-viewer-state-and-selection.md) | Accepted; implemented, local verification passed | 001 |
| 004 | [Transformations, refresh, and undo](004-transform-refresh-undo.md) | Accepted; implemented and verified | 001, 003 |
| 005 | [Annotations, measurements, and overlays](005-annotations-and-overlays.md) | Accepted | 001, 002, 003 |
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
| 017 | [Lazy datastructure element-attribute tables](017-lazy-datastructure-attribute-tables.md) | Accepted | 006; sidebar coordination |
| 018 | [Datastructure element-attribute editing](018-datastructure-attribute-editing.md) | Accepted | 017; 006/016 refresh ownership |
| 019 | [Configured Viewer identity](019-configured-viewer-identity.md) | Accepted | Independent |
| 020 | [Viewer configuration lifecycle and field audit](020-viewer-config-lifecycle-and-audit.md) | Accepted | 019; sidebar coordination with 017–018 |

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
