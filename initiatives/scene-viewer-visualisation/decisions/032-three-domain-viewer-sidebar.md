# ADR 032: Three-Domain Viewer Sidebar

## Status

Accepted.

## Context

The current right sidebar places the Scene tree, the flat Annotations panel,
and a shared Object/Camera/Display/Units tab form in one vertical splitter.
Selecting an annotation changes the annotation panel's size hint and updates
the complete sidebar, which redistributes the other panels. Spatial-object
details remain visible at the same time as annotation details even though the
two selections are intentionally independent. This makes the retained object
selection look stale or incorrectly connected to the annotation selection.

Annotation details are embedded below the annotation list, annotation naming
depends on an undiscoverable inline tree edit, and neither an empty viewport
click nor the effective window-level Escape shortcut clears annotation
selection. The resulting UI does not give Scene, annotation, and system
settings clear ownership or a stable master/detail layout.

## Options

1. Replace the stacked sidebar with three top-level domains: **Scene**,
   **Annotations**, and **System**.
2. Keep the current splitter and repair its sizing, update routing, and
   selection behavior.
3. Introduce one union selection shared by spatial objects and annotations.
4. Make spatial and annotation selection mutually exclusive.

## Recommendation

Choose option 1.

`SideBarRight` becomes one full-height tab widget with exactly three built-in
tabs:

- **Scene** contains the spatial hierarchy and the selected spatial object's
  details and controls.
- **Annotations** contains the ordered annotation list and the selected
  annotation's details and controls.
- **System** contains Camera, Display, and Units and Measurement sections.

Scene and Annotations use ordinary vertical layouts with a stable
master/detail allocation. The sidebar must not use a splitter whose sizes are
recomputed when a selection changes or a detail form is rebuilt. System uses
one scrollable page of clearly labeled sections rather than adding more
top-level tabs. The active tab is transient UI state, defaults to Scene, and
does not require a Viewer configuration schema change.

Keep `ViewerState.selection` and `ViewerState.annotation_selection` as
independent typed selections. They may both contain values and are preserved
when tabs change. Spatial picking and the Scene tree change only spatial
selection. The annotation list changes only annotation selection. The design
does not add a union or active-selection abstraction.

An unmodified click on empty viewport background clears both selections.
Ctrl-click on empty background remains a no-op. Escape first cancels an active
measurement and stops; otherwise it clears both selections. An editor that
owns Escape retains its normal local behavior. Annotation-list Delete removes
annotations only, while spatial Delete retains ADR 031's behavior.

The annotation Name column is display-only. For exactly one selected
annotation, the details area exposes an explicit Name field, read-only Type,
and the supported distance-dimension style controls. Name commits update the
annotation collection and list without rebuilding render resources. Style
edits refresh only the affected annotation layer. No selection shows a clear
empty state; multiple selection shows a summary and the supported removal
operation rather than an ambiguous single-item form.

Commands address the sidebar through a narrow tab/section navigation boundary
instead of reaching into generic form internals:

```python
SidebarTab = Literal["Scene", "Annotations", "System"]
SystemSection = Literal["Camera", "Display", "Units and Measurement"]

class SideBarRight:
    def set_current_tab(self, tab: SidebarTab) -> None: ...
    def focus_system_section(self, section: SystemSection) -> None: ...
```

The strings above name the complete accepted identifier sets, not arbitrary
extension values. Either method raises `ValueError` for an unsupported value.
`focus_system_section` activates System before focusing the requested section.
In particular, Camera Settings uses it to activate System and focus Camera.

Existing sidebar-item component types remain the extension input for this
migration and are routed by domain:

- `SceneTree`, `ObjectSetting`, and optional `DatastructureAttributes` belong
  to Scene;
- `AnnotationPanel` belongs to Annotations; and
- `CameraSetting`, `DisplaySetting`, and `MeasurementSetting` belong to
  System.

The datastructure inspector remains omitted from the default composition. When
it is explicitly added through `viewer.sidebar_items`, it appears in Scene.

## Consequences

- Scene, annotation, and system controls have explicit and stable ownership.
- Spatial and annotation context can coexist without being presented as one
  selection.
- Annotation naming and detail editing become discoverable.
- Background click and Escape provide predictable global deselection.
- The sidebar no longer resizes unrelated panels when annotation details
  change.
- Viewer sidebar composition and interaction tests require a coordinated
  update; Core Scene and its serialization require no change.

## Compatibility

This is a clean Viewer UI-composition change. It preserves the existing
spatial and annotation state models, durable annotation collection, Viewer
configuration schema, and optional sidebar component types. Code that reaches
through the sidebar into the old shared tab form is internal and must migrate
to the explicit sidebar navigation boundary. No compatibility layer for the
old visual arrangement is required.

## Verification

- Verify exactly three built-in top-level tabs and their component ownership.
- Verify no root or page splitter redistributes panes after selection or form
  updates.
- Verify explicit annotation Name editing and the single, multiple, and empty
  annotation-detail states.
- Verify object picking affects only spatial selection and annotation-list
  interaction affects only annotation selection.
- Verify tab switching preserves both selections.
- Verify an unmodified empty viewport click clears both selections and
  Ctrl-click does not.
- Verify real-window Escape cancels an active measurement first and otherwise
  clears both selections, including when the viewport or a tree has focus.
- Verify editor-local Escape, annotation Delete, and spatial Delete retain
  their distinct ownership.
- Verify Camera Settings activates System and focuses Camera.
- Verify optional datastructure attributes are absent by default and route to
  Scene when explicitly configured through `viewer.sidebar_items`.
- Update Viewer user and developer documentation for the three domains and
  selection behavior.

## Dependencies

- Refines Accepted ADRs 003, 027, 029, and 031.
- Preserves ADR 029's separate annotation collection and selection.
- Preserves ADR 031's separate spatial deletion operation.
- Requires no Core change.

## Decision

Approved on 2026-11-09. Viewer replaces the mixed stacked sidebar with stable
Scene, Annotations, and System domains. Spatial and annotation selections
remain independent and survive tab changes; empty-background click and Escape
clear both after measurement-cancel precedence. Annotation naming moves to an
explicit detail form, and commands use the closed sidebar tab/section
navigation boundary recorded above.
