# ADR 044: Editing Persistent Distance-Dimension Format

## Status

Accepted; implemented, locally verified, and independently reviewed.

## Context

`DistanceDimension` durably owns its coordinate-unit declaration and display
precision. **Grid and Units** supplies defaults for transient measurements and
new dimensions, and accepted ADRs intentionally prevent later default changes
from rewriting existing dimensions.

The Annotations details panel currently exposes annotation name, type, and
dimension style only. Users therefore cannot correct the unit or precision
snapshot of an existing dimension. Core also validates these values only at
construction, so invalid later assignment can corrupt formatting state.

An unbounded precision also permits impractically large fixed-point output and
would leave Core data, Viewer configuration, and Viewer editors with different
effective domains. One bounded contract must apply at every boundary.

## Options

1. Add validated mutable Core properties and edit them in selected annotation
   details.
2. Validate only in Viewer and keep unsafe direct Core assignment.
3. Replace the selected dimension with a newly constructed object.
4. Make Grid and Units retroactively update existing dimensions.
5. Treat format as entry-owned style or add bulk format editing.

## Recommendation

Choose option 1.

Keep `DistanceDimension.unit` and `DistanceDimension.precision` publicly
assignable through validated properties. Construction uses the same setters.

- `unit` accepts `None` or a `str` that is non-empty after stripping
  whitespace. Core retains the supplied valid string without conversion or
  canonicalization.
- `precision` accepts a non-boolean integer from 0 through 15 inclusive.
- Rejected assignment raises before changing the stored value.
- Precision outside 0–15 raises `ValueError`; it is never clamped or
  truncated.
- Changing either field never rescales coordinates, anchors, or measured
  distance.
- Serialization fields and Scene schema remain unchanged.

For exactly one selected annotation entry whose semantic item resolves to a
`DistanceDimension`, the Annotations details area exposes a separate
**Measurement Format** group:

- **Coordinate Unit**
- **Display Precision**

This group is separate from **Dimension Style** because the values belong to
semantic dimension data rather than entry presentation. Hide the group for no
selection, multiple selection, text or arrow annotations, and unresolved data
bindings. A dimension with currently unresolved associative anchors remains
editable because its data item is still available.

Viewer trims unit input and maps blank input to `None`. Precision is assigned
through the Core property. Synchronization blocks editor signals. Commit only
when the stored value changes and refresh only the affected annotation through
`viewer.refresh_annotations((entry,))`. Unit Escape restores the durable value,
clears editor focus, and does not trigger global deselection.

Mutation preserves dimension and entry identity, anchors, optional explicit
label, style, ordering, visibility, both selections, Viewer measurement
defaults, spatial hierarchy, and spatial buffers. An explicit label remains a
verbatim override, so stored format edits may intentionally produce no visible
label change until that override is removed. The override does not relax unit
or precision validation.

**Grid and Units** continues to control transient formatting and the snapshot
copied into dimensions created afterward. It never becomes a bulk or
retroactive editor.

## Consequences

- Existing dimensions can be corrected without losing identity or
  associations.
- Core enforces its format invariants after construction and deserialization.
- Viewer defaults and durable per-dimension format remain distinct.
- No unit conversion, schema migration, configuration migration, generic
  property editor, or bulk editing is introduced.
- Invalid post-construction assignments that previously succeeded now fail
  immediately under the already documented invariant.

## Compatibility

Existing scenes whose dimensions use precision within 0–15 require no
migration. Valid direct assignment remains source-compatible. Invalid
assignment raises `TypeError` for non-string units, boolean or non-integer
precision; `ValueError` for blank units and precision outside 0–15. Blank
Viewer input maps to `None` before Core assignment. Existing serialized
dimensions or Viewer configurations containing precision above 15 are rejected
and must be corrected before loading; they are not migrated, clamped, or
truncated. Scene and Viewer configuration schema versions remain unchanged.

## Verification

- Verify valid reassignment at 0 and 15, invalid atomic rejection at -1 and 16,
  formatting, explicit labels, unchanged distance and anchors, and
  serialization round-trip.
- Verify the group appears only for one resolved distance-dimension item,
  including geometrically unresolved associative anchors.
- Verify unit trimming, blank-to-`None`, precision editing, signal-blocked
  synchronization, and editor-local Escape.
- Verify identity, anchors, style, selection, Viewer defaults, hierarchy, and
  spatial buffers remain unchanged.
- Verify exactly one annotation refresh and no sidebar rebuild.
- Verify default changes do not rewrite existing dimensions and subsequently
  created dimensions receive current defaults.
- Update Core property docstrings, Viewer guides, examples, and changelogs;
  run focused/full package checks and framework integration.

## Dependencies

- Amends ADR 022: snapshots resist automatic default changes but are explicitly
  editable afterward.
- Clarifies ADR 027 and ADR 041: Grid and Units remains a default-setting
  surface, not an existing-dimension editor.
- Amends ADR 029 and ADR 032: selected annotation details gain semantic
  Measurement Format controls separate from entry-owned style.

## Decision

Approved on 2026-11-10. Existing dimensions gain validated mutable unit and
precision properties and selected-annotation Measurement Format controls under
the contract above. Grid and Units remains a default-setting surface for
transient and newly created measurements and never rewrites existing
dimensions automatically.

Amended on 2026-11-10 to set one shared Core and Viewer precision domain of
0–15 inclusive. Values outside that range raise `ValueError`; no assignment,
configuration load, or deserialization path clamps or truncates them. Explicit
labels do not bypass validation. Existing data or configuration above 15 is
rejected without migration or a schema-version change.

## Implementation and verification

Core and Viewer implementation is present in the working trees. Core routes
construction and later assignment through the same validated `unit` and
`precision` properties. Viewer exposes Measurement Format only for one bound
distance dimension, trims unit text, maps blank input to `None`, and refreshes
only the affected annotation. The approved 0–15 domain applies consistently to
Core assignment, Viewer configuration, and both Viewer editors.

The full Core suite passes 2,264 tests. The Viewer tree before the final toolbar
follow-up passes 575 tests plus one expected structured OpenGL skip. The final
combined Viewer tree passes 587 plus the same expected skip. Independent focused
review passes 92 Core and 83 Viewer tests with no remaining findings.
Strict Core and Viewer documentation checks pass, and the framework
direct-source gate passes 15 tests with one expected exact-revision skip.
Hosted package CI and candidate-artifact verification have not been run for
these working trees.
