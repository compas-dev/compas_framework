# Scene, Viewer, and Visualisation Proposal

## Summary

Keep `compas.scene` responsible for durable, backend-neutral scene content and
hierarchy. Put indexed render buffers, picking, selection, transient state,
tools, overlays, GPU synchronization, and UI composition in `compas_viewer`.
Expose only the public operations required by Viewer-owned tools and UI
components. Future integrations may consume that boundary after it is proven.

The first implementation wave should establish these boundaries and deliver
object selection, efficient indexed geometry, multi-object transforms,
measurements, annotations, scale/legend overlays, and public dock/command
composition. It should not attempt a universal renderer API, a generic reactive
framework, sub-object editing, a shell, or host-application migration.

ADRs 001–010 are Accepted. Implementation may proceed in dependency order
within the approved initial scope; Session redesign and Viewer/Session
convenience operations remain later work.

## New evidence requiring amendment

- A Viewer Box/ShapeObject local translation `[2, 0, 0]` reloads as
  `transformation is None` because `ViewerSceneObject.settings` replaces core
  settings. A headless ShapeObject with `u=7`, `v=9`, and a face color reloads
  with resolution defaults `16`, `16`, and the default face color.
- A ModelViewer scene fails while loading. Runtime factory dispatch constructs
  `ModelObject` with its default `add_elements=True`; it calls `self.add`
  before attachment and raises `RuntimeError: A detached scene object cannot
  own child objects.` The original controller deliberately used
  `add_elements=False` and `add_children=False`. Render settings and caches are
  absent too, but caches are transient and should stay out of scene files.
- Shared item identity survives through the item GUID store. Scene-object GUIDs
  do not survive, so they cannot yet serve as the durable identity assumed by
  ADR 001.

## Recommended architecture

### Durable scene content and runtime adapters

Core `Scene` remains the backend-neutral serializable hierarchy, but its
durable entries become scene-owned node/state value objects rather than runtime
`SceneObject` adapters. Nodes preserve their own GUID, optional item GUID,
local transformation, hierarchy, visibility, base appearance, and explicitly
declared extension state. Runtime item bindings preserve shared identity
without making Scene the owner or serialization container of those items.

Runtime `SceneObject` instances bind a complete node and item to a chosen
visualization context. They are not serialized identities and may be created
only after deserialization has rebuilt the hierarchy and resolved the required
item bindings.
Their constructors do not populate hierarchy. Scene context is runtime binding
configuration; absence of a backend cannot prevent loading durable content.

Durable node GUIDs are the stable boundary between scene content and Viewer
state. Renderer pick IDs remain short-lived Viewer mappings and are never
serialized. Unknown namespaced adapter state remains inactive but round-trips
without importing that adapter.

Base node state uses a closed core schema. Additional durable fields use
explicit MRO-composed declarations. Introspection may validate declarations
and support editors, but `__dict__`, public properties, annotations, and
constructor parameters never define persistence automatically.

### Scene descriptions, item bindings, and aggregation

Durable scene nodes reference items by stable item GUID. Serialized `Scene`
contains the visual node hierarchy and state but does not require referenced
`Data` objects to live inside it. At runtime Scene binds already loaded objects
to those GUIDs without taking exclusive ownership; the same object remains
independently serializable and directly usable by algorithms.

A separately loaded description may contain unresolved references. Its
hierarchy and node state remain inspectable, and callers can bind items later.
All nodes sharing one GUID resolve to the same bound instance. Item-dependent
adapter, draw, and packaging operations fail precisely when the required GUID
is unresolved.

A redesigned `compas_session.Session` is the likely optional aggregate for
independently serialized data, one or more scene descriptions, settings,
history, and their shared identity. Its design and implementation require a
separate dependent decision and scope approval; this initiative does not add a
redundant one-scene `SceneBundle`. Scene remains usable without Session.

Do not add URI resolution, filesystem search, network loading, or an asset
registry without a concrete future requirement.

### Indexed render geometry

`compas_viewer` owns one public indexed `BufferGeometry` contract:

