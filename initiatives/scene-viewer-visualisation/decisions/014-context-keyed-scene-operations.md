# ADR 014: Context-Keyed Scene Operation Plugins

## Status

Accepted.

## Context

Current visualization plugins register replacement `SceneObject` subclasses by
represented item type and context. `SceneObject.__new__` may therefore return a
Viewer, Rhino, Blender, Grasshopper, or Notebook subclass. This changes object
type based on installed plugins and mixes durable scene semantics with backend
runtime behavior.

The general COMPAS pluggable dispatcher identifies extension points globally
by domain, category, and function name. It does not select an implementation
from a call's explicit context or represented object type. Directly registering
multiple `draw` plugins would therefore conflict when several backends are
installed.

## Options

1. Register operation functions in a small scene-specific registry keyed by
   context, stable scene-object type, and operation.
2. Extend the general plugin manager with argument-aware dispatch.
3. Use one global backend plugin that switches internally on context and type.
4. Retain backend-specific replacement classes.

## Recommendation

Choose option 1.

Backend packages expose lightweight registration plugins that register
functions rather than classes:

```python
register_scene_operation(
    context="Viewer",
    sceneobject_type=MeshObject,
    operation="draw",
    implementation=draw_meshobject,
)
```

Lookup is deterministic by `(context, scene-object type MRO, operation)`.
Duplicate registrations for one exact key fail clearly. Heavy Qt, OpenGL,
Rhino, Blender, or other host imports remain inside operation bodies.

The initial public operation surface is only:

- `draw`;
- `clear`.

Backend-private buffer extraction, host-object creation, component drawing,
refresh strategies, and cache structures do not become speculative public
operations. Additional operations require demonstrated cross-backend need and
approval.

Conceptually:

```python
scene.draw(context="Viewer", runtime=viewer)
meshobject.draw(context="Viewer", runtime=viewer)
```

The selected implementation receives the owning scene, stable scene object,
and optional transient backend runtime. It may return opaque handles. Runtime
resources live in a nonserialized context store keyed by context and
scene-object GUID, never on the durable object.

There is no adapter-binding phase. Changing context selects different
operations and resources without replacing scene objects. Automatic context
selection is permitted only when exactly one compatible context is available.
Missing operations report context, scene-object type, and operation.

Keep the general COMPAS plugin manager unchanged. Its existing lightweight
`register_scene_objects` pattern may be renamed or replaced by
`register_scene_operations`, but discovery must remain graphics-free.

## Consequences

- Several visualization backends can coexist without class or plugin
  conflicts.
- Backend implementations become ordinary functions with explicit inputs.
- Stable scene-object classes remain backend-neutral.
- Runtime ownership is explicit and serialization-safe.
- Viewer requires a coordinated migration because its renderer currently
  consumes concrete `ViewerSceneObject` buffer APIs rather than only `draw`.
- CAD, notebook, robots, and domain backends require later coordinated
  migrations before they are admitted as compatible C3 candidates.

## Compatibility

Remove context-specific scene-object class registration,
`SceneObject(item, context=...)` factory substitution, `sceneobject_type=`,
`Scene.bind_context`, and direct one-shot `SceneObject(item).draw()`.

Preserve explicit context selection, automatic selection when unambiguous,
graphics-free plugin discovery, `scene.add(data, ...)`, and deterministic
resource clearing.

The initial coordinated implementation remains core, Viewer, and framework.
Other backends are recorded as incompatible until migrated; no compatibility
factory should retain type substitution.

## Verification

- Install Viewer and a fake second backend simultaneously and select each
  explicitly.
- Verify deterministic MRO fallback and duplicate-registration errors.
- Verify missing-operation diagnostics.
- Prove discovery imports no graphics modules.
- Prove context changes never replace or mutate durable scene objects.
- Prove draw/clear resource handling does not enter serialized state.
- Preserve indexed Viewer buffers, picking by stable scene-object GUID, and
  exact-candidate framework integration.

## Dependencies

- Depends on Proposed [ADR 013](013-hierarchy-nodes-and-stable-sceneobjects.md).
- Replaces context-specific class registration if approved.
- Leaves the general plugin dispatcher unchanged.

## Decision

Accepted on 2026-11-07. The user approved context-keyed operation functions,
the initial `draw`/`clear` surface, backend-neutral durable state, and
coordinated later migration of visualization hosts.
