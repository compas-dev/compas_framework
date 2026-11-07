# Scene, Viewer, and Visualisation Decisions

All decisions are Proposed. None authorizes package source changes until the
user explicitly accepts it.

| ADR | Decision | Status | Dependencies |
|---|---|---|---|
| 001 | [Ownership and state boundaries](001-ownership-boundaries.md) | Proposed | Geometry 022/024; Plugin 002 |
| 002 | [Indexed Viewer buffer geometry](002-indexed-buffer-geometry.md) | Proposed | 001; Typing structural inputs |
| 003 | [Viewer state and object selection](003-viewer-state-and-selection.md) | Proposed | 001 |
| 004 | [Transformations, refresh, and undo](004-transform-refresh-undo.md) | Proposed | 001, 003 |
| 005 | [Annotations, measurements, and overlays](005-annotations-and-overlays.md) | Proposed | 001, 002, 003 |
| 006 | [Public Viewer integration facade](006-viewer-integration-facade.md) | Proposed | 001, 003, 004, 005 |
| 007 | [Initial scope and verification](007-scope-and-verification.md) | Proposed | 001–006; Plugin 005 |
