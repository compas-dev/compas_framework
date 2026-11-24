# ADR 041: Grid and Units System Section

## Status

Accepted.

## Context

The System sidebar currently separates grid controls into Display while unit,
precision, and nine read-only global-tolerance values occupy Units and
Measurement. Grid and coordinate units describe the same spatial presentation
context, whereas global COMPAS tolerance is not currently a Viewer setting and
cannot be changed there.

Camera and Display also rely on implicit row sizing with different editor
width limits. This produces inconsistent alignment and gives some controls less
usable width than others.

## Options

1. Add a Grid and Units section, remove tolerance from Viewer UI, and apply one
   System-form layout rule.
2. Keep separate Display and Units and Measurement sections but align them.
3. Make global tolerance editable from Viewer.
4. Change the generic container layout for every Viewer form.

## Recommendation

Choose option 1.

The closed System section set becomes, in order:

1. Camera
2. Display
3. Grid and Units

Display retains:

- Render Mode;
- Current View;
- Background Color; and
- Selection Color.

Grid and Units contains:

- Show Grid;
- Show Z Axis;
- Grid Mode;
- Grid Color;
- Grid X Extent and Divisions;
- Grid Y Extent and Divisions;
- Coordinate Unit; and
- Display Precision.

Replace the public `MeasurementSetting` component and sidebar item type with
`GridUnitSetting`. Replace the closed section identifier `Units and
Measurement` with `Grid and Units`. Remove the old names without aliases.

Remove every tolerance row and the component's dependency on
`compas.tolerance.TOL`. Do not modify, copy, or provide Viewer controls for the
process-wide tolerance object. Computational code may continue using COMPAS
tolerance internally.

Preserve the existing `renderer.*`, `measurement.*`, and
`ViewerState.set_measurement_*` paths. Unit remains an informational
declaration: it does not convert coordinates, grid spacing, snapping, geometry,
or measurements. Precision remains paired with the unit and controls
measurement formatting. Because configuration ownership and paths do not move,
no configuration-schema migration is introduced.

Camera, Display, and Grid and Units use one private two-column layout rule:

- labels occupy one left-aligned label column;
- editors occupy one aligned right-hand field column;
- editor rows share a common right edge;
- fields use the available column width rather than unrelated fixed maxima;
- checkboxes align within the same field column; and
- compact margins and row heights are retained.

Implement the rule privately in the three System components. Do not change the
generic `Container` or introduce a public form-layout abstraction.

## Consequences

- Spatial grid presentation, declared coordinate unit, and precision are
  available in one coherent section.
- Display becomes limited to general renderer presentation.
- Irrelevant global-tolerance information no longer consumes sidebar space,
  while COMPAS tolerance behavior remains unchanged.
- System controls use consistent alignment and gain usable editor width.
- Custom sidebar definitions using `MeasurementSetting` or the old section
  identifier require a clean update.
- Existing configuration files and runtime state paths remain valid.

## Verification

- Verify the exact Camera, Display, and Grid and Units section order and closed
  identifiers.
- Verify Display no longer owns grid controls and `GridUnitSetting` owns grid,
  unit, and precision controls.
- Verify no tolerance widgets or Viewer component dependency on `TOL` remains.
- Verify grid changes still rebuild only grid resources.
- Verify unit and precision changes affect measurement presentation without
  changing geometry, grid scale, snapping, or global tolerance.
- Verify fixed-width Qt layout tests give each System section a common field
  column, shared right edge, aligned checkboxes, and usable editor width.
- Verify the retired component type and section identifier fail clearly.
- Preserve configuration round-trip and Viewer-state tests, then run the full
  Viewer suite, Ruff, Pyright, strict MkDocs, package CI, and framework
  integration.

## Dependencies

- Amends Accepted ADR 027 by removing tolerance display while preserving unit
  and precision semantics.
- Amends Accepted ADR 032's closed System section and component-type sets.
- Preserves Accepted ADR 020's configuration ownership and schema.
- Coordinates with ADR 040 through shared render-mode and view state.

## Decision

Approved on 2026-11-09. System contains Camera, Display, and Grid and Units.
Grid and Units replaces `MeasurementSetting` with `GridUnitSetting`, owns grid,
coordinate-unit, and display-precision controls, and removes tolerance from the
Viewer UI without changing global COMPAS tolerance or existing configuration
and state paths. All three System sections use the approved private aligned
two-column layout. The retired component and section names receive no aliases.
