# ADR 022: Distance-Dimension Unit Semantics

## Status

Accepted.

## Context

Accepted ADR 005 requires a distance dimension to store a unit and precision.
The user also requires Viewer-level unit, precision, and tolerance settings
with UI exposure. The framework currently has no approved scene-unit owner or
conversion service, and Accepted ADR 020 deliberately removed the old Viewer
root `unit` field until a coordinated unit-aware workflow has an approved owner
and lifecycle.

Treating a unit label as an implicit conversion request would therefore hide
an unknown source unit and produce unverifiable values.

## Options

1. Snapshot the active Viewer measurement unit and precision when a persistent
   dimension is created; the unit declares the coordinates' unit and performs
   no conversion.
2. Require unit and precision explicitly for every persistent dimension,
   independent of Viewer settings.
3. Add separate source and display units with conversion infrastructure in
   this phase.

## Recommendation

Choose option 1, dependent on approval of ADR 027.

Persistent dimensions snapshot unit and precision at creation so their durable
labels do not change when Viewer preferences change later. Explicit
construction arguments may override the current settings. Transient
inspections use the current Viewer unit and precision without creating a
durable snapshot.

`DistanceDimension.unit` is `str | None`. For example, `unit="mm"` declares
that the stored coordinate distance is already expressed in millimetres. It
appends `mm` to the formatted value but never rescales coordinates.

`precision` is a non-negative number of decimal places. The derived label uses
fixed-point formatting and separates a non-empty unit from the value with one
space. A non-`None` explicit label is displayed verbatim instead of the
derived value.

Tolerance remains Viewer measurement behavior governed by ADR 027; it is not
stored on every dimension. Do not add a supported-unit registry, spelling
normalization, localization, source-unit inference, or conversion factor in
this phase. Actual conversion depends on a separate framework-wide unit
decision.

## Consequences

- Formatting is deterministic and honest about the available information.
- Callers and Viewer remain responsible for supplying coordinates in the
  declared unit.
- The unit string is descriptive rather than computational.
- Durable dimensions remain stable when Viewer measurement preferences change.
- Later conversion infrastructure may extend construction explicitly, but it
  must not silently change existing serialized meaning.

## Compatibility

There is no existing distance-dimension payload. This decision establishes the
initial serialized semantics without reviving the removed Viewer root unit.

## Verification

- Derive and format distances with no unit and with an explicit unit.
- Verify zero and multiple precision values.
- Reject negative precision and invalid unit values precisely.
- Verify an explicit label bypasses derived numeric and unit formatting.
- Verify serialization preserves unit, precision, and label without adding a
  conversion factor or source-unit field.
- Verify persistent creation snapshots Viewer settings while transient
  inspection reads their current values.
- Verify later Viewer-setting changes do not rewrite existing dimensions.

## Dependencies

- Depends on proposed ADR 021 for `DistanceDimension` ownership and schema.
- Depends on proposed ADR 027 for Viewer measurement-setting ownership.
- Refines Accepted ADR 005.
- Respects Accepted ADR 020's removal of the unowned Viewer root unit.

## Decision

Approved on 2026-11-08. Persistent dimensions snapshot the active Viewer unit
and precision at creation, while transient inspections use their current
values. The unit declares the coordinates' existing unit and formats a suffix;
it never performs implicit conversion. Durable dimensions retain their
snapshot when Viewer preferences change, and tolerance is not duplicated on
each dimension. The rationale is deterministic, honest formatting without an
unowned source unit or hidden conversion.


