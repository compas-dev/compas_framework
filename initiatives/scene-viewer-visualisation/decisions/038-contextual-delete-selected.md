# ADR 038: Contextual Delete Selected

## Status

Proposed.

## Context

The default **Edit > Delete Selected** command and Delete shortcut currently
remove only spatial scene objects. Annotation removal exists in the
Annotations panel, but selecting a dimension does not make the user-facing
command remove it. Spatial and annotation selections may intentionally coexist,
so deleting their union would cross ownership boundaries and could remove more
than the current context indicates.

## Options

1. Dispatch the user-facing command to the selection owned by the current
   interaction context.
2. Delete both spatial and annotation selections together.
3. Keep the menu command spatial-only and require the annotation Remove
   control.
4. Replace the two selections with one union selection.

## Recommendation

Choose option 1.

**Delete Selected** removes the selection owned by the current interaction
context and never crosses collection boundaries or deletes both coexisting
selections. The two existing removal operations remain separate.

Dispatch follows this precedence:

1. A focused text or numeric editor retains its normal local Delete behavior.
2. Focus in the annotation list or annotation details removes annotation
   selection.
3. Focus in the Scene tree or viewport removes spatial selection, even if a
   different sidebar tab remains visible.
4. Menu activation obscures the previous focused widget, so **Edit > Delete
   Selected** follows the active sidebar tab: Scene removes spatial selection,
   Annotations removes annotation selection, and System disables the menu
   action. The underlying command safely performs no operation if invoked
   directly while System is active.

When both selections contain values, exactly one domain is affected and the
other selection remains unchanged. The explicit Annotations-panel Remove
control remains annotation-only.

## Consequences

- Selected dimensions can be removed through the same discoverable command as
  selected spatial objects without conflating the two collections.
- Delete behavior follows visible interaction context and preserves
  editor-local key behavior.
- Existing spatial subtree removal and annotation removal primitives remain
  independently testable.
- Viewer needs a narrow way to query the active sidebar domain and route menu
  and shortcut invocation.
- No union-selection abstraction or Core schema change is introduced.

## Verification

- Verify local Delete remains available in focused text and numeric editors.
- Verify annotation-list and annotation-detail focus delete annotations only.
- Verify Scene-tree and viewport focus delete spatial objects only.
- Verify menu invocation follows Scene, Annotations, and System tab ownership.
- Verify System disables the menu action and direct command invocation is a
  no-op.
- Verify simultaneous selections remove exactly one domain and preserve the
  other selection.
- Verify the explicit annotation Remove control remains annotation-only.
- Re-run spatial subtree, annotation resource cleanup, unresolved associative
  anchor, and transformation-history invalidation regressions.

## Dependencies

- Amends Accepted ADR 032's input-ownership and Delete behavior.
- ADR 031 continues to govern the spatial removal primitive.
- ADR 029 continues to govern annotation removal and selection.

## Decision

Pending explicit approval.
