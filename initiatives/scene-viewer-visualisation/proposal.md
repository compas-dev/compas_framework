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

ADRs 013–014 are Accepted, implemented, and verified. Session redesign and
Viewer/Session convenience operations remain later work.

ADRs 015–016 authorize one normalized editable-attribute mapping composed from
editable `SceneStateField` entries, narrowly declared non-state attributes,
and runtime-only contextual overrides. The earlier `FormField` implementation
was replaced; the amended core and Viewer implementation is independently
approved and green in package and exact-candidate integration CI.

ADRs 017–020 authorize lazy datastructure element-attribute tables and editing,
configured Viewer identity, and an explicit configuration lifecycle/field
audit. Their implementation is verified locally and in hosted Viewer and
framework CI. ADR 003 object selection is also fully verified. ADR 004
transformations, categorized refresh, and Viewer-level transform history is
implemented, independently approved, and verified locally and in hosted core,
Viewer, and framework CI.

ADRs 029 and 031 are implemented and verified locally and in hosted package
and exact source-installed integration CI. Direct use then exposed a sidebar
composition problem: one stacked splitter presents spatial, annotation, and
system contexts simultaneously, redistributes unrelated panels, and hides
annotation naming and global deselection behavior. Accepted ADR 032 responds
with three stable top-level domains while preserving separate spatial and
annotation selection models. Its implementation and local verification pass;
hosted package and exact source-installed integration verification also pass.

## Proposed three-domain sidebar amendment

Replace the shared vertical splitter with one full-height tab widget containing
Scene, Annotations, and System. Scene owns the hierarchy and selected spatial
object details. Annotations owns the ordered annotation list and an explicit
selected-annotation detail form. System owns Camera, Display, and Units and
Measurement sections. Ordinary layouts provide stable master/detail space;
selection updates must not resize or rebuild unrelated domains.

Spatial and annotation selections remain independent and can coexist. Tab
changes preserve both. Spatial picking changes only spatial selection and the
annotation list changes only annotation selection. An unmodified empty
viewport click clears both. Escape cancels an active measurement first and
otherwise clears both, while focused editors retain their local Escape
behavior. Annotation and spatial deletion remain separate operations.

The annotation detail form makes Name editing explicit and presents Type and
the supported narrow dimension style without embedding those controls in the
list. Commands navigate with `sidebar.set_current_tab`, accepting only Scene,
Annotations, or System, and `sidebar.focus_system_section`, accepting only
Camera, Display, or Units and Measurement. Unsupported identifiers raise
`ValueError`; focusing a system section first activates System. The optional
datastructure inspector remains absent by default and routes to Scene when
explicitly configured. The existing Viewer configuration schema, Core Scene
schema, and optional sidebar component types remain unchanged.

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
  reference-only descriptions from a possible future Session aggregate; its
  accepted replacement is implemented and verified.
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

## Architecture correction after Phase 1

Implementation evidence invalidates the detached/bound adapter mechanism used
for the first implementation of ADRs 008–009. It duplicates provisional and
node state, changes GUID meaning at binding, and requires hidden attribute
interception. Removal and context replacement can expose stale values on old
adapter references. Backend class substitution adds another ambiguity: the
type returned for one scene entry depends on which visualization plugins are
installed and selected.

The preferred correction assigns one purpose to each concept:

- `SceneNode` stores only ordered hierarchy through a scene-object GUID;
- stable backend-neutral `SceneObject` values own item references, identity,
  transformation, appearance, visibility, and semantic type-specific state;
- independently serialized `Data` items remain external and bind by GUID; and
- visualization backends register context-keyed `draw` and `clear` functions
  rather than replacement scene-object classes.

`scene.add(data, ...)` remains the primary convenience path and returns the
stable scene object. One node is allowed per scene object; repeated appearances
of one item use multiple scene objects. The scene-object GUID is the hierarchy
key, so there is no second durable node identity. A scene serializes stable
object records plus a hierarchy of GUID references and loads without any
backend installed.

