# ADR 049: Viewer Settings Surface

## Status

Proposed on 2026-11-13. No implementation is authorized.

## Context

The default Viewer sidebar currently presents **Scene**, **Data**,
**Annotations**, and **System** as peer domains. The first three are projections
of content in the active session context: spatial scene objects, referenced
data, and durable annotations. System is different. It is a collection of
Viewer controls for Camera, Display, and Grid and Units.

Treating content and settings as equivalent top-level domains obscures that
ownership distinction. It also makes the content sidebar responsible for a
large settings form even though those controls are not selected objects or
data. The existing controls, configuration paths, and live refresh behavior
are otherwise established and should not be redesigned as part of correcting
their placement.

## Options

1. Move the existing settings sections into one modeless **Viewer Settings**
   window owned by each Viewer.
2. Use a modal settings dialog.
3. Use a second dock or dockable panel.
4. Use a toolbar popover or viewport drawer.
5. Keep System as a fourth content-sidebar tab.

## Recommendation

Choose option 1.

The built-in right sidebar contains exactly three top-level content domains,
in this order:

1. Scene
2. Data
3. Annotations

`UI` owns one modeless **Viewer Settings** window per Viewer. It contains the
existing sections, in their current order:

1. Camera
2. Display
3. Grid and Units

Construct the window after the viewport and keep it hidden initially. Opening
it refreshes controls from the current Viewer state, shows and raises the same
window instance, and optionally focuses one of the closed section identifiers.
Closing the settings window hides rather than destroys it. Its visibility,
geometry, scroll position, and active section remain transient UI state; they
are not serialized and do not extend Viewer configuration.

The primary entry is **View → Viewer Settings…**. The existing Camera Settings
command opens the same window focused on Camera. Repeated commands must reuse
the owned window rather than create independent surfaces.

Keep editor-local Escape behavior local. Escape handled by the settings window
hides that window and must not cancel an active measurement or clear spatial
or annotation selection in the main window. Closing the main Viewer window
also closes the owned settings window and releases its Qt resources.

Use one clear composition and navigation path:

```python
SidebarTab = Literal["Scene", "Data", "Annotations"]
SettingsSection = Literal["Camera", "Display", "Grid and Units"]

viewer.ui.settings.show(section: SettingsSection | None = None)
```

Remove `SideBarRight.focus_system_section`. Move `CameraSetting`,
`DisplaySetting`, and `GridUnitSetting` from `viewer.sidebar_items` to a new
`viewer.settings_items` composition boundary. If `SystemPanel` and
`SystemSection` remain public, rename them to Viewer-settings terminology.
Retire the old System placement and identifiers without compatibility aliases
or two supported navigation paths.

Preserve the existing `renderer.*`, `measurement.*`, state, configuration,
refresh, and command semantics. This proposal changes presentation ownership,
not the controlled values.

## Alternatives and Tradeoffs

A modal dialog gives settings a separate surface but blocks viewport orbit,
pan, zoom, and selection while Camera, Display, or Grid values are tuned. That
conflicts with the existing live-feedback behavior.

A dock keeps controls modeless but competes with the content sidebar and the
generic Side Dock for main-window space. It also introduces docking position,
visibility persistence, and layout-restoration decisions that are not required
to correct the ownership boundary.

A toolbar popover is too small and lifecycle-sensitive for three scrollable
forms. It would repeat the popup and focus-teardown risks already encountered
by the Viewer controls. A viewport drawer adds new chrome and accessibility
behavior without a current requirement.

Keeping System in the sidebar preserves the implementation but retains the
content/settings category error identified by direct use.

## Consequences

- The right sidebar becomes a coherent content navigator.
- Settings remain available during viewport interaction and provide live
  feedback from one reusable surface.
- Viewer, not Scene or Session, continues to own Camera, Display, and Grid and
  Units presentation.
- Core APIs, Scene serialization, Viewer configuration schema 4, measurement
  semantics, and renderer state do not change.
- Custom applications using `viewer.sidebar_items` for settings,
  `set_current_tab("System")`, or `focus_system_section` require a clean
  migration.
- The new settings composition boundary must not become a generic dock,
  workspace, or persistence framework.

## Verification

- Verify exactly Scene, Data, and Annotations in the default content sidebar.
- Verify Data remains read-only and contextual deletion remains limited to
  Scene and Annotations.
- Verify one modeless settings window per Viewer, reused across repeated open
  and section-focus commands.
- Verify opening refreshes Camera, Display, and Grid and Units from current
  state without duplicating signal connections or refresh work.
- Verify close hides the settings window and main-window teardown closes it
  without Qt lifetime errors.
- Verify editor-local Escape remains local and window-level Escape hides only
  Viewer Settings without cancelling measurement or clearing selection.
- Verify keyboard traversal, accessible names and title, light/dark styling,
  high-DPI layout, minimum sizing, and scrolling.
- Verify Camera, Display, grid, unit, and precision edits preserve their
  existing live refresh scope.
- Verify configuration schema 4 round-trip and every existing state path are
  unchanged.
- Update the Viewer user guide, developer composition guide, changelog,
  package tests, and framework integration assertions.

## Dependencies

- Amends ADR 032's top-level sidebar and navigation contract.
- Moves, but does not change, ADR 041's Camera, Display, and Grid and Units
  sections.
- Preserves ADR 038's contextual deletion ownership.
- Preserves ADRs 040, 043, and 046 for controls, theme, and content palette.
- Follows ADR 048 by treating Scene, Data, and Annotations as the content
  domains.

## Approval Gate

Approve the modeless Viewer Settings ownership, clean API migration, and
verification contract before changing Viewer runtime code. This proposal does
not authorize implementation, compatibility aliases, a dock framework, or
settings persistence.
