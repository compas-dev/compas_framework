# Scene, Viewer, and Visualisation Inventory

Inventory date: 2026-11-07.

## Audited checkpoints

| Repository | Branch | Exact head | State |
|---|---|---|---|
| `compas-dev/compas` | `remove-future` | `99b82a6673ff7d05c1c323c8921135c274993f11` | Clean |
| `compas-dev/compas_viewer` | `c3-upgrade` | `cf5a5195bda840a511319d6b7201978af68c15e3` | Clean |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | Clean |
| `compas-dev/compas_session` | `c3-upgrade` | `e0bdd02aa8490248c6f2f36042651d8ebfc4442b` | Clean |
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | Based on `e797d49f77ac32b65371497a21925a02b7d048d8` | Clean before initiative documents |

## Core scene infrastructure

`compas.scene.Scene` owns a serializable tree, item and scene-object stores,
context selection, hierarchy mutation, drawing traversal, and glTF conversion.
`SceneObject` combines serializable visual configuration with context-adapter
factory dispatch, local/world transformations, renderer identifiers, and
manual cache invalidation.

The global context registry maps item types to adapter classes and uses plugin
registration. Its lifecycle offers `clear`, `before_draw`, and `after_draw`,
but no renderer capability, event, change-notification, reverse-picking, or
incremental-update contract. Core has no common indexed render-buffer type.

Core tests cover context registration, hierarchy, transformations,
serialization, glTF conversion, and scene ownership. They do not cover
selection, interaction state, undo, incremental redraw, overlays, or batched
render data. The visualisation introduction is stale in its use of `data`, its
transformation explanation, and its assumptions about available adapters.

## Viewer architecture

`Viewer` coordinates the Qt application, `ViewerScene`, renderer,
`ViewerState`, commands, events, and UI as a singleton. `ViewerScene` fixes the
context to `"Viewer"`, maps picking colors, and directly coordinates renderer
and sidebar updates. `ViewerSceneObject` converts items into point, line,
front-face, and back-face channels and reaches the active viewer through that
singleton.

`BufferManager` efficiently batches ordinary objects into shared GPU-oriented
buffers and can update transforms without rebuilding topology. However,
`BufferGeometry` accepts expanded point, line-vertex, and triangle-vertex
arrays rather than shared vertices plus edge or triangle indices. Examples and
several adapters therefore duplicate vertices manually. `TessellationObject`
and `PolygonalSurfaceObject` already demonstrate indexed paths, but there is no
uniform public convenience layer.

Viewport and scene-tree multi-selection exist. Selection is stored as mutable
`is_selected` flags on scene objects and synchronized by imperative refresh
calls. There is no separate observable selection model, selection-change
event, complete rectangle-deselection path, or common programmatic mutation
contract.

Programmatic transforms and efficient transform-buffer updates exist, but
there is no object gizmo, transformation command, multi-object transform UI,
or defined undo contract. `Tag` and `ArrowOverlay` provide useful text and
arrow primitives, but the renderer special-cases their concrete classes. No
measurement, dimension, scale-bar, legend, or general overlay contract exists.

`ViewerState` provides observable dotted-path access to persistent
configuration. Selection, active tools, gestures, scene mutations, and command
execution live elsewhere. Commands and UI definitions offer useful extension
points, but there is no comparable public dock composition API and no console,
terminal, assistant, or safe execution boundary.

## Draft model integration evidence

`compas_model` owns backend-neutral model scene adapters, Viewer-specific
adapters, a `ModelViewer` controller, NumPy-based `RenderGeometry`, quality
settings, a revision-aware CPU cache, hierarchy projections, selection,
inspectors, and contact layers.

The draft treats `Model.tree` and rendered `Scene` hierarchy as separate.
remain separate. `ModelViewer` constructs and indexes the scene projection,
but reaches into concrete viewer sidebar and renderer APIs. Structural changes
are reconciled through explicit rebuilds rather than an observed projection
contract.

Draft model render geometry preserves separate indexed filled triangles and visible
line segments, but Viewer-specific adapters expand some arrays back to Python
lists. This makes buffer ownership and reusable conversion responsibilities
unclear. Package tests and documentation describe the current controller,
including multi-selection, visibility, caching, contacts, and offscreen viewer
integration. They establish implementation evidence, not public behavior that
this initiative must preserve.