```python
geometry = BufferGeometry(
    vertices=vertices,
    points=point_indices,
    edges=edge_indices,
    triangles=triangle_indices,
)
```

Vertices accept the approved structural numerical input, including Python
sequences and NumPy arrays. Index channels are optional and retain their
connectivity. Convenience constructors cover the common direct cases:

```python
BufferGeometry.from_points(vertices)
BufferGeometry.from_vertices_and_edges(vertices, edges)
BufferGeometry.from_vertices_and_triangles(vertices, triangles)
```

Construction normalizes each supplied channel once to the Viewer's required
NumPy dtype and validates only rank, column count, and index bounds. It does
not create `Mesh`, `PolygonalSurface`, `Tessellation`, or one object per
primitive. Styling stays on the scene object; a separate color-buffer decision
is required only when current uniform/per-item styling proves insufficient.

Existing Viewer adapters should return indexed channels to the buffer manager
instead of expanding geometry. Geometry producers continue to use their approved
`to_tessellation` and `to_polygonal_surface` APIs; this Viewer contract does
not become a geometry-algorithm input.

### Viewer state and selection

Separate three state classes:

| State | Owner | Persistence |
|---|---|---|
| Scene items, hierarchy, local transformations, durable appearance | `compas.scene` | Scene serialization |
| Viewer defaults, appearance, key bindings, layout preferences | `Viewer.config` | Viewer configuration |
| Selection, hover, active tool, gestures, and transient tool results | `Viewer.state` | Session-only |

`Viewer.state.selection` is the one object-selection model. It stores ordered
scene-object GUIDs and exposes replace, add, remove, toggle, clear, and query
operations plus one change notification. Viewport picking, rectangle
selection, the scene tree, commands, and programmatic consumers all mutate
this model.
The current mutable and serialized `ViewerSceneObject.is_selected` path is
removed rather than retained as a second authority.

Initial selection is object-level. The architecture reserves no generic
component-token schema; vertex, edge, face, or domain-element selection should
be proposed when a concrete editing workflow requires it.

The state implementation should be a small Python model with a Qt bridge, not
a generic observable dictionary or third-party reactive framework. The
renderer reads selection state when updating its per-object settings buffer.

### Transformations and undo

Core transformations remain authoritative. Viewer exposes one public
multi-object transformation operation and uses it from code, commands, and a
future gizmo:

```python
viewer.transform_objects(objects, transformation, space="world")
```

The initial operation applies one world-space delta to every selected object's
pre-operation world transformation. For each object, Viewer derives the new
local transformation from its parent world transformation. Ancestor/descendant
pairs in one request are rejected initially because applying the same delta to
both is ambiguous. Invalid targets leave all objects unchanged.

Every successful call is one transaction containing the before and after local
transformations. A small Viewer undo stack handles these explicit reversible
transactions. Existing callback commands remain valid; only mutating commands
that implement the reversible transaction contract enter history. This does
not move general application/session history into Viewer or `compas_session`.

Viewer retains explicit refresh operations for geometry, appearance,
transform, and hierarchy changes. The initial wave does not add a generic core
scene event bus: direct external mutation still requires the corresponding
public Viewer refresh call. This keeps synchronization costs explicit and
avoids making all core scene properties observable.

### Annotations and overlays

Use two explicit paths:

- World-anchored annotations are serializable scene items with Viewer scene
  adapters. The initial types are text annotation and distance dimension. A
  distance dimension stores its two world anchors, display unit/precision, and
  optional label override; its measured value is derived, not duplicated.
- Screen-space overlays are transient Viewer UI objects. The initial types are
  scale indicator and legend. They are not scene items and do not participate
  in scene serialization or picking unless a later requirement says so.

Existing `Tag` and `ArrowOverlay` should be aligned with these two paths rather
than leaving concrete-class checks in the renderer. Do not introduce a
framework-wide overlay registry. One Viewer-owned world-annotation adapter
path and one Viewer overlay layer are sufficient for the approved types.

