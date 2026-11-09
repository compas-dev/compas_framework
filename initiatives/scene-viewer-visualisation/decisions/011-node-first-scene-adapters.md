# ADR 011: Node-First Scene Construction and Adapter Lifetime

## Status

Superseded by ADRs 013–014 before acceptance.

## Context

ADR 008 correctly separates durable scene nodes from runtime adapters, but its
first implementation still constructs a detached `SceneObject` before creating
the node. The adapter temporarily owns the item reference, GUID, name,
transformation, appearance, and extension values. Binding then changes those
properties to read from the node.

This creates two object modes, duplicate storage, and identity whose meaning
changes after binding. Verified probes show that removal can expose stale
provisional values and a different GUID. Context rebinding replaces adapters
and leaves external references detached with the same stale fallback state.
The implementation therefore contradicts ADR 008's requirement that an
adapter constructor must not own serialized state.

## Options

1. Create the node first and construct a permanently node-bound runtime
   adapter from `(scene, node)`.
2. Retain detached and bound adapter modes while hiding the transition behind
   additional helpers.
3. Put runtime drawing behavior directly on `SceneNode`.
4. Preserve detached adapters through a compatibility wrapper.

## Recommendation

Choose option 1.

`SceneNode` remains the sole durable authority for identity, hierarchy, item
GUID, name, local transformation, appearance, visibility, and extension state.
`SceneObject` becomes a plain runtime adapter rather than a `Data` object. It
is constructed only from an existing scene and node and owns only context
handles, derived caches, drawing behavior, and invalidation.

Keep the convenient public call:

```python
sceneobject = scene.add(mesh, color=Color.red(), show=True)
```

Internally, `Scene.add` resolves the adapter type, validates node and extension
arguments, creates and attaches the node, records the item binding, and only
then creates `adapter_type(scene, node)`. Failure rolls back the node and item
binding atomically.

Deserialization remains node-only. `Scene.bind_context` constructs a complete
replacement adapter table after hierarchy and required items exist, then swaps
it in atomically. Adapter construction never creates hierarchy or durable
state.

Remove detached adapter construction, `Scene.add(sceneobject)`, adapter
serialization, adapter-owned temporary GUIDs and presentation fallbacks, and
constructor-driven child creation. Registry dispatch moves from
`SceneObject.__new__` to `Scene`.

Removed or context-replaced adapters become invalid runtime references. They
do not transition to a detached reusable mode. Re-adding content means adding
the `Data` item or retaining and explicitly rebinding an existing node.

## Compatibility

This intentionally breaks direct `SceneObject(item, ...)`,
`Scene.add(sceneobject)`, reusable removed adapters, and one-shot
`SceneObject(item).draw()`. Core and Viewer tests migrate to `Scene.add`.
GhPython one-shot conversion requires a small explicit context helper or local
scene. CAD-host adapters require audit before their later migration.

`Scene.add(data, ...)`, registry/context dispatch, durable node GUIDs,
reference-only serialization, unresolved loading, explicit item binding, and
shared item identity remain public behavior.

Direct `Group(...)` construction and arbitrary group constructor keywords as
future child defaults are removed. `scene.add_group(...)` creates the node
first; callers pass child presentation explicitly.

## Verification

- Prove the node exists before adapter construction.
- Prove adapter constructors receive only scene and node.
- Prove construction and context-binding failures roll back atomically.
- Prove GUID meaning and durable property storage never switch.
- Prove removed and replaced adapters fail precisely.
- Prove deserialization and unknown extension round trips need no adapters.
- Preserve Viewer round trips and `compas_model` compatibility through the
  public `Scene.add(data, ...)` path.

## Dependencies

- Supersedes the construction, adapter identity, and compatibility clauses of
  Accepted [ADR 008](008-scene-nodes-and-runtime-adapters.md).
- Preserves Accepted [ADR 010](010-scene-description-and-item-bundling.md).
- Works with Proposed [ADR 012](012-explicit-node-backed-adapter-state.md).

## Decision

Not accepted. Superseded on 2026-11-07 by Accepted ADRs 013–014.
