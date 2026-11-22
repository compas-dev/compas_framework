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

## Direct-use follow-ups

Direct use after ADR 032 identifies seven independent refinements. ADRs 033–034
and 036–039 are Accepted and implemented. ADR 035 is implemented, locally
verified, and independently reviewed:

- keep the three-domain root; introduce independent Scene and Annotations
  splitters; remove the inline description textbox and expose its information
  through a modal Details dialog;
- separate normal Mesh vertex glyph visibility from measurement acquisition by
  rendering an invisible measurement-only vertex footprint;
- store a distance dimension's signed world-space offset and captured plane
  normal as durable scene presentation, without storing a full construction
  plane or changing the measured value;
- treat text pinned to a viewport location as a Viewer overlay in normalized
  screen coordinates; initially expose only programmatic add/remove and keep
  it outside Scene serialization unless a future Session/view-state decision
  and management surface explicitly provide persistence and interactive
  authoring;
- add only optional background color and logical-pixel padding to labels,
  without introducing a typography or theme abstraction;
- make Delete Selected dispatch to the selection owned by the current
  interaction domain, never to both spatial and annotation selections; and
- move the existing geometry creation hierarchy from top-level Add to
  **Scene → Add**, while keeping measurement acquisition tools under Measure.

The spatial dimension offset records only the plane normal needed for stable
layout. A reusable construction plane is an authoring aid and should be
designed separately rather than embedded in each dimension. Viewport text
persistence is likewise deferred to the separately proposed Session/view-state
boundary; configuration and Scene are not suitable owners.

Further UI and measurement feedback produces three additional independent
proposals:

- populate and show the default toolbar with a synchronized Render Mode
  selector and five exclusive standard-view buttons using the existing
  commands and Viewer state;
- replace Units and Measurement with Grid and Units, remove tolerance from the
  Viewer UI without changing global COMPAS tolerance, and align every System
  form on one two-column field layout; and
- add transient selection-driven area and volume inspection using represented
  items' public scalar APIs and exact supported world-transformation rules,
  without tessellation fallback or persistent annotations.

If accepted together, establish the final System ownership and layout first,
then add the synchronized toolbar controls, then add the independent area and
volume inspections.

## Accepted COMPAS Viewer theme structure

Treat COMPAS as Viewer's one built-in visual theme and retain `system`,
`light`, and `dark` as color-scheme choices. `system` continues to follow the
operating system; the other values force the corresponding COMPAS theme
variant. Do not add a fourth appearance value, a separate public theme field,
arbitrary stylesheet loading, or a theme registry while no second selectable
theme is required. The configuration shape and schema version remain
unchanged.

The initial theme owns Qt application chrome only. A private semantic token
module supplies complete light and dark palettes and, only where palette roles
are insufficient, one narrow application stylesheet. Renderer background,
selection, and grid colors and all scene, annotation, measurement, legend, and
overlay presentation retain their existing owners. Appearance switching stops
overwriting the renderer background, so explicit viewport choices survive
theme changes.

Retain the platform UI font, packaged COMPAS application icon, configurable
icon override, and existing monochrome icons. A new font or icon family is a
separate asset, licensing, fallback, and accessibility decision. Reconcile the
current System-section heading refinement with the private theme without
creating a public typography or spacing framework.

The inspected repositories do not define an authoritative COMPAS brand token
table. The approved implementation therefore uses ADR 043's Viewer-specific
palette without claiming organization-wide brand authority. Its exact tokens
and contrast requirements were approved on 2026-11-10. Native macOS, Windows,
and Linux visual verification remains part of rollout. ADR 043 records the full
alternatives, compatibility implication, and verification contract.

## Accepted persistent-dimension format editing

Keep **Grid and Units** as the presentation default for transient measurements
and dimensions created afterward. Do not retroactively rewrite existing
dimensions. Instead, expose **Coordinate Unit** and **Display Precision** in a
separate **Measurement Format** group when exactly one resolved
`DistanceDimension` is selected in Annotations.