The measurement tool owns temporary pointer/preview state in `Viewer.state`.
Completing a measurement creates a durable distance-dimension scene item;
cancelling it leaves no scene mutation.

### Public Viewer operations

Expose the small set of operations that Viewer-owned commands, tools, and UI
components need without coupling them to renderer or widget internals:

- `viewer.scene` for durable content;
- `viewer.state.selection` for selection;
- `viewer.refresh_geometry`, `refresh_appearance`, `refresh_transform`, and
  `refresh_hierarchy` for explicit synchronization;
- `viewer.transform_objects` and undo/redo;
- public command registration and menu placement;
- public dock addition/removal using Viewer component/widget content; and
- public annotation and overlay addition.

These operations are justified and tested inside Viewer. They are not designed
around the current draft `compas_model.ModelViewer`. That controller may be
redesigned freely in a later consumer phase, at which point it can use the
small proven Viewer boundary or motivate a separately approved addition.

A console, terminal, or assistant can later occupy a public dock and invoke
registered commands, but arbitrary code execution, shell access, credentials,
remote transports, and assistant policy are explicitly outside this wave and
require a security decision.

## Alternatives and tradeoffs

### Put render buffers in core

Rejected for the initial wave. Core would gain renderer-oriented dtype,
channel, and update assumptions while notebook and host backends have not
demonstrated a shared contract. Structural geometry inputs and `Tessellation`
already cover neutral transfer needs; GPU-ready batching belongs to Viewer.

### Use scene-object flags as selection state

Rejected. It makes transient interaction state serializable, requires every UI
to poll/mutate objects, and leaves viewport, tree, domain controller, and
renderer synchronization distributed.

### Add a universal reactive store and scene event bus

Rejected for the initial wave. It adds a second application framework and
forces observability into core without established semantics for arbitrary
item mutation. Explicit state models and refresh categories satisfy current
requirements more transparently.

### Make all annotations screen overlays

Rejected. Measurements and world labels need world anchors, scene hierarchy,
transformations, and persistence. Conversely, scale indicators and legends are
view-dependent and should not become durable geometry.

### Standardize every visualisation backend now

Rejected. Notebook and CAD hosts are important compatibility consumers, but
their runtime and rendering models differ. The first wave should avoid breaking
their core scene contracts and record follow-up work only after the Viewer
design is proven.

## Compatibility implications

- Removing `ViewerSceneObject.is_selected` is a deliberate Viewer API break.
  Commands, tree widgets, shaders, and tests migrate in one coordinated change;
  no writable compatibility alias remains.
- `BufferGeometry` construction changes from expanded channel vertices to
  shared indexed vertices. Current examples and adapters migrate together.
  A deprecated parallel constructor is not proposed.
- Existing core scene serialization is not sufficient for the approved
  architecture. ADRs 008–009 define a new explicit node schema without a
  compatibility loader for existing scene files. ADR 010 separates
  reference-only descriptions from a possible future Session aggregate;
  implementation is blocked pending its approval.
- Current `Tag` and `ArrowOverlay` data may require a documented migration to
  the accepted annotation/overlay types. Exact compatibility should be checked
  against serialized fixtures before implementation; do not silently reinterpret
  ambiguous old data.
- The current draft `compas_model.ModelViewer` behavior, hierarchy projections,
  selection behavior, controller shape, and cache arrangement are not
  compatibility requirements. Its failure remains evidence for the scene
  reconstruction problem, and its redesign is deferred.
- Viewer plugin discovery remains graphics-free and function-local under the
  accepted plugin ADRs.

## Affected packages

| Package | Responsibility |
|---|---|
| `compas` | Preserve scene identity, hierarchy, transformations, durable appearance, and serialization; clarify stale documentation. |
| `compas_viewer` | Implement indexed buffers, state/selection, transforms/history, annotations, overlays, facade, rendering, and UI. |
| `compas_model` | Later redesign consumer and regression evidence; no current draft controller behavior is preserved by this wave. |
| `compas_framework` | Pin exact candidates and verify installed cross-package scene, plugin, selection, transform, and buffer behavior. |

