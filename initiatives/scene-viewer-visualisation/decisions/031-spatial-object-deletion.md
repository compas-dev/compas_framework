# ADR 031: Spatial Object Deletion

## Status

Proposed.

## Context

Core `Scene.remove` already removes one scene object or one complete group
subtree without deleting the independently owned geometry or data item. Viewer
already wraps that operation with render-resource, picking, selection, buffer,
and UI cleanup, and registers `viewer.delete_selected` with the Delete key.

Deletion is not discoverable in the default menus, however, and the viewport
key binding may not be available while the scene tree owns keyboard focus.
Deletion also has to remain consistent with transform-only history, associative
dimensions, and the proposed separation of spatial objects and annotations.

## Options

1. Expose the existing **Delete Selected** command in the default Edit menu and
   preserve the current removal semantics.
2. Add deletion to the transform undo/redo stack.
3. Cascade deletion to dimensions that reference removed objects.
4. Add a separate Scene-tree-specific deletion implementation.

## Recommendation

Choose option 1.

The default Edit menu exposes one **Delete Selected** action backed by the
existing `viewer.delete_selected` command and Delete shortcut. The operation
removes every selected spatial object and every descendant of a selected group
as one Viewer mutation.

Deletion does not delete independently owned geometry or data. It removes
scene placement, render resources, picking registrations, and every removed
object from selection. It rebuilds the affected Viewer buffers and refreshes
the scene tree and viewport.

Deletion is not undoable in this phase. It clears the existing transform-only
undo and redo history instead of implying a broader history contract.
Associative dimensions that reference a removed object remain durable and
become explicitly unresolved; deletion never converts them to fixed dimensions
or removes them as a cascade.

If ADR 029 is accepted, its flat Annotations UI owns annotation removal.
Spatial deletion remains a Scene-tree operation and does not remove annotation
entries merely because their referenced objects were deleted.

## Consequences

- Deletion is visible and usable regardless of whether the viewport or scene
  tree currently has focus.
- Core and Viewer retain one removal path rather than duplicating Scene-tree
  logic.
- Subtree, independent-data, selection, rendering, and unresolved-association
  behavior remain explicit.
- Deletion remains outside undo/redo until a broader history decision is
  proposed and approved.

## Compatibility

This exposes existing behavior through the default Edit menu. It does not
change Core scene serialization, object ownership, removal semantics, or the
transform-only history contract.

## Verification

- Verify **Delete Selected** appears once in the default Edit menu with the
  existing command and shortcut.
- Verify it works when the viewport and scene tree respectively own focus.
- Verify one object and one selected group subtree remove all associated render
  objects, picking colors, and selection entries.
- Verify independently owned data remains available after scene removal.
- Verify deletion clears transform undo and redo history.
- Verify an associative dimension remains present and resolves as unresolved
  after deletion of its referenced object.
- Verify a fixed dimension is unchanged by deletion of unrelated objects.
- If ADR 029 is accepted, verify spatial deletion and annotation removal remain
  separate operations.

## Dependencies

- Preserves Accepted ADRs 003, 004, 010, 013, and 028.
- Annotation removal depends on Proposed ADR 029 and is not authorized here.

## Decision

Pending explicit approval.