Core gains validated mutable properties for the already serialized unit and
precision fields. Viewer mutates only the selected dimension and refreshes only
its annotation render layer. Precision uses one shared Core and Viewer domain
of 0–15 inclusive; values outside it raise `ValueError` and are never clamped
or truncated. Units remain declaration-only and perform no conversion.
Explicit labels remain verbatim overrides without bypassing validation.
Existing data or configuration above 15 is rejected without migration or a
schema change. No bulk editor, unit registry, or generic property abstraction
is introduced.
ADR 044 records the complete ownership, validation, and verification contract.
Implementation is present in the Core and Viewer working trees: validated
property assignment and selected-entry Measurement Format controls preserve
the separate ownership of durable snapshots and Viewer defaults. Local
verification and independent review pass.

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
33. [ADR 033 — Resizable Scene inspector and Details dialog](decisions/033-scene-inspector-details.md)
34. [ADR 034 — Mesh-vertex snapping independent of vertex glyphs](decisions/034-hidden-vertex-snapping.md)
35. [ADR 035 — Distance-dimension spatial layout](decisions/035-distance-dimension-spatial-layout.md)
36. [ADR 036 — Viewport text ownership and persistence](decisions/036-viewport-text-ownership-and-persistence.md)
37. [ADR 037 — Optional annotation label backgrounds](decisions/037-annotation-label-backgrounds.md)
38. [ADR 038 — Contextual Delete Selected](decisions/038-contextual-delete-selected.md)
39. [ADR 039 — Scene-owned Add menu](decisions/039-scene-add-menu.md)
40. [ADR 040 — Default toolbar view shortcuts](decisions/040-default-toolbar-view-shortcuts.md)
41. [ADR 041 — Grid and Units System section](decisions/041-grid-and-units-system-section.md)
42. [ADR 042 — Selected area and volume inspection](decisions/042-selected-area-and-volume-inspection.md)
43. [ADR 043 — Built-in COMPAS Viewer theme](decisions/043-built-in-compas-viewer-theme.md)
44. [ADR 044 — Editing persistent distance-dimension format](decisions/044-editing-persistent-dimension-format.md)
45. [ADR 045 — Default viewport and content contrast](decisions/045-default-viewport-content-contrast.md)
46. [ADR 046 — Viewer scheme-aware content palette](decisions/046-viewer-content-palette.md)
47. [ADR 047 — Editable parametric shape resolution](decisions/047-editable-parametric-shape-resolution.md)
48. [ADR 048 — Referenced Data domain](decisions/048-referenced-data-domain.md)
49. [ADR 049 — Viewer Settings surface](decisions/049-viewer-settings-surface.md)
50. [ADR 050 — Read-only Data item inspection](decisions/050-read-only-data-item-inspection.md)
51. [ADR 051 — Scene Object Details and settings boundary](decisions/051-scene-object-details-boundary.md)
52. [ADR 052 — Executable Viewer documentation and example coverage](decisions/052-executable-viewer-documentation-and-example-coverage.md)

ADRs 013–016 are Accepted. ADRs 008–009 and 011–012 are superseded as recorded
in the decision index; ADR 010 remains Accepted with amended terminology.
The amended ADR 015–016 implementation is complete and verified; the
superseded `FormField` implementation was replaced.
ADRs 017–020 are Accepted and were implemented in order ADR 019, ADR 020, ADR
017, then ADR 018 so configuration and sidebar ownership were established
first. Local verification, independent review, and hosted verification passed.
ADRs 050–052 were accepted on 2026-11-14 and remain independent. ADR 050
completes the existing read-only Data Details surface without changing Data
ownership. ADR 051 completes the read-only Scene Object Details snapshot while
retaining Object Settings as the sole editing surface. ADR 052 adopts an
executable Viewer documentation and category-level example contract without
changing runtime behavior.
ADR 003 is fully verified. ADR 004 is implemented, locally verified, and
independently approved; refreshed hosted core, Viewer, and framework
verification passed.

ADRs 033–039 respond to direct-use feedback. ADR 036 is Accepted with a
screen-pinned, non-persistent, programmatic-first contract. ADRs 037–039 are
implemented, locally verified, and independently reviewed. ADRs 040–042 are
also Accepted. ADR 034 is implemented, locally verified, and independently
reviewed. Its measurement-only Mesh-vertex footprints do not enter ordinary
rendering or add edge, face, or broader object-type acquisition. ADR 033 is
implemented and user-confirmed. ADR 035 was accepted on 2026-11-11,
implemented, locally verified, and independently reviewed; native direct use
and hosted verification remain pending.

