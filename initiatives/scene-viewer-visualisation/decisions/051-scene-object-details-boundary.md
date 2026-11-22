# ADR 051: Scene Object Details and Settings Boundary

## Status

Accepted on 2026-11-14. Implemented and locally verified in the uncommitted
Viewer working tree based on `0f263f1`.

## Context

Accepted ADRs 015–016 make Object Settings the editing surface for one
normalized mapping of declared editable SceneObject attributes. Accepted ADR
033 moves descriptive information to a read-only modal Object Details snapshot.
That snapshot currently shows name, represented-item type, visibility, and
safe represented-item parameters for one object.

Users need access to general SceneObject identity and presentation plus the
declared type-specific state, including noneditable values. Expanding the
snapshot must not create a second editor, infer arbitrary object attributes, or
duplicate the authoritative editability contract.

## Options

1. Expand Object Details with explicit read-only SceneObject sections while
   retaining Object Settings as the only editing surface.
2. Put every inspected value into Object Settings and make it editable where
   possible.
3. Build a generic introspection or metadata registry for SceneObject details.
4. Keep the current minimal snapshot.

## Recommendation

Choose option 1.

For one selected object, keep one main-window-owned modal snapshot and show the
existing read-only scrolling text surface with sections in this order:

1. **Identity**;
2. **General Scene State**;
3. **Type-Specific Scene State**; and
4. **Represented Item Parameters** when the item is bound.

Identity contains the SceneObject name, concrete SceneObject type, SceneObject
GUID, represented-item concrete type, item GUID, and Bound or Unresolved
status. Rows use `Label: value` with labels **Name**, **Scene Object Type**,
**Scene Object GUID**, **Represented Type**, **Item GUID**, and **Status** in
that order.

General Scene State contains the explicit base values already owned by
`SceneObject`: visibility, base color, opacity, and local transformation. These
are displayed even when a corresponding value is not editable in the current
Viewer context, with labels **Visible**, **Base Color**, **Opacity**, and
**Local Transformation** in that order.

Type-Specific Scene State enumerates only the declarations returned by
`type(obj).scene_state_fields()`. Preserve namespace and field declaration
order. Display each stable `namespace.field` name and read its current value
through the declaration's `attribute`. Include editable and noneditable fields.
Do not inspect unknown extension payloads, `__dict__`, arbitrary properties, or
undeclared adapter caches.

Represented Item Parameters reuses the existing safe parameter inspection. An
unresolved represented item omits that section while retaining complete
SceneObject identity and declared state.

Identity values use their canonical string form. General state, type-specific
state, and represented-item parameter values use `repr(value)`. A failure to
read or format one value renders `<unavailable: ExceptionType>` for that row
and does not prevent the remainder of the snapshot from opening. Parameter rows
retain the existing `<not exposed by object>` marker when inspection identifies
a constructor parameter but cannot safely resolve its value. Details remains a
snapshot and does not track later selection or mutation.

Keep existing multiple-selection Details unchanged: show count, represented
types, and names only. A merged multi-object state inspector, common-value
calculation, or multi-edit surface requires separate evidence.

## Editing Boundary

Object Settings remains the single editing surface. It continues to resolve
ADRs 015–016's normalized Viewer-context mapping, use existing presentation
labels and editors, apply atomic mutation, and select the required refresh.
Object Details adds no setters, controls, callbacks, refresh metadata, or
mutation path.

Represented-item parameters remain descriptive in Details and follow the
separate existing ParameterForm path where that form is explicitly invoked.
This decision does not make arbitrary represented-item parameters editable in
Object Settings.

## Alternatives and Tradeoffs

Adding all values to Object Settings would blur inspection with editability,
duplicate or bypass ADRs 015–016, and require editor/validation/refresh
contracts for noneditable state. It is rejected.

A generic details registry could provide custom labels and sections, but it
would duplicate stable SceneStateField declarations and add speculative
presentation metadata to Core or plugins. Explicit base fields plus declared
scene state satisfy the current requirement without a new extension boundary.

Keeping the current snapshot avoids UI work but hides object identity,
transformation, presentation, and noneditable type-specific state.

## Compatibility

The change is additive within the modal Details snapshot. SceneObject APIs,
editability, serialization, selection, configuration, and refresh behavior do
not change. No Core source, schema, migration, alias, or new public metadata
type is required.

## Verification

- Show the exact Identity and General Scene State fields for a bound object.
- Preserve namespace and declaration order for editable and noneditable
  `scene_state_fields()` values across representative Geometry, Mesh, Graph,
  Shape, Surface, and noneditable-state objects.
- Show declared SceneObject state for an unresolved item while omitting only
  Represented Item Parameters.
- Isolate one read/format failure without losing the remaining snapshot.
- Keep Details read-only and prove it causes no mutation, refresh, redraw,
  serialization, selection, or history change.
- Preserve the existing multiple-selection count/type/name snapshot.
- Verify Object Settings still contains exactly the normalized editable
  Viewer-context mapping and remains the sole editing path.
- Extend the Viewer tutorial and examples to distinguish SceneObject settings,
  Object Details, represented-item parameters, Data Details, and Viewer
  Settings across representative built-in object types.

## Dependencies

- Amends Accepted ADR 033's one-object Details content.
- Preserves Accepted ADRs 015–016 as the authoritative editability and mutation
  contract.
- Uses Accepted ADR 013's stable SceneObject and declared scene-state model.
- Independent of Accepted ADR 050; either decision may be implemented and
  verified separately.

## Implementation Evidence

The Viewer implementation renders the four ordered one-object sections from
explicit base state and declared `scene_state_fields()` while leaving Object
Settings unchanged as the only editor. Focused Scene-form tests pass within the
55-test implementation check. The complete Viewer suite passes 705 tests with
two expected offscreen native OpenGL skips. Viewer Ruff, formatting, package
Pyright with zero errors, strict MkDocs, and `git diff --check` pass. The
framework direct-source gate passes 16 tests with one expected exact-revision
skip and covers declared noneditable state, section ordering, and nonmutation.
Native visual and interaction confirmation, refreshed hosted CI, and
candidate-artifact verification remain separate pending layers.

## Acceptance Scope

The user accepted the explicit read-only sections and the retained Object
Settings editing boundary on 2026-11-14. Acceptance does not authorize new
editable attributes, a details registry, merged multi-selection state,
arbitrary introspection, or Core changes.
