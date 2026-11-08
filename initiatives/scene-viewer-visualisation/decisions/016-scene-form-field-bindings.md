# ADR 016: Scene Form Field Bindings

## Status

Accepted.

## Context

ADR 015 requires one small declarative contract that links a form field to its
actual owner. The initial use cases need to edit either stable presentation
state on a `SceneObject` or a supported parameter on its externally bound
represented item. The contract must make ownership, mutation, refresh, and
failure behavior explicit without growing into a general form language.

## Options

1. Use flat, named attribute bindings with a fixed initial editor and refresh
   vocabulary.
2. Accept arbitrary getters, setters, callbacks, validators, and refresh
   functions on every field.
3. Resolve dotted paths dynamically from arbitrary runtime objects.
4. Infer editable fields from annotations, constructor signatures, or
   `hasattr` checks.

## Recommendation

Choose option 1.

Each field declares only:

- a form-unique `id`;
- a user-facing `label`;
- `target`, either `sceneobject` or `item`;
- one flat named `attribute`;
- `editor`, initially `boolean`, `number`, `text`, or `color`;
- `refresh`, either `draw` or `geometry`;
- an explicit numeric `order`; and
- an optional flat `section` label.

`sceneobject` targets bind a named public attribute of the stable scene object.
`item` targets bind a named writable attribute or supported parameter of the
explicitly bound represented item. Dotted paths, implicit item loading, nested
schemas, arbitrary widget factories, and per-field executable callbacks are
outside the initial contract.

Before displaying an editable control, Viewer resolves the complete binding
and verifies that the target and attribute are available and writable. An
unresolved external item never triggers loading or lookup beyond the scene's
existing binding. Its item-targeted fields are omitted from the form.

Mutation uses `setattr` on stable scene-object attributes. Item parameters
reuse the existing represented-item parameter mutation and rollback behavior
where it applies. A failed setter restores the previous value and control,
reports the original exception, and performs no refresh.

After a successful mutation:

- `draw` refreshes the object's appearance using existing render data;
- `geometry` rebuilds the object's render data and then redraws it.

Form descriptors, resolved bindings, control values, validation errors, and
refresh state are transient Viewer state and are never serialized with a scene
or represented item.

## Consequences

- Ownership is visible at every field rather than inferred from similarly
  named attributes.
- All contextual fields share one mutation, failure, and refresh path.
- The initial editor vocabulary matches existing Viewer controls.
- More complex editors or bindings require evidence and an amendment rather
  than hidden escape hatches.
- The API may later gain narrowly justified metadata without revisiting the
  Viewer ownership decision in ADR 015.

## Compatibility

Built-in object-settings controls map to equivalent declarative fields. The
general represented-item parameter dialog remains a separate explicit command
during the initial migration. No serialized scene format or represented-item
format changes.

## Verification

- Mutate a stable scene-object attribute and the intended represented-item
  parameter through separate fields.
- Verify `draw` and `geometry` invoke only their specified refresh behavior.
- Verify read-only or missing attributes do not produce an editable binding.
- Verify a failed setter restores the old object and control values, reports
  the failure, and does not redraw.
- Verify unresolved external items omit item-targeted fields without loading
  data implicitly.
- Verify supported Boolean, numeric, text, and color fields use the existing
  Viewer controls consistently.
- Prove field and binding state is absent from scene and item serialization.

## Dependencies

- Depends on Accepted ADR 015 for contribution registration, lookup, and
  lifecycle.
- Reuses accepted stable scene-object and external item-binding semantics from
  ADRs 010 and 013.

## Decision

Approved on 2026-11-08. Contextual fields use flat named bindings with explicit
ownership, editor, order, and refresh semantics. The rationale is to provide
one transparent mutation and rollback path for stable scene-object attributes
and already-bound item parameters without arbitrary callbacks, dotted paths,
implicit loading, serialized UI state, or a general schema framework.