The 2026-11-10 amendment to ADR 040 keeps the compact Render Mode dropdown but
replaces the native View combo popup with exclusive icon-only Perspective, Top,
Front, Right, and Ortho buttons. They use the existing palette-aware P, T, F,
and R assets plus a matching O asset; semantic titles remain tooltips and
accessible names. Native direct use showed that combo-popup teardown could
still disrupt viewport focus. One pending event-driven restoration now waits
for `focusWindowChanged` or a queued readiness check to observe the main window
focused and active with the popup cycle complete. It uses no arbitrary delay or
retry loop. The amendment narrowly extends an existing toolbar `button` item
with `state`, `value`, and optional `icon_only`, preserves custom text-only,
text-plus-icon, and unbound buttons, and does not authorize a general widget
registry.

The narrow 2026-11-10 amendment to ADR 029 changes only the color used by a
new default `DimensionStyle` from white to magenta. Explicit and serialized
colors remain authoritative, the Scene schema remains version 4, and no
adaptive or universal contrast guarantee is introduced.

## Approved direct-use presentation follow-up

The latest native retest accepts the standard-view button behavior, Camera
population, and general presentation, but rejects the remaining Render Mode
combo focus behavior. It also identifies missing label-background editing,
non-semantic letter icons, useful existing command candidates for the toolbar,
and insufficient contrast between the default white surface and white
viewport.

The proposed response is split by ownership:

1. Amend ADR 037 to expose the implemented optional label background and
   logical-pixel padding in the selected annotation's details. Disabling the
   background writes `None`; enabling it uses an explicit selected color. This
   changes no Core schema or serialization contract.
2. Amend ADR 040 again to remove the unreliable default Render Mode popup.
   Use four exclusive semantic buttons with original monochrome SVGs: a filled
   cube for Shaded, face-shaded cube for Lighted, translucent or dashed cube
   for Ghosted, and outline cube for Wireframe. Move Perspective, Top, Front,
   Right, and Ortho into one private fixed viewport control synchronized
   through the existing command and state path. This interprets the requested
   fixed view list as those five standard views. Add the existing Zoom
   Selected, Zoom Extents, and Capture View commands to the default toolbar
   with semantic magnifier/selection, framing, and camera assets.
3. Apply Accepted ADR 045 by changing Viewer's fixed default viewport
   background to `#D8DDE2` while preserving Core defaults and ADR 043's theme
   separation.

The fixed viewport control is private Viewer chrome, not a new public
interactive-overlay type or general widget registry. All icon titles remain
tooltips and accessible names. Asset provenance, licensing, palette behavior,
high-DPI rendering, checked state, and disabled state require verification.

These changes were approved on 2026-11-10, including the standard-view
interpretation and ADR 045's Viewer-owned `#D8DDE2` background. Package source
implementation, local verification, direct-source framework integration, and
independent re-review pass, and user direct use confirms the correction works
well. Hosted CI and candidate-artifact verification remain pending.

## Accepted grouped controls, Details, splitters, and content palette follow-up

The next direct-use checkpoint accepts the corrected implementation and asks
for a more compact composition:

1. Amend ADR 040 to replace the viewport's fixed view list and the toolbar's
   four render buttons with one private viewport menu. Its titled exclusive
   groups are **View** (Perspective, Top, Front, Right, Ortho) and **View
   Mode** (Shaded, Lighted, Ghosted, Wireframe). Add one default measurement
   menu button for Inspect Distance, Add Fixed, Add Associative, and Cancel;
   retain Zoom Selected, Zoom Extents, and Capture View.
2. Apply ADR 033's removal of the inline description and modal Details
   snapshot. Add independent resizable splitters for Scene hierarchy/details
   and Annotations list/dimension-details; neither domain resizes the other.
3. Amend ADR 037 so newly completed Viewer distance dimensions start with a
   two-pixel label background: `#FAFAFAE6` in light and `#10161BE6` in dark.
   Existing, explicit, serialized, text-annotation, and Core programmatic
   behavior remains unchanged.
4. Adopt ADR 046's exact Viewer defaults:

   | Role | Light | Dark |
   |---|---:|---:|
   | Viewport | `#FAFAFA` | `#10161B` |
   | Surface and face | `#D8DEE4` | `#3A4650` |
   | Line and edge | `#4B5563` | `#B8C2CC` |
   | Point and vertex | `#111827` | `#F2F6F8` |