## Adjacent packages

`compas_session` persists a generic core scene, data, settings, and undo/redo
history, but it is not a reactive viewer/UI state store. Notebook and CAD-host
packages consume core scene contracts under different runtime constraints.
They should be checked for compatibility with approved core changes, but
implementation migration would broaden the initial initiative materially.

## Framework evidence

Package-local core and Viewer tests provide substantial evidence. Draft model
tests provide additional coupling and regression evidence. The
framework repository currently has no installed cross-package scene/viewer
test. The plugin initiative separately requires a coordinated installed
model/viewer registry and lifecycle test; this initiative should coordinate
that gate rather than duplicate it.

Focused reconnaissance results:

- Core scene/plugin/glTF suite: 53 passed; one non-authoritative cache-write
  warning because the checkout cache directory was not writable.
- Viewer selection/state/tessellation/tag/overlay suite: 35 passed offscreen.
- Draft model integration behavior was inspected from its existing tests and
  build workflow; no new model tests were run and those tests are not treated
  as preservation requirements.

## Principal gaps and risks

1. Durable scene state, persistent configuration, and transient interaction
   state do not have explicit ownership boundaries.
2. Renderer identity has no common reverse mapping to scene objects or domain
   elements.
3. Scene mutations, selection, renderer updates, and UI refreshes use
   distributed imperative paths.
4. Raw indexed buffers lack a uniform public input and batching contract.
5. Overlay rendering is coupled to concrete Viewer classes.
6. The draft model controller demonstrates coupling to private or concrete
   Viewer structure, but its shape is not an architectural constraint.
7. Core appearance serialization and glTF export do not cover all visual
   settings consistently.
8. Per-object pickability conflicts with batching for large auxiliary data.
9. Singleton coupling makes state, commands, rendering, and scene behavior
   harder to test independently.
10. Scope can expand rapidly across notebook and host adapters unless initial
    and compatibility-only packages are explicit.

## Scene state and serialization follow-up

The current scene format is not ordinary `SceneObject` serialization. `Scene`
stores every domain item once by GUID and writes hierarchy nodes as an optional
item GUID, a free-form `settings` mapping, and children. Loading replays those
settings through `Scene.add`, which selects and constructs a runtime adapter
before the reconstructed hierarchy is complete. Multiple nodes can correctly
share one item, but node/adapter GUIDs are not preserved.

Two regressions were reproduced at the audited heads:

- a Viewer Box/ShapeObject translated by `[2, 0, 0]` reloads without its
  transformation because `ViewerSceneObject.settings` replaces the base
  mapping; `u=7`, `v=9`, and face color also reload as defaults;
- a `ModelViewer` scene fails to load because constructor replay uses
  `ModelObject(add_elements=True)` before attachment, causing its child
  creation to raise `RuntimeError: A detached scene object cannot own child
  objects.`

Unrestricted serialization introspection is unsafe. Concrete COMPAS objects
contain cycles, scene/item backreferences, GPU and picking identifiers, native
handles, lazy caches, derived NumPy buffers, and constructor commands. Public
properties can be computed or side-effecting, while persistent descriptor
values are often stored privately. Constructor signatures also lose inherited
state behind `**kwargs`.

Introspection remains useful when applied to a closed declared schema: it can
validate readable fields, constructor compatibility, and editor metadata. It
cannot safely determine persistence from `__dict__`, public names,
annotations, properties, or constructor parameters alone.

## Architecture questions

1. Does core own only scene hierarchy and transformations, or also neutral
   render primitives and change events?
2. Where do indexed buffers, picking identities, and reverse lookup live?
3. What observable state model unifies viewport, tree, and programmatic
   selection without making UI state serializable scene data?
4. What change categories allow transform-only, style-only, geometry, and
   hierarchy updates to remain efficient?
5. Which annotation and overlay objects are durable, transient, or both?
6. Which Viewer capabilities should be public because Viewer-owned tools and
   components require them, independently of a draft domain controller?
7. What is the smallest safe extension boundary for docks, consoles, and
   optional assistant integrations?
8. Which scene appearance semantics must serialization and glTF preserve?
