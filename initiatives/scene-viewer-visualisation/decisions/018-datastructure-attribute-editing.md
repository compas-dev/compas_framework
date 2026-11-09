# ADR 018: Datastructure Element-Attribute Editing

## Status

Accepted.

## Context

ADR 017 defines lazy Viewer tables for declared Mesh and Graph element
attributes. Editing needs a narrow value-type, mutation, selection, and refresh
contract. Without one, delegates could silently change types, bypass
datastructure semantics, or couple table selection to viewport object
selection.

## Options

1. Edit supported declared values through singular datastructure APIs and keep
   table interaction local.
2. Write directly into internal element dictionaries.
3. Add batch editing, default-schema editing, undo, and viewport selection in
   the first version.
4. Treat all values as editable text.

## Recommendation

Choose option 1.

Editor choice follows the declared default value's exact supported type:

- `bool`;
- `int`;
- `float`; and
- `str`.

Other default types are displayed read-only. The table shows effective values
through the singular getter, including inherited defaults. A successful edit
uses the matching singular setter. Reset uses the singular unset operation so
the effective value falls back to its declared default rather than copying the
default into local storage.

Table row/cell selection is local to the table. It does not mutate Viewer
object selection, viewport picking, or a future component-selection model.

After a successful mutation, Viewer conservatively refreshes the affected
scene object's render data, redraw, and relevant UI. Failed validation or
mutation leaves the datastructure and displayed value unchanged and triggers
no refresh.

The initial version does not edit default attribute definitions, scan or add
sparse undeclared attributes, batch-edit cells, add undo/redo transactions, or
link table selection to viewport selection.

## Consequences

- Editing preserves datastructure validation and default/local semantics.
- Unsupported values remain visible without unsafe coercion.
- Conservative refresh favors correctness before optimization.
- Bulk operations, history, and component selection remain separately
  decidable features.

## Compatibility

No core API or serialized data format changes. Existing singular getters,
setters, and unset operations remain authoritative.

## Verification

- Select Boolean, integer, float, and text editors from default value types,
  distinguishing `bool` from `int`.
- Display unsupported types read-only.
- Mutate through each singular setter and reset through each singular unset
  operation.
- Display effective inherited defaults without inserting local values.
- Keep table selection independent of Viewer and viewport selection.
- Verify failed edits are atomic and successful edits invoke one conservative
  Viewer refresh path.
- Verify no default editing, sparse scan, batch edit, undo, or viewport
  component-selection behavior appears in the initial implementation.

## Dependencies

- Depends on Accepted ADR 017 for the lazy table model and declared columns.
- Uses Viewer refresh ownership established by ADRs 006 and 016 without
  extending the scene-object editable-attribute mechanism.

## Decision

Approved on 2026-11-08. The initial editor supports only declared Boolean,
integer, float, and text values; mutations and resets use the existing singular
datastructure APIs, table selection remains local, and successful changes use
one conservative Viewer refresh path. The rationale is to preserve declared
types and default/local semantics without unsafe coercion, direct dictionary
writes, batch operations, undo, or viewport component-selection coupling.