Viewer resolves omitted geometry and dimension presentation when content is
created. Explicit and serialized values remain authoritative, Core defaults do
not change, and existing objects are not recolored on a live scheme switch.
The automatic viewport does follow the scheme unless explicitly configured.
Full live content inversion is deferred because it requires durable
automatic-versus-explicit provenance in Core rather than color-value guessing.

Viewer configuration advances to schema 4 with
`RendererConfig.backgroundcolor: Color | None`; `None` is automatic. Every
schema-3 concrete background, including `#D8DDE2`, migrates as explicit.
For Geometry, Mesh, Graph, and VolMesh, an explicit specialized color wins; an
omitted specialized channel continues to derive from an explicit base color;
scheme tokens apply only when both base and specialized channel are omitted.
Collections and buffer-backed objects keep existing explicit/per-element
semantics and receive tokens only through an already supported omitted uniform
channel.

These changes, including both domain-local splitters, were approved on
2026-11-11. Implementation, local verification, independent review, and native
direct use pass; hosted verification remains pending.

## Accepted ADR 035 initial editing surface

The preferred first authoring path for deterministic spatial dimension layout
is a **Spatial Layout** group in Annotations details for one selected, bound
distance dimension. It exposes a finite signed world-space Offset, optional
Plane Normal X/Y/Z components, derived read-only resolution Status, and Reset
Layout. All normal fields blank means no normal; otherwise all three finite
components are required.

Field edits remain a local draft, and tabbing preserves partial input.
**Apply Layout** replaces the complete layout atomically; invalid Apply and
Escape restore durable values without refresh. **Reset Layout** immediately
restores the default layout. A changed Apply or Reset refreshes only the
selected annotation once. Offset zero is resolved without a normal, regardless
of normal or anchor layout inputs. For nonzero offsets,
status precedence is unresolved anchor, coincident anchors, missing normal,
zero normal, parallel normal, then resolved. Missing, zero, or parallel layout
direction falls back to the current zero-offset line only when both anchors
resolve. An unresolved anchor preserves ADR 028 behavior and produces no
cached, stale, synthesized, or fallback dimension line. Viewer never falls
back to the camera.

Core gains the validated immutable-value-style layout data, while Scene
serialization advances from schema 4 to schema 5 and annotation-entry schema
version 2. Because `DataDecoder` reconstructs nested entries before the parent
Scene version is visible, current versioned entries require `layout` and reject
missing or unsupported versions. Only legacy unversioned schema-4 entries may
omit it; they retain `None` until binding normalizes distance entries and
preserves or validates text/arrow entries.
Viewer adds extension lines, displaced bounds, derived statuses, and the
single-selection form. Viewport dragging, construction-plane tools, collision
avoidance, and multi-dimension editing remain excluded. This amended ADR 035
was explicitly approved on 2026-11-11. Implementation, local verification,
and independent review pass. Native direct
use and hosted verification remain pending.

## Approved dimension-details and extension-line refinement

The accepted Annotations splitter must scroll rather than compress its details
form when the lower allocation is smaller than the content's natural height.
Use a vertical `QScrollArea` as the splitter child, retain natural group and
field spacing through a minimum-size layout constraint, disable horizontal
scrolling, and preserve transient splitter allocation across refreshes. This
is an approved correction to ADR 033 and is implemented and locally verified.

The independent line-weight request is a durable style change. Amend ADRs 029
and 035 with `extension_line_width`, a positive finite logical-pixel value.
The existing main-line default remains `3.0`; new extension lines default to
`1.0`. Viewer exposes **Dimension Line Width** and **Extension Line Width** and
uses the latter only for anchor-to-displaced-endpoint lines. A zero-offset
dimension has no extension lines.

Preserve existing serialized appearance through Scene schema 6,
annotation-entry schema 3, and dimension-style schema 2. Genuine schema-5
styles migrate `extension_line_width=line_width`; schema-6 requires the
versioned field. Explicit values remain authoritative. No extension color,
dash, opacity, or arrow-style surface is proposed. This style amendment
was approved on 2026-11-11. Implementation and local verification pass.

## Approved editable parametric-shape resolution

Core already owns durable `ShapeObject.u`, `ShapeObject.v`,
`SurfaceObject.u`, and `SurfaceObject.v` values with default `16`; Viewer
already consumes them when generating polygonal representations. ADR 047
approves exposing those fields without adding a second resolution API or
changing serialization.

