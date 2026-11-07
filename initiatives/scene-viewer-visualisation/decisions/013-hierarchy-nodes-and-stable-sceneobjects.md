# ADR 013: Hierarchy-Only Nodes and Stable Scene Objects

## Status

Proposed.

## Context

Accepted ADR 008 separated durable scene nodes from runtime adapters, but the
implementation duplicated state across detached and bound adapter modes.
Proposed ADR 011 removes that dual lifecycle, but still makes `SceneNode` own
both hierarchy and all durable visual state while `SceneObject` is only a
runtime projection. This leaves two public concepts that appear to describe
the same scene entry and makes backend-specific replacement classes central to
ordinary object access.

A simpler separation is possible: nodes describe only hierarchy; stable scene
objects describe everything durable about a visualized item; backends provide
operations rather than replacement object classes.

## Options

1. Use hierarchy-only nodes and durable, stable scene objects.
2. Keep durable state on nodes and make scene objects always-bound adapters as
   proposed by ADRs 011–012.
3. Merge hierarchy and durable state back into one tree-node class.
4. Keep the implemented detached/bound adapter model.

## Recommendation

Choose option 1.

`SceneObject` is a backend-neutral `Data` object with a stable Python type and
GUID. It owns:

- the referenced item GUID, if any;
- name and local transformation;
- visibility, opacity, and durable backend-neutral appearance; and
- stable semantic type-specific state.

Stable subclasses such as `GroupObject`, `GeometryObject`, `ShapeObject`,
`MeshObject`, `GraphObject`, and `VolMeshObject` express durable semantics.
Installing Viewer, Rhino, Blender, or another backend never changes an
object's class.

`SceneNode` owns only ordered parent/child relationships and a reference to one
scene-object GUID. Enforce exactly one node per scene object in one scene.
Instancing is not included. Multiple appearances of one data item use multiple
scene objects referencing the same item GUID.

Do not serialize a second durable node GUID. The scene-object GUID is the
hierarchy key. The root is an ordinary `GroupObject` with a corresponding root
node rather than a special identity model.

`Scene` owns separate object and hierarchy stores. `scene.add(item, **state)`
creates the stable semantic scene object, attaches its hierarchy node, and
returns the object. `scene.add_object(sceneobject, parent=...)` explicitly
attaches an existing durable scene object; `Scene.add` is not overloaded with
runtime adapters.

Scene serialization contains a version, name, stable scene-object records,
and a hierarchy of scene-object GUID references. Referenced `Data` items remain
external under ADR 010. Loading requires no visualization backend and leaves
item references unresolved until explicitly bound.

Durable type-specific state follows ADR 009's useful rule: a closed base schema
plus explicit fields. State lives as ordinary `SceneObject` attributes, not in
node extensions and not behind attribute interception. Unknown namespaced
state may be retained solely for lossless forward round trips. Backend plugins
may not add durable fields.

Selection, picking, UI state, renderer configuration, generated buffers,
handles, and caches remain runtime/application state outside `SceneObject`.

## Consequences

- Nodes, scene objects, represented data, and backend operations have distinct
  and explainable roles.
- Scene-object type and GUID remain stable through attachment, removal,
  serialization, and context changes.
- A durable scene object may exist detached without acquiring a second storage
  mode; attachment adds only a nonserialized scene backreference.
- Removing and explicitly reattaching an object never reveals stale fallback
  values or changes identity.
- The scene schema changes from nested stateful nodes to object records plus a
  hierarchy of references.
- Backend-specific replacement classes are removed under ADR 014.

## Compatibility

Preserve `scene.add(data, ...)`, shared item identity, unresolved scene loading,
explicit item binding, stable object GUIDs, and hierarchy operations through
returned scene objects.

Remove backend adapter serialization, constructor-driven child creation, and
implicit group child defaults. `GroupObject` is durable and backend-neutral.
`compas_model`'s maintained controller path already uses `scene.add`; its custom
scene-object redesign remains a later phase.

## Verification

- Prove nodes serialize only hierarchy references.
- Prove one node per scene object and reject accidental instancing.
- Preserve scene-object GUIDs through add, move, remove, reattach, reload, and
  visualization-context changes.
- Prove durable state has one storage location.
- Load, inspect, edit, and serialize a scene without backend plugins.
- Bind independently loaded items with shared identity.
- Round-trip multiple scene objects referencing one item.
- Exclude selection, handles, buffers, caches, and context from serialization.

## Dependencies

- Intended to supersede Accepted ADR 008 and ADR 009's placement of extension
  state if approved.
- Retains ADR 009's closed-schema principle.
- Preserves Accepted ADR 010, with item references moving from nodes to scene
  objects.
- Works with Proposed [ADR 014](014-context-keyed-scene-operations.md).

## Decision

Pending explicit user approval.
