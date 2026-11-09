# ADR 033: Resizable Scene Inspector and Details Dialog

## Status

Proposed.

## Context

The Scene tab currently gives the hierarchy and selected-object controls a
fixed layout allocation. `ObjectSetting` also places a read-only description
textbox above the editable controls. The description consumes scarce sidebar
space, while users cannot resize the hierarchy and selected-object areas.

ADR 032 prohibited the previous root splitter because it mixed unrelated
Scene, Annotation, and System domains and redistributed them during updates.
That does not require the complete absence of a stable splitter inside one
domain.

## Options

1. Use one Scene-local two-pane splitter and move descriptive information to a
   Details dialog.
2. Keep the fixed layout and only remove the description.
3. Restore a root-level splitter.
4. Add a permanently live modeless inspector window.

## Recommendation

Choose option 1.

Keep the root three-domain tab widget. When both hierarchy and selected-object
details exist, the Scene page contains one vertical splitter with exactly two
stable children for its complete lifetime. The hierarchy is above the existing
Object or Object/Attributes detail surface. Initial stretch is 3:2, neither
child is collapsible, and selection or form updates never reset the user's
dragged allocation. Splitter position is transient UI state.

Remove the inline read-only object-description textbox. Keep editable controls
in the selected-object panel and add a fixed **Details** button at its bottom:

- no selection: show `No object selected` and disable Details;
- one selection: show editable controls and enable Details;
- multiple selection: show only a short count, no shared editing controls, and
  enable Details.

Details opens a read-only modal dialog owned by the main window. It snapshots
the current selection. For one object it shows name, represented type,
visibility, and complete inspected parameters. For multiple objects it shows
count, types, and names. It does not track later selection changes.

## Consequences

- Sidebar space is used for editable controls rather than duplicated prose.
- Users control the Scene hierarchy/detail allocation without destabilizing
  Annotations or System.
- No configuration, serialization, selection, or Core change is required.
- A live modeless inspector and persisted splitter position remain outside
  scope.

## Verification

- Verify the root remains the three-domain tab widget.
- Verify exactly one Scene-local splitter when both panes exist and none in
  Annotations or System.
- Verify user-set sizes survive zero, one, and multiple selection updates.
- Verify the inline description textbox is absent.
- Verify Details enablement and one/multiple-selection dialog content.
- Verify existing editable controls and optional Attributes routing remain
  unchanged.

## Dependencies

- Narrowly amends Accepted ADR 032's no-page-splitter rule.
- Preserves Accepted ADRs 015–018 and 032's domain ownership.

## Decision

Pending explicit approval.