Viewer shows **U Resolution** for Cone and Cylinder; **U Resolution** and
**V Resolution** for Sphere and Torus; U plus an even V for Capsule; and both
axes for parametric Surface objects. Box and unknown Shape producers expose no
ineffective controls. Values are whole integers with producer-specific minima.
Invalid edits roll back atomically without refresh. A valid edit rebuilds only
the affected object's representation, buffers, and bounds while preserving the
analytic shape, selection, unrelated objects, and scene round-trip.

Circle/Ellipse discretization, BRep/backend tolerances, adaptive level of
detail, global defaults, and a speculative maximum cap remain outside scope.
ADR 047 was accepted on 2026-11-11. Implementation, local verification, and
independent review pass. An exact native macOS Torus U-resolution change from
16 to 64 passed with a valid OpenGL context. The later interactive crash was
traced to Qt emitter lifetime and fixed. Native direct use on 2026-11-11
confirmed the resolution crash remains fixed at Torus U resolution 64.

Direct use at higher resolution also exposed an avoidable full rebuild for
ordinary display toggles. The accepted ADR 047 amendment routes `show`,
`show_points`, `show_lines`, `show_surfaces`, opacity, point size, and line
width through one selected-object settings-texture update and one redraw. These
edits do not tessellate, rebuild global buffers, or rebuild the Scene tree
unless displayed tree content changed. Resolution fields `u` and `v` remain
topology edits. Colors remain on the current appearance-data path for now.

ShapeObject and SurfaceObject forms label the existing line controls **Show
wireframe**, **Wireframe color**, and **Wireframe width**. MeshObject and
GraphObject retain edge terminology. The wording introduces no durable alias,
API, or serialization change. This amendment is accepted and implementation is
locally verified and independently reviewed. Native direct use confirms that a
Torus at U resolution 64 toggles **Show wireframe** off and on responsively and
accepts the wireframe wording.

## Accepted referenced Data domain

Scene already exposes a non-owning runtime binding map for item GUIDs referred
to by spatial objects and annotations. Accepted ADR 048 adds a fourth top-level
Viewer **Data** domain as a flat projection of those references, not a second
store. One row per distinct GUID is ordered by first spatial-hierarchy then
annotation reference and shows name, type, bound/unresolved status, and
reference count. Shared items are deduplicated; unresolved GUIDs remain visible
without implicit resolution.

Data selection is transient and independent from Scene, Annotations, viewport,
and element-table selection. A read-only modal Data Details snapshot shows
identity/reference metadata and safe inspected parameters. Mesh and Graph
reuse ADR 017's lazy tables in read-only mode with declared columns only.

The projection refreshes after scene replacement, reference add/remove, item
binding, and Data-domain activation while preserving selection by GUID where
possible. It neither mutates data nor rebuilds render buffers. Unattached data,
Session aggregation, files and resolvers, loading, editing, deletion, search,
persisted selection, and modeless inspectors remain outside scope. The user
approved this narrow first step on 2026-11-11. Implementation, local
verification, and independent review pass, with the final sidebar order Scene,
Data, Annotations, System. Direct object/reference additions refresh Data once
without renderer work, selection survives refresh while still referenced, and
safe shared inspection isolates attribute failures without reading arbitrary
`__data__`. The active Scene is the initial inventory source. A future Session
ADR may replace or extend it with unattached or multi-scene data, but Viewer
must remain a read-only consumer rather than the aggregate owner.

## Accepted Viewer Settings surface

Direct use identifies a category mismatch in the resulting four-tab sidebar:
Scene, Data, and Annotations are content domains, while System is a collection
of Viewer settings. Accepted ADR 049 leaves exactly the three content domains
in the right sidebar and moves the existing Camera, Display, and Grid and Units
sections into one per-Viewer modeless **Viewer Settings** window.

The window is opened from **View → Viewer Settings…**, refreshed and
raised on reuse, hidden rather than destroyed on close, and owned by the main
Viewer lifecycle. Its visibility, geometry, and focused section remain
transient, as does its scroll position. Window-level Escape hides only Viewer
Settings; it does not cancel measurement or clear content selection. Existing
renderer, measurement, state, and configuration paths stay unchanged.

