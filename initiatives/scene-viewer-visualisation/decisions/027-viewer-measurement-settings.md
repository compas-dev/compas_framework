# ADR 027: Viewer Measurement Settings and UI

## Status

Proposed.

## Context

Unit, precision, and tolerance are important Viewer measurement information
and presentation settings and must be visible through the UI. Accepted ADR 020
removed the old unowned root `unit` field and treats direct configuration
mutation as setup-only, so reintroducing editable values requires explicit
ownership, lifecycle, and mutation semantics.

COMPAS global tolerance is process-wide numerical infrastructure. A Viewer
control must not silently mutate it or imply that display preferences change
geometry algorithm tolerances.

## Options

1. Add Viewer-owned unit and precision presentation defaults and show the
   active COMPAS tolerance context read-only in one dedicated UI panel.
2. Add an explicit, clearly labeled operation for changing process-wide COMPAS
   tolerance from Viewer.
3. Copy global tolerance into an independent editable Viewer field.
4. Keep all three values transient and omit them from Viewer configuration.

## Recommendation

Choose option 1 unless an explicit process-wide tolerance editing workflow is
separately approved.

Add one typed `measurement` group to Viewer configuration:

- `unit: str | None` declares the coordinate unit used for measurement labels;
- `precision: int` controls displayed decimal places; and
- tolerance information reports the active numerical tolerance context used by
  COMPAS computations; it is not a private Viewer substitute.

Expose the values through one **Units and Measurement** sidebar tab. Unit and
precision are presentation settings used by transient labels and snapshot into
persistent dimensions according to ADR 022. The recommended first version
shows tolerance read-only and identifies its owner. Whether the same panel may
edit process-wide tolerance remains unresolved and requires explicit approval;
it must never happen as a side effect of editing Viewer presentation.

Unit, precision, and displayed tolerance are informational or presentational;
they are not sources of geometric correctness. Snap resolution and component
association follow ADRs 026 and 028. The UI does not reinterpret precision as
a geometric tolerance or silently mutate `compas.tolerance.TOL`.

Persistent dimensions snapshot unit and precision according to ADR 022.
Transient inspection reads the current settings. Tolerance remains referenced
numerical context rather than being copied into every durable dimension or
duplicated as independent Viewer state.

## Consequences

- Measurement presentation and numerical tolerance context are discoverable.
- Runtime changes are explicit and validated instead of depending on arbitrary
  dataclass mutation.
- Viewer presentation remains distinct from computational geometry tolerance.
- A later framework-wide unit-conversion design may extend these settings but
  cannot silently reinterpret the initial declaration-only unit.

## Compatibility

This is a new schema field with an explicit owner. It does not restore the old
root `unit` field or weaken schema-2 rejection of that retired path. Its schema
version and migration must be coordinated with the next approved Viewer
configuration version.

## Verification

- Validate unit and precision with complete configuration paths and show the
  active tolerance source accurately.
- Verify setup serialization, schema migration, explicit runtime updates, and
  UI synchronization.
- Verify transient inspection responds to current settings.
- Verify persistent dimensions retain snapshot unit and precision after later
  setting changes.
- Verify ordinary Viewer setting changes never mutate COMPAS global tolerance.
- If tolerance editing is later approved, verify it is explicit, process-wide,
  and cannot be confused with Viewer-only state.
- Verify the measurement panel does not promise snapping or unit conversion.

## Dependencies

- Refines Accepted ADR 005 and proposed ADR 022.
- Amends the scoped configuration lifecycle of Accepted ADR 020 without making
  general Viewer configuration reactive.
- Coordinates with proposed ADR 026 measurement interaction.
- Respects Accepted ADR 028: presentation settings do not determine whether an
  anchor is fixed, associative, resolved, or geometrically correct.

