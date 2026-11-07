# Scene, Viewer, and Visualisation Decisions

ADRs 001–010 are Accepted. ADRs 011–012 are Proposed architecture corrections
after the Phase 0 implementation exposed a dual adapter lifecycle and hidden
state routing that conflict with the initiative's simplicity rule.

| ADR | Decision | Status | Dependencies |
|---|---|---|---|
| 001 | [Ownership and state boundaries](001-ownership-boundaries.md) | Accepted | Geometry 022/024; Plugin 002 |
| 002 | [Indexed Viewer buffer geometry](002-indexed-buffer-geometry.md) | Accepted | 001; Typing structural inputs |
| 003 | [Viewer state and object selection](003-viewer-state-and-selection.md) | Accepted | 001 |
| 004 | [Transformations, refresh, and undo](004-transform-refresh-undo.md) | Accepted | 001, 003 |
| 005 | [Annotations, measurements, and overlays](005-annotations-and-overlays.md) | Accepted | 001, 002, 003 |
| 006 | [Public Viewer integration facade](006-viewer-integration-facade.md) | Accepted | 001, 003, 004, 005 |
| 007 | [Initial scope and verification](007-scope-and-verification.md) | Accepted | 001–006; Plugin 005 |
| 008 | [Serializable scene nodes and runtime adapters](008-scene-nodes-and-runtime-adapters.md) | Accepted | 001; verified round-trip regressions |
| 009 | [Explicit scene-state serialization fields](009-scene-state-fields.md) | Accepted | 008 |
| 010 | [Scene description, item bindings, and aggregation boundary](010-scene-description-and-item-bundling.md) | Accepted | 008, 009 |
| 011 | [Node-first scene construction and adapter lifetime](011-node-first-scene-adapters.md) | Proposed | Supersedes parts of 008; preserves 010 |
| 012 | [Explicit node-backed adapter state](012-explicit-node-backed-adapter-state.md) | Proposed | 011; supersedes implementation mechanism of 009 |

ADRs 008–010 were accepted on 2026-11-07. ADR 010 refines ADR 008's item store
into non-owning runtime bindings and keeps aggregation outside Scene. A
redesigned Session is the likely aggregate under separate future approval.