The accepted decision replaces the System sidebar identifier and
`focus_system_section` with one settings-window API and moves the three
components from `viewer.sidebar_items` to `viewer.settings_items`, without
aliases or overlapping supported paths. The public navigation boundary is
`viewer.ui.settings.show(section)`, and `default_settings_items()` provides the
built-in composition. The implemented setup path accepts typed keyword-only
`sidebar_items` and `settings_items` iterables on the first `Viewer(...)`
construction, shallow-copies them before UI construction, and uses built-in
definitions when omitted. Because Viewer is a process-local singleton, later
constructor calls ignore new composition inputs, and post-construction list
mutation does not live-recompose the interface. No reset or reload framework
is added. A modal dialog would block live
viewport tuning; a dock would introduce layout and persistence decisions; and
a popover or drawer would be too small and focus-sensitive for the existing
forms. The user approved ADR 049 on 2026-11-14. Implementation and verification
now pass locally, including independent re-review and the framework
direct-source gate. The Viewer tutorial and executable Viewer Settings example
cover the setup-time composition and navigation contract. A permanent public
singleton regression now verifies that later `Viewer(...)` composition inputs
are ignored; clean follow-up review reports no findings. Native macOS modeless
focus, high-DPI, and direct-use confirmation
plus refreshed hosted CI remain pending.

## Accepted Scene and Data inspection completion

The current Scene and Data surfaces expose complementary but incomplete views.
Object Settings edits the normalized declared Viewer-context attributes, while
Object Details shows only a small descriptive snapshot. Data Details shows safe
parameters for general Data, but substitutes Mesh/Graph element tables for
those parameters and does not expose general `Datastructure.attributes`.

The recommended correction is two independent read-only decisions.

### Data Details interface

Accepted ADR 050 preserves ADR 048's identity/reference header and gives every
bound item one ordered tab surface:

1. **Parameters** — safe available public constructor parameters with no
   serialized fallback or arbitrary `__data__` traversal;
2. **General Attributes** — the ordered public `attributes` mapping for verified
   Core `Datastructure` values only; and
3. the existing lazy read-only Mesh vertex/edge/face or Graph node/edge tabs.

Empty Parameters or General Attributes tables remain visible. Component tabs
retain ADR 017's declared-column, effective-value, lazy-read, and sparse-omission
semantics. Unresolved items remain metadata-only. Each value-formatting failure
is isolated to its row or cell. Parameter and General Attributes tables use
**Parameter/Attribute** plus **Value** columns and the existing `str(value)` or
`<unavailable: ExceptionType>` convention. Component tables retain their
existing key, scalar, and Boolean presentation.

The Data projection remains non-owning and read-only. No edit, bind, resolve,
rename, delete, selection-coupling, serialization, renderer-refresh, or generic
inspection registry is added. VolMesh, CellNetwork, external Data types, and
undeclared sparse attributes remain unsupported until concrete evidence
justifies a later decision.

### Scene Object Details interface

Accepted ADR 051 preserves Object Settings as the only editing surface and
expands the one-object modal Details snapshot into four ordered sections:

1. **Identity** — name, concrete SceneObject type and GUID, represented-item
   type and GUID, and binding status;
2. **General Scene State** — visibility, base color, opacity, and local
   transformation;
3. **Type-Specific Scene State** — every editable or noneditable declaration
   from `scene_state_fields()`, in namespace and declaration order; and
4. **Represented Item Parameters** — existing safe parameters when bound.

Type-specific rows use stable `namespace.field` identifiers and read values
through each declaration's `attribute`. The snapshot does not inspect unknown
extension payloads, `__dict__`, arbitrary properties, or adapter caches. One
read/format failure is isolated without hiding other state. Unresolved items
still show complete SceneObject state, and the existing multiple-selection
count/type/name snapshot remains unchanged.

The existing scrolling text snapshot remains the presentation surface. Each
section has its exact heading; identity and base-state rows use the labels in
ADR 051, declared state uses `namespace.field: repr(value)`, and parameter rows
use `name: repr(value)`. A failed value is shown as
`<unavailable: ExceptionType>`.

Object Settings continues to resolve ADRs 015–016's normalized editability
mapping, own editor/validation behavior, and select refresh after atomic
mutation. Object Details adds no second setter or refresh path.

### Alternatives and tradeoffs

