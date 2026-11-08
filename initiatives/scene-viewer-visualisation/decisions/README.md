# Scene, Viewer, and Visualisation Decisions

ADRs 013–016 are Accepted. ADRs 013–014 supersede the implemented
node/runtime-adapter model of ADR 008, part of ADR 009, and the unaccepted
alternatives in ADRs 011–012. ADR 010 remains Accepted with item references
moved to stable scene objects. ADRs 015–016 authorize a Viewer-owned mechanism
for contextual object-settings fields; implementation remains pending.

| ADR | Decision | Status | Dependencies |
|---|---|---|---|
| 001 | [Ownership and state boundaries](001-ownership-boundaries.md) | Accepted | Geometry 022/024; Plugin 002 |
| 002 | [Indexed Viewer buffer geometry](002-indexed-buffer-geometry.md) | Accepted | 001; Typing structural inputs |
| 003 | [Viewer state and object selection](003-viewer-state-and-selection.md) | Accepted | 001 |
| 004 | [Transformations, refresh, and undo](004-transform-refresh-undo.md) | Accepted | 001, 003 |
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
| 015 | [Contextual scene form contributions](015-contextual-scene-form-contributions.md) | Accepted | 013; respects 014 |
| 016 | [Scene form field bindings](016-scene-form-field-bindings.md) | Accepted | 015; 010 and 013 semantics |

ADRs 008–010 were accepted on 2026-11-07. ADR 010 refines ADR 008's item store
into non-owning runtime bindings and keeps aggregation outside Scene. A
redesigned Session is the likely aggregate under separate future approval.
ADRs 015–016 were accepted on 2026-11-08 and authorize contextual form
implementation without extending core's scene-operation registry or durable
scene state.
