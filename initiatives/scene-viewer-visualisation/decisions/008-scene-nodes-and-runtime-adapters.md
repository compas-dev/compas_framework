# ADR 008: Serializable Scene Nodes and Runtime Adapters

## Status

Proposed.

## Context

ADR 001 correctly separates durable scene content from Viewer interaction and
renderer state, but it still treats `SceneObject` as both durable node and
context-specific runtime adapter. Current serialization stores an item's GUID
plus `sceneobject.settings`, then calls `Scene.add(..., **settings)` during
load. Factory dispatch chooses a runtime subclass and executes its constructor
before that object is attached to the reconstructed hierarchy.

Two verified regressions expose the consequences:

1. A Viewer Box/ShapeObject with local translation `[2, 0, 0]` reloads with
   `transformation is None` because `ViewerSceneObject.settings` replaces
   rather than extends core settings. In a headless ShapeObject case, `u=7`,
   `v=9`, and a face color reload as the defaults `16`, `16`, and the default
   face color.
2. A `ModelViewer` scene cannot reload. The controller originally creates
   `ModelObject(add_elements=False)` and `ElementObject(add_children=False)`,
   but those construction controls are absent from serialized settings.
   Reload dispatches `ModelObject` with `add_elements=True`; its constructor
   calls `self.add(...)` before attachment and raises `RuntimeError: A detached
   scene object cannot own child objects.` Render caches are transient and
   should not be serialized, but hierarchy reconstruction must not depend on
   them or on constructor side effects.

The shared item store already preserves identity when multiple nodes reference
one item GUID. Scene-object/node GUIDs are not preserved across round trips.
Context also determines which runtime subclass is constructed, even though a
serialized scene should remain loadable without that backend.

## Options

1. Separate a serializable scene-owned node/state value from context-specific
   runtime adapters and reconstruct them in two phases.
2. Keep `SceneObject` as both node and adapter and expand every subclass's
   `settings` property until current tests pass.
3. Serialize complete runtime adapter objects, including their concrete class
   and context.
4. Serialize only items and hierarchy and discard all per-node appearance and
   transformations.

## Recommendation

Choose option 1.

`Scene` owns a serializable node/state record for every hierarchy entry. The
closed base record contains:

- a durable node GUID;
- node kind (`item` or `group`);
- optional item GUID;
- name;
- local transformation;
- visibility, opacity, and base appearance; and
- explicitly declared extension state governed by ADR 009.

The item store remains separate and keyed by item GUID, preserving shared item
identity. Node GUIDs are serialized and restored so selection references,
domain indexes, and external scene references have durable identity. Runtime
adapter instances are not durable identities.

Deserialize in two phases:

1. validate and create the item store, nodes, state, GUIDs, and complete
   hierarchy without context dispatch or adapter constructors;
2. bind adapters for an explicitly requested or detected runtime context only
   after the scene is structurally complete, either eagerly for drawing or
   lazily on first use.

`SceneObject` becomes the runtime adapter bound to a scene, node, and optional
item. Its constructor must not populate hierarchy or own serialized state.
Domain projection such as `ModelViewer` creates nodes explicitly through a
controller; adapter binding never recreates children.

Scene context is runtime binding configuration, not authoritative serialized
content. A scene may record a non-binding context hint for user experience,
but loading must not require that context or silently select a different one.
Drawing without a usable context raises a precise runtime error after the
backend-neutral scene has loaded.

Known extension fields are activated only by a compatible adapter. Unknown
extension namespaces and fields are preserved losslessly as inactive node
state and written back unchanged. Unknown required base schema versions fail
validation; unknown adapter state is not passed blindly to constructors.

## Refinement of ADR 001

This ADR preserves ADR 001's package boundaries but refines these clauses:

- "Core owns scene items, hierarchy, scene-object GUIDs..." becomes: core
  owns items plus durable node/state GUIDs; runtime adapter identity is not
  serialized.
- "GUIDs connect durable scene objects to Viewer state" becomes: durable node
  GUIDs connect scene content to Viewer state and domain indexes.
- Core still owns transformations, visibility, durable appearance, and
  serialization, but those values live on node state rather than being
  discovered from a runtime adapter's constructor/settings implementation.

Implementation of ADR 001's durable identity and serialization boundary is
blocked until this amendment and ADR 009 are approved.

## Consequences

- Scenes load without Viewer, model adapters, or another visualization backend.
- Runtime constructors no longer execute hierarchy-building side effects during
  deserialization.
- Switching or omitting runtime contexts does not destroy durable node state.
- Shared item identity and durable node identity have separate, explicit GUIDs.
- Core Scene/SceneObject APIs require a coordinated redesign and compatibility
  review; this is larger than patching two `settings` properties.
- Adapter binding and lifecycle need focused tests, but no universal renderer
  abstraction or event bus is introduced.

## Compatibility

The existing serialized scene shape requires an explicit one-way loader into
the new node schema. Old files have no durable node GUID, so the loader
generates one deterministically only where the legacy hierarchy supplies a
stable path; otherwise it generates and documents a new identity. It preserves
known legacy settings and rejects ambiguous state rather than guessing.

Existing public code may continue to receive a `SceneObject` adapter from
`Scene.add`, but code that treats adapter identity or constructor side effects
as durable must migrate. Exact compatibility is part of the Phase 1 audit.

## Verification

- Reproduce both verified regressions as tests before implementation.
- Round-trip local transformations, `u=7`, `v=9`, face color, shared items,
  node GUIDs, groups, and hierarchy without a visualization backend installed.
- Load the model scene without calling adapter hierarchy constructors, then
  bind Viewer adapters after the hierarchy is complete.
- Load and re-save unknown extension state without loss or constructor use.
- Verify missing/unknown context permits load but produces a precise binding or
  draw error.
- Verify duplicate item or node GUIDs and unsupported base schema versions fail
  atomically.

## Affected packages

`compas`, `compas_viewer`, `compas_model`, and `compas_framework`.

Compatibility review only: `compas_session`, `compas_notebook`, and CAD-host
scene adapters.

## Dependencies

- [ADR 001](001-ownership-boundaries.md), refined by this decision

ADR 009 supplies the serialization field policy required to implement this
decision. The two Proposed amendments must be approved together, but ADR 008
defines the ownership boundary first.