Editable Data is not recommended. A deduplicated item may have many referrers,
so editing requires new decisions for validation, atomicity, referrer-wide
refresh, defaults/reset, and undo. It conflicts with ADR 048's accepted
read-only boundary and needs a separate future ADR.

A generic Data or Scene-details registry is also not recommended. Existing
public Datastructure and SceneStateField contracts satisfy the demonstrated
Mesh/Graph and SceneObject needs. A registry would introduce extension and
presentation metadata without evidence for additional producers.

Keeping the current surfaces avoids implementation work but fails the stated
need to access general and component-specific data together and to inspect
noneditable SceneObject state.

### Affected packages and compatibility

Only `compas_viewer` runtime, tests, examples, and documentation change.
`compas` already provides the required public contracts; no Core source,
schema, serialization, or migration change is proposed. `compas_framework`
adds direct-source integration assertions for the resulting read-only surfaces.

Both changes are additive inside existing modal snapshots. Existing Data and
Scene selection, editing, refresh, identity, and configuration behavior remain
unchanged. ADRs 050 and 051 may be implemented and verified independently.

### Required tests and examples

- Verify Parameters and General Attributes order, emptiness, safe formatting,
  and failure isolation.
- Verify Mesh/Graph component tabs appear alongside general sections while
  retaining lazy declared-column behavior and sparse omission.
- Verify unresolved and shared Data identity/reference behavior and prove
  Details causes no mutation or renderer/UI refresh.
- Verify exact Object Details identity/base-state fields and namespace/field
  declaration order across representative SceneObject types.
- Verify unresolved-item, read/format failure, multiple-selection, and
  no-mutation/no-refresh behavior.
- Verify Object Settings remains exactly the normalized editable mapping and
  the only editing surface.
- Add one focused example with Mesh general attributes, declared defaults,
  local component overrides, and shared Scene references; extend the Viewer
  tutorial and representative built-in examples to document the distinctions
  among Object Settings, Object Details, Data Details, opt-in editable Scene
  Attributes, and Viewer Settings.

The user accepted ADRs 050 and 051 on 2026-11-14. Their uncommitted Viewer
implementation, focused and full package tests, typing and formatting gates,
strict documentation, direct-source framework integration, and independent
runtime review pass. Native interaction/visual evidence, refreshed hosted CI,
and candidate artifacts remain separately pending.

## Accepted executable Viewer documentation contract

Accepted ADR 052 separates documentation quality from the runtime ownership in
ADRs 049–051. It recommends one maintained end-to-end tutorial backed by one
authoritative runnable script, plus focused workflow/category examples rather
than ad-hoc prose, a prose-only tutorial, or an exhaustive example for every
public symbol. Public and touched Python APIs use MkDocs-compatible NumPy
docstrings and Python 3.12 annotations without changing runtime semantics.

The exact coverage matrix in ADR 052 spans Scene/content domains and inspection
boundaries, Viewer Settings/configuration, selection/transforms/refresh,
measurements/annotations, serialization, overlays, dynamic examples, and
optional geometry backends. Python under `docs/examples/` is checked by Ruff
and Pyright. The canonical tutorial and representative workflows receive
headless smoke or contract coverage; strict MkDocs, link/snippet validation,
focused doctests where applicable, and diff checks complete the automated
documentation gate. Native rendering, visual layout, focus, scrolling,
keyboard behavior, and high-DPI checks remain separately reported evidence.
Optional backend examples must name their dependency and must not convert an
unavailable runtime into a claimed pass.

Documentation may describe only implemented and verified behavior. Runtime
gaps found while documenting a workflow return to the ADR that owns the
contract; they are not fixed speculatively under ADR 052. The uncommitted
end-to-end tutorial, Viewer Settings and Object/Data inspection examples,
coverage matrix, and affected docstring/type work now implement the accepted
documentation contract and follow the verified disposition of ADRs 050 and
051.

Only `compas_viewer` documentation-facing source, examples, documentation
tests, and package documentation configuration are in scope. ADR 052 changes
no runtime API, behavior, schema, serialization, ownership, or migration
contract. The user accepted ADR 052 on 2026-11-14. The documentation-example
suite passes 20 tests; authoritative examples pass Ruff, formatting, and
Python 3.12 Pyright; strict MkDocs and `git diff --check` pass. Independent
review findings on annotation serialization coverage and scope wording were
corrected and revalidated. Native and optional-backend evidence remains
separately pending.
