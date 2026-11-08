# ADR 015: Contextual Scene Form Contributions

## Status

Accepted.

## Context

Viewer's object-settings form currently decides which controls to show through
hardcoded attribute checks on private render helpers. This couples the form to
renderer aliases, makes capability exceptions such as face-less graph objects
ad hoc, and gives external packages no supported way to expose a specific
stable scene-object attribute or represented-item parameter.

The accepted scene architecture keeps durable `SceneObject` types stable and
backend-neutral. ADR 014 deliberately limits core's context-keyed scene
operation registry to `draw` and `clear`. Forms, controls, layout, and refresh
behavior are Viewer UI concerns and must not become serialized scene state.

## Options

1. Add a Viewer-owned registry of declarative form contributions.
2. Let plugins construct and return arbitrary Viewer or Qt components.
3. Add form operations to core's context-keyed scene operation registry.
4. Store form annotations on durable scene-object classes or instances.
5. Retain hardcoded `hasattr`-based form construction.

## Recommendation

Choose option 1.

`compas_viewer` owns a runtime registry keyed by:

```text
(context, form, stable scene-object type, contribution ID)
```

The initial public form identifier is only `object-settings`. Registration is
lightweight and may occur during ordinary plugin discovery without importing
Qt, OpenGL, or another graphics runtime. A provider is called only when that
form is populated. It receives the stable scene object and the explicit
transient Viewer/runtime context, and returns declarative field links governed
by ADR 016.

Applicable contributions are collected through the stable scene-object MRO,
from general types to specific types. Fields are sorted deterministically by
`(field.order, general-to-specific MRO rank, contribution_id,
provider-return sequence)`. Registering the same exact registry key twice is
an error. Producing the same final field ID twice is also an error; a more
specific provider does not silently replace another provider's field.

If a provider raises, Viewer aborts population of the complete form and
reports the context, form identifier, stable scene-object type, and
contribution ID. It never silently omits a failed contribution or exposes a
partially rebuilt form.

The Viewer creates the controls, applies its consistent layout and lifecycle,
and performs mutations through one binding path. Providers do not return
ready-made widgets. By contract, a provider must not mutate the scene object
or represented item while describing the form.

The built-in object-settings controls migrate to built-in contributions.
Unsupported capabilities are omitted rather than inferred from renderer
attributes. For example, a graph contributes no face field, while mesh and
shape contributions may do so. The current private face-capability workaround
can then be removed.

## Consequences

- Packages can expose only the fields appropriate for a particular form and
  Viewer context without replacing scene-object classes.
- Stable scene objects remain free of Viewer-specific form metadata.
- Plugin discovery remains graphics-free and control construction stays
  consistent.
- The registry is intentionally a Viewer extension point, not a universal
  form or schema framework.
- Arbitrary widgets, nested layouts, conditional schema languages, and other
  form identifiers require demonstrated needs and separate approval.

## Compatibility

The first implementation replaces the hardcoded object-settings population
path without adding durable fields or changing scene serialization. The
existing general represented-item `ParameterForm` remains available. Explicit
item-parameter contributions may coexist with it; replacing the general dialog
is not part of this decision.

## Verification

- Compose general and specific contributions in the complete deterministic
  order defined above.
- Reject duplicate exact registrations and duplicate final field IDs.
- Verify a provider exception reports the complete registry context, aborts
  population, and leaves no partially rebuilt form.
- Verify Graph omits face controls while Mesh and Shape retain them.
- Verify providers are invoked only while the requested form is populated.
- Prove plugin discovery imports no graphics or UI modules.
- Verify built-in providers leave scene objects, represented items, and their
  serialized data unchanged while describing a form.
- Verify two contexts can contribute different fields for the same stable
  scene-object type.

## Dependencies

- Depends on Accepted ADR 013 for stable scene-object types.
- Respects ADR 014's restricted `draw`/`clear` operation surface and does not
  extend the core scene operation registry.
- Its implementation depends on Accepted ADR 016 for the declarative field and
  mutation contract; the Viewer ownership decision can be approved
  independently.

## Decision

Approved on 2026-11-08. Viewer owns one lightweight contextual form registry
whose providers return declarative field links rather than widgets. The
rationale is to make supported fields explicit and extensible while keeping
stable scene objects backend-neutral, plugin discovery graphics-free, and
control construction, lifecycle, ordering, and failure handling consistent in
Viewer.
