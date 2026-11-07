# ADR 004: Transformations, Refresh, and Undo

## Status

Accepted.

## Context

Core already owns local/world transformations and Viewer can update transform
buffers efficiently, but there is no public multi-object transformation
operation, gizmo contract, or undo behavior. Geometry, selection, sidebar, and
renderer refreshes are invoked through concrete internals. A universal core
event bus would make every mutable property observable before its semantics are
known.

## Options

1. Add explicit Viewer transform transactions, undo/redo, and categorized
   refresh operations while retaining core transformations.
2. Add a generic observable mutation/event system to core Scene.
3. Mutate scene objects directly and require callers to refresh internals.
4. Move transformations and history entirely into Viewer state.

## Recommendation

Choose option 1.

Expose `viewer.transform_objects(objects, transformation, space="world")`.
Apply one world-space delta to each pre-operation world transformation and
derive each new local transformation through its parent. Reject requests that
contain both an ancestor and its descendant in the initial version. Validate
the entire request before mutation and leave all objects unchanged on failure.

Record before/after local transformations as one reversible Viewer
transaction. Add a small undo/redo stack for explicit reversible Viewer
transactions; do not absorb general session or domain history.

Expose explicit geometry, appearance, transform, and hierarchy refresh
operations. Do not add a core scene event bus in this wave. Direct external
mutation requires the matching Viewer refresh call.

## Consequences

- Code, commands, and a future gizmo use identical transformation semantics.
- Atomic transactions provide predictable undo and efficient transform-buffer
  updates.
- Ancestor/descendant simultaneous transforms remain unsupported until their
  intended group semantics are decided.
- Arbitrary item mutation is not magically detected; synchronization remains
  explicit and testable.

## Compatibility

Existing direct transformation mutation remains a core operation, but Viewer
consumers migrate to the public transaction when they require refresh or undo.
Existing callback commands remain valid and simply do not enter history unless
they produce a reversible transaction.

## Verification

- Test world/local conversion under transformed parents.
- Test multiple independent objects, atomic validation failure, ancestor/
  descendant rejection, undo, redo, and redo invalidation after new work.
- Assert transform-only refresh does not rebuild geometry buffers.
- Verify failed commands do not create history entries.

## Affected packages

Initial implementation: `compas`, `compas_viewer`, and `compas_framework`.

Later redesign consumer: `compas_model`.

## Dependencies

- [ADR 001](001-ownership-boundaries.md)
- [ADR 003](003-viewer-state-and-selection.md)