The general COMPAS plugin dispatcher cannot select a `draw` implementation
from an invocation's explicit visualization context. The preferred design does
not complicate it. Lightweight discovery plugins populate a small scene
operation registry keyed by `(context, scene-object type, operation)`. Runtime
buffers, host handles, picking state, and caches live outside durable objects.

ADRs 011–012 record the unaccepted first node-first alternative. Accepted ADRs
013–014 record the selected design, which is now implemented and verified.

## Accepted editable scene-object declarations

Durable semantic fields use their existing `SceneStateField` as the single
source of persistence and editability. That field gains only `editable=False`
and an optional synchronous atomic data-side `update(owner, value) -> None`
callback; providing `update` while not editable is invalid. Ordinary mutation
uses `setattr`.

`SceneObject.__editable_attributes__` is reserved for genuinely editable
non-state attributes, initially `name` and `opacity`. Its values are only
optional update callbacks. `SceneObject.editable_attributes()` composes both
sources base-to-derived into one ordered `name -> optional callback` mapping
without duplicating subclass state-field names. Core contains no labels,
editors, arbitrary data, form identifiers, refresh categories, or context
metadata. Viewer infers presentation and does not maintain a parallel built-in
field list or expose public `FormField` values.

Graphics-free context plugins may extend, replace, or remove entries through
the same mapping. They compose general-to-specific by stable scene-object MRO.
Their key is `(context, stable SceneObject type, contribution ID)`. Within each
MRO specificity, contributions apply by lexical contribution ID while
preserving mapping insertion order. Duplicate exact registrations and
same-specificity edits or removals of one attribute are errors rather than
load-order overrides. Contributions and resolved mappings are runtime-only and
never serialized.

After a successful mutation, Viewer exclusively decides whether to rebuild
render data, redraw, and refresh UI. Context plugins only modify neutral
editable-attribute declarations. Core contains no refresh callback, refresh
category, or context protocol. Failed mutation restores the control and
triggers no view refresh.

The initial scope is only stable scene-object attributes in object settings.
Represented-item parameters remain on the existing `ParameterForm` path. The
amended ADRs explicitly supersede the earlier public `FormField`, item-target,
and field-level refresh design and the first uncommitted separate
`EditableAttribute` declaration design. The replacement is implemented and
verified.

## Accepted datastructure element-attribute tables

Viewer may add lazy `QAbstractTableModel` views for Mesh and Graph element
attributes without changing core. Domains and columns come from existing
`default_*_attributes` mappings and matching singular APIs. Default mapping
insertion order defines columns; sparse undeclared attributes are not scanned
or shown. Tabs exist only for domains with declared attributes.

The accepted editing contract supports Boolean, integer, float, and text
defaults. Other types are read-only. Cells show effective values, mutate
through singular setters, and reset through singular unset operations. Table
selection remains local, and Viewer refreshes conservatively after successful
mutation. Default-schema editing, sparse-column discovery, batch editing,
undo, and viewport component selection remain outside the first version.

## Accepted Viewer identity and configuration lifecycle

The existing `WindowConfig.title` should consistently supply Qt application
name, display name, and window title. `icon=None` selects the packaged icon;
otherwise the icon is an absolute path. Identity and window behavior are
startup-only, fullscreen is honored, and configuration is applied before Qt
application construction. This identity decision is independent of schema
migration and unrelated field cleanup.

Viewer should retain nested dataclasses and gain explicit path-aware
validation rather than Pydantic, arbitrary plugin dictionaries, or a reactive
configuration promise. Schema version 2 connects fullscreen and status-bar
visibility; removes `about`, obsolete sidebar fields, renderer `opacity`, and
the duplicated `display` group; removes root `unit` until a unit-aware workflow
has an approved owner and lifecycle; adds `ortho` to renderer view choices; and
keeps active `vectorsize`. Schema-1 migration drops known retired fields,
preserves retained values, and rejects unknown fields; schema 2 rejects
explicit retired fields. Typed Viewer subclasses may add typed dataclass
configuration fields with their own validation. Direct mutation is setup-time
only, replacing `viewer.config` is unsupported, and dotted-path `ViewerState`
access is transitional rather than an extension API.

