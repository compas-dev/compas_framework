# Scene, Viewer, and Visualisation Decisions

ADRs 001–007 are Accepted. New round-trip evidence requires two Proposed
amendments before implementation starts. ADRs 008–009 refine, but do not
silently rewrite, the accepted ownership boundary.

| ADR | Decision | Status | Dependencies |
|---|---|---|---|
| 001 | [Ownership and state boundaries](001-ownership-boundaries.md) | Accepted | Geometry 022/024; Plugin 002 |
| 002 | [Indexed Viewer buffer geometry](002-indexed-buffer-geometry.md) | Accepted | 001; Typing structural inputs |
| 003 | [Viewer state and object selection](003-viewer-state-and-selection.md) | Accepted | 001 |
| 004 | [Transformations, refresh, and undo](004-transform-refresh-undo.md) | Accepted | 001, 003 |
| 005 | [Annotations, measurements, and overlays](005-annotations-and-overlays.md) | Accepted | 001, 002, 003 |
| 006 | [Public Viewer integration facade](006-viewer-integration-facade.md) | Accepted | 001, 003, 004, 005 |
| 007 | [Initial scope and verification](007-scope-and-verification.md) | Accepted | 001–006; Plugin 005 |
| 008 | [Serializable scene nodes and runtime adapters](008-scene-nodes-and-runtime-adapters.md) | Proposed | 001; verified round-trip regressions |
| 009 | [Explicit scene-state serialization fields](009-scene-state-fields.md) | Proposed | 008 |

Phase 1 is blocked until ADRs 008–009 are explicitly approved. ADR 008 refines
ADR 001's statement that core owns durable scene content: the durable object is
a scene-owned node/state record, not the context-specific runtime
`SceneObject` adapter. ADR 009 replaces the implicit `settings`/constructor
replay mechanism with an explicit schema. The remaining accepted decisions
retain their intent but must be implemented against the amended boundary.