`compas_session`, `compas_notebook`, Rhino, Grasshopper, and Blender are
compatibility-reviewed but not implementation targets in the initial wave.

## Tests and examples

### Core

- Preserve scene serialization, shared-item identity, hierarchy, and local/
  world transformation tests.
- Add the verified Viewer transformation/ShapeObject settings regression.
  Preserve the ModelViewer detached-child failure as evidence and cover its
  core failure mode with a minimal adapter whose constructor must not run
  during hierarchy deserialization; the draft controller itself is deferred.
- Preserve durable node GUIDs separately from shared item GUIDs and round-trip
  unknown namespaced extension state without its runtime adapter.
- Load independently serialized items, bind them to reference-only scene
  descriptions, preserve shared identity, and verify unresolved-reference
  behavior without Session.
- Add regression coverage proving transient Viewer state is absent from core
  scene data and serialization.
- Correct and test the core scene/visualisation guide against current APIs.

### Viewer

- Accept list and NumPy vertices/indices; verify shapes, bounds, dtypes,
  non-mutation, and retained indices.
- Compare large indexed edge/triangle input with expected buffer counts and
  assert it does not create one scene object per primitive.
- Exercise selection replacement/add/remove/toggle from viewport, tree, and
  code through the same observable model.
- Verify renderer picking IDs resolve to scene GUIDs and are not serialized.
- Test world-space multi-object transforms, parent conversion, atomic failure,
  undo/redo, and ancestor/descendant rejection.
- Test distance derivation, unit/precision formatting, tool cancel/complete,
  annotation serialization, and transient overlay non-serialization.
- Test public dock/command composition without importing optional integrations
  during plugin discovery.

### Framework and later consumers

- Use the current draft ModelViewer load failure as regression evidence for
  two-phase scene reconstruction, not as a public behavior suite.
- Add an installed exact-candidate test for core Scene and Viewer contracts.
- Redesign and verify model integration only in a later approved consumer phase.
- Keep candidate-artifact evidence separate from source-build integration.

Examples remain direct scripts and demonstrate, in order:

1. vertices and edges;
2. vertices and triangles;
3. shared indexed geometry with selection;
4. multi-object transformation and undo;
5. distance measurement and world annotation; and
6. scale/legend overlays and a custom dock.

## Dependency order

```text
ADR 001 --> ADR 008 --> ADR 009 --> ADR 010
    |
    +--------> ADR 002
    +--------> ADR 003 --> ADR 004

ADRs 001–003 ----------> ADR 005
ADRs 001, 003–005 -----> ADR 006
ADRs 001–010 ----------> ADR 007 rollout gate
```

Core geometry, typing, plugin, and repository-modernisation decisions remain
upstream constraints. Implementation starts only after all ADRs required for a
wave are Accepted.

## Decision record

1. [ADR 001 — Ownership and state boundaries](decisions/001-ownership-boundaries.md)
2. [ADR 002 — Indexed Viewer buffer geometry](decisions/002-indexed-buffer-geometry.md)
3. [ADR 003 — Viewer state and object selection](decisions/003-viewer-state-and-selection.md)
4. [ADR 004 — Transformations, refresh, and undo](decisions/004-transform-refresh-undo.md)
5. [ADR 005 — Annotations, measurements, and overlays](decisions/005-annotations-and-overlays.md)
6. [ADR 006 — Public Viewer integration facade](decisions/006-viewer-integration-facade.md)
7. [ADR 007 — Initial scope and verification](decisions/007-scope-and-verification.md)
8. [ADR 008 — Serializable scene nodes and runtime adapters](decisions/008-scene-nodes-and-runtime-adapters.md)
9. [ADR 009 — Explicit scene-state serialization fields](decisions/009-scene-state-fields.md)
10. [ADR 010 — Scene description, item bindings, and aggregation boundary](decisions/010-scene-description-and-item-bundling.md)

ADRs 001–010 are Accepted.