## Architectural watchpoint

The user has reserved judgment on whether the overall relationship between
`Data`, durable scene state, and extension mechanisms is the final model. The
current Accepted ADRs remain authoritative and implementation should proceed
as specified. If implementation evidence exposes duplicated ownership,
non-transparent extension paths, forced representation changes, or another
concrete mismatch, bring that evidence back for an explicit amendment or new
decision. Do not preemptively reopen the accepted architecture or add a
speculative replacement model.

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
11. [ADR 011 — Node-first scene construction and adapter lifetime](decisions/011-node-first-scene-adapters.md)
12. [ADR 012 — Explicit node-backed adapter state](decisions/012-explicit-node-backed-adapter-state.md)
13. [ADR 013 — Hierarchy-only nodes and stable scene objects](decisions/013-hierarchy-nodes-and-stable-sceneobjects.md)
14. [ADR 014 — Context-keyed scene operation plugins](decisions/014-context-keyed-scene-operations.md)
15. [ADR 015 — Editable scene-object attributes](decisions/015-contextual-scene-form-contributions.md)
16. [ADR 016 — Contextual editable-attribute overrides and mutation](decisions/016-scene-form-field-bindings.md)
17. [ADR 017 — Lazy datastructure element-attribute tables](decisions/017-lazy-datastructure-attribute-tables.md)
18. [ADR 018 — Datastructure element-attribute editing](decisions/018-datastructure-attribute-editing.md)
19. [ADR 019 — Configured Viewer identity](decisions/019-configured-viewer-identity.md)
20. [ADR 020 — Viewer configuration lifecycle and field audit](decisions/020-viewer-config-lifecycle-and-audit.md)
21. [ADR 021 — Durable annotation ownership and schema](decisions/021-durable-annotation-ownership.md)
22. [ADR 022 — Distance-dimension unit semantics](decisions/022-distance-dimension-units.md)
23. [ADR 023 — Clean break for legacy Viewer annotations](decisions/023-annotation-clean-break.md)
24. [ADR 024 — Measurement outcomes and persistence](decisions/024-measurement-outcomes-and-persistence.md)
25. [ADR 025 — Scale and legend overlay contracts](decisions/025-scale-and-legend-overlays.md)
26. [ADR 026 — Measurement interaction and acquisition](decisions/026-measurement-interaction-and-acquisition.md)
27. [ADR 027 — Viewer measurement settings and UI](decisions/027-viewer-measurement-settings.md)
28. [ADR 028 — Fixed and associative dimension anchors](decisions/028-dimension-anchor-modes.md)
29. [ADR 029 — Persistent annotation collection and UI](decisions/029-persistent-annotation-collection-and-ui.md)
30. [ADR 030 — Always-visible persistent dimension rendering](decisions/030-always-visible-dimension-rendering.md)
31. [ADR 031 — Spatial object deletion](decisions/031-spatial-object-deletion.md)
32. [ADR 032 — Three-domain Viewer sidebar](decisions/032-three-domain-viewer-sidebar.md)

ADRs 013–016 are Accepted. ADRs 008–009 and 011–012 are superseded as recorded
in the decision index; ADR 010 remains Accepted with amended terminology.
The amended ADR 015–016 implementation is complete and verified; the
superseded `FormField` implementation was replaced.
ADRs 017–020 are Accepted and were implemented in order ADR 019, ADR 020, ADR
017, then ADR 018 so configuration and sidebar ownership were established
first. Local verification, independent review, and hosted verification passed.
ADR 003 is fully verified. ADR 004 is implemented, locally verified, and
independently approved; refreshed hosted core, Viewer, and framework
verification passed.
