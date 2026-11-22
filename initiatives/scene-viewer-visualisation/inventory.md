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

## 2026-11-10 direct-use toolbar and presentation evidence

The latest direct-use retest confirms that the five standard-view buttons,
initial Camera section, and general presentation work. It also supplies
contrary evidence for the remaining Render Mode focus claim: choosing a mode
from the native macOS combo popup still does not reliably return interaction
focus to the viewport.

The current popup tests do not reproduce that native path. They call
`hidePopup()` when synthetic interaction leaves the popup visible, which
forces the `Hide` event awaited by the implementation. A native popup can
close without sending that event to either cached watched object, leaving the
pending focus restoration stranded.

Additional verified inventory:

- `label_background` and `label_background_padding` already persist and render
  for text-bearing annotations, but the Annotations details panel has no
  controls for them;
- Core materializes white as the default scene-object color, and Viewer also
  defaults its viewport background to white. ADR 043 intentionally prevents
  the light/dark Qt theme from changing either content or renderer colors;
- the current P, T, F, R, and O SVGs are letter glyphs rather than pictorial
  view assets, although the existing palette-aware SVG path can render
  semantic monochrome assets;
- Zoom Selected, Zoom Extents, and Capture View already exist as registered
  commands and View-menu actions; and
- the approved overlay canvas is paint-only and mouse-transparent. An
  interactive fixed view list therefore needs private viewport chrome, not an
  expansion of the public overlay layer.

For the proposal, “view selection” is interpreted as the fixed Perspective,
Top, Front, Right, and Ortho choices. This interpretation remains an explicit
approval point.

On 2026-11-10 the user approved that standard-view interpretation, the ADR 037
and ADR 040 amendments, and ADR 045 option 1 with Viewer's fixed default
background set to `#D8DDE2`. Core's white default remains unchanged.

The approved correction is implemented and locally verified. The Viewer suite
passes 596 tests with one expected offscreen OpenGL skip; six focused
corrected-contract tests and independent re-review pass. Ruff, formatting,
configured Pyright, strict MkDocs, `git diff --check`, and the direct-source
framework gate pass. Direct-use, hosted CI, and candidate artifacts remain
pending.

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
# COMPAS Viewer theme follow-up

The current public appearance contract is the closed
`Literal["system", "light", "dark"]` configuration field. Viewer applies a
complete palette to the application-wide Qt instance, observes operating-system
scheme changes for `system`, and currently forces the renderer background when
the effective appearance changes. Renderer background, selection, and grid
colors otherwise remain separately persisted configuration; scene objects,
annotations, measurements, legends, and overlays own their own presentation.

There is no centralized theme or design-token module. Small component-local
stylesheets coexist with platform Qt typography. The pending System-section
refinement adds another local heading style. The packaged COMPAS application
icon and configurable icon override are already established, while remaining
UI icons are monochrome Font Awesome SVGs. FreeSans is packaged for rendered
annotation text, not registered as the Qt application font.

The inspected Viewer, Core, and framework repositories do not declare an
authoritative COMPAS brand palette. MkDocs uses blue and light-blue Material
settings, and examples contain blue values, but neither is sufficient evidence
for organization-wide design tokens. Any exact light/dark palette therefore
requires an approved brand source or must be described narrowly as
Viewer-specific COMPAS styling.

Relevant implementation and verification surfaces include
`compas_viewer.config.UIConfig`, `Viewer.set_appearance`, the View → Appearance
menu, component-local stylesheets, packaged icons, configuration and Viewer
tests, distribution checks, and native Qt rendering across supported
platforms.

## 2026-11-11 grouped-control and palette findings

The private viewport currently owns five labeled view buttons, while the
default toolbar owns four render-mode buttons plus Zoom Selected, Zoom Extents,
and Capture View. The existing View menu already provides the requested View
and View Mode groupings through stable commands and state paths. A private
viewport `QToolButton`/`QMenu` can reuse them without extending the public
mouse-transparent overlay layer. Existing Measure commands cover Inspect
Distance, Add Fixed Distance, Add Associative Distance, and Cancel.

`ObjectSetting` still owns an inline read-only description textbox. Accepted
ADR 033 removes it in favor of a modal Details snapshot and adds independent
domain-local splitters for Scene hierarchy/details and Annotations
list/dimension-details. Neither splitter owns or resizes the other domain.

Viewer-acquired dimensions currently inherit Core's transparent label
background. The narrow new-default boundary is interactive Viewer completion;
Core and general programmatic construction need not change.

Core materializes concrete scene colors and serializes them without recording
whether they were omitted or explicit. Viewer therefore cannot safely invert
existing content during a scheme switch. The bounded option is to resolve
scheme-aware Viewer defaults at creation time, preserve explicit and
serialized values, and let only an automatic viewport follow later scheme
changes. Full live inversion requires a separately approved Core provenance
and schema design.

The automatic viewport itself needs durable provenance. The accepted bounded design
uses Viewer configuration schema 4 with `backgroundcolor=None` as the only
automatic marker; all schema-3 concrete values migrate as explicit. Existing
Geometry, Mesh, Graph, and VolMesh uniform channels can apply scheme tokens
only when both base and specialized arguments are omitted. An explicit base
continues to drive Core's existing specialized-color derivation. Collections
and buffer-backed objects must retain current explicit/per-element behavior.

## 2026-11-11 ADR 035 implementation checkpoint

The amended deterministic distance-dimension spatial-layout contract is
Accepted. It adds durable signed world-space offset plus optional plane-normal
presentation, Scene schema 5 migration, displaced dimension and extension-line
rendering, and one atomic single-dimension Spatial Layout form. Unresolved
anchors retain ADR 028 behavior and never render cached or synthesized lines.
Dragging, construction-plane tools, collision avoidance, and multi-dimension
editing remain outside the approved initial scope. Core and Viewer
implementation, documentation, local verification, direct-source framework
integration, and independent review pass. Native direct use, hosted CI, and
candidate-artifact verification remain pending.

## 2026-11-11 dimension-details refinement

Direct use shows that the Annotations details widget is the splitter child
itself, with only an 80-pixel minimum height and no scroll viewport. Qt
therefore compresses the visible groups and fields when the lower splitter
allocation shrinks. The implemented, locally verified correction makes a vertical `QScrollArea`
the splitter child and keeps the complete details widget at its natural
minimum height.

`DimensionStyle.line_width` already defaults to `3.0` and currently controls
the displaced dimension line and both extension lines. The Viewer form exposes
only that one width. The implemented, locally verified narrow amendment adds a durable
`extension_line_width` defaulting to `1.0` for new styles, with separate form
labels and rendering. Because the nested style payload is closed, preserving
legacy appearance requires versioned style data and migration from the legacy
stored `line_width`, not a Viewer-only multiplier.

## 2026-11-11 parametric-shape resolution findings

Resolution is already durable rather than fixed in Viewer. Core scene
`ShapeObject` and `SurfaceObject` store `u` and `v` with default `16`, Viewer
accepts and consumes them during polygonal conversion, and existing refresh
paths rebuild representation data and bounds. The missing contract is
editability and applicability filtering.

Cone and Cylinder consume U only. Sphere and Torus consume U and V with a
minimum of `3`. Capsule consumes U at least `3` and even V at least `4`.
Parametric Surface consumes U and V at least `1`. Box ignores both, and the
current unknown-Shape conversion consumes neither. Accepted ADR 047 therefore
reuses existing fields, filters ineffective controls, and adds no alias or
schema change. Its implementation, local verification, and independent review
pass. A native macOS Torus U-resolution change from 16 to 64 passed in an exact
subprocess with valid OpenGL. A later interactive crash was diagnosed as Qt
emitter lifetime and fixed; direct user retesting remains pending.

High-resolution direct use then showed slow line visibility changes. The
current edit route treats ShapeObject and SurfaceObject appearance settings as
full data changes: it regenerates representation data, rebuilds renderer
buffers globally, and refreshes the Scene tree. The renderer already exposes a
per-object settings-texture update path for visibility and scalar display
settings, so tessellation is unnecessary for `show`, `show_points`,
`show_lines`, `show_surfaces`, opacity, point size, and line width. In contrast,
`u` and `v` change topology and must retain the representation/buffer/bounds
rebuild. Colors currently use appearance data rather than the settings texture
and remain on that path for this amendment.

The durable line fields describe a tessellation wireframe for ShapeObject and
SurfaceObject, but edges for MeshObject and GraphObject. The approved UI
wording therefore changes only the Shape/Surface labels to **Show wireframe**,
**Wireframe color**, and **Wireframe width**. It does not rename fields, add
aliases, or change serialization.

The optimization and wording implementation passes the final 656-test Viewer
suite with two expected offscreen native-OpenGL skips, plus Ruff, formatting,
Pyright, strict documentation, and diff checks. Independent review passes. The
framework direct-source gate passes 15 tests with one expected exact-VCS skip.
The earlier exact native high-resolution Torus probe passes with native OpenGL,
and the Qt emitter-lifetime crash correction remains intact. Direct user
confirmation on 2026-11-11 passes: with Torus U resolution 64, **Show
wireframe** toggles off and on responsively, the wording is accepted, and the
resolution crash remains fixed.

## 2026-11-11 referenced-data findings

Every spatial scene object and annotation entry retains an item GUID, and
`Scene.item_store` exposes bound referenced items through one read-only,
non-owning runtime mapping. Shared references resolve to the same item instance;
unresolved GUIDs remain inspectable; bindings are pruned only after their final
scene reference disappears. The binding table is not serialized and rejects
unreferenced items.

Viewer can derive a flat GUID-deduplicated inventory from public scene objects,
annotations, and `item_store` without changing Core ownership. Existing Object
Details provides safe parameter inspection, and ADR 017's lazy Mesh/Graph
models can support read-only attribute views. Editing from a deduplicated Data
surface would require refreshing every referring render object and is excluded
from accepted ADR 048. The user approved this narrow, read-only first step on
2026-11-11. Implementation, local verification, and independent review pass.
The final sidebar order is Scene, Data, Annotations, System. Direct object and
reference additions refresh the projection once without renderer work;
selection survives while its GUID remains referenced. Shared inspection avoids
arbitrary `__data__` and isolates individual attribute failures. Its source is
only the active Scene's references. A future Session ADR may replace or extend
that source with unattached or multi-scene data while keeping ownership outside
Viewer.

The completed ADR 048 tree, including final removal, clearing, batched-deletion,
and Scene-name refresh regressions, passes 672 Viewer tests with two expected
offscreen OpenGL skips and 16 framework direct-source tests with one expected
exact-VCS skip. Ruff, formatting, Pyright, strict MkDocs, diff checks, and
independent review pass. Native user direct use, hosted CI, and
candidate-artifact verification remain pending.

## 2026-11-14 Scene and Data inspection findings

The accepted Scene and Data surfaces expose different partial views of the
same referenced content.

`ObjectSetting` is the editing surface for the normalized attributes governed
by ADRs 015–016. It includes general editable values such as name and opacity,
Viewer-context contributions, and applicable type-specific durable state such
as Mesh display fields or Shape/Surface resolution. It intentionally excludes
noneditable state. Its modal Object Details snapshot currently shows name,
represented-item type, visibility, and safe represented-item parameters for
one selection; it does not show SceneObject identity, item identity, base
presentation, transformation, or declared noneditable type-specific scene
state. Multiple-selection Details shows only count, represented types, and
names.

ADR 048's Data Details dialog shows identity, binding status, and all Scene or
Annotation references. For a bound general `Data` value it shows safe public
constructor parameters without reading arbitrary `__data__`. For Mesh and
Graph it currently shows the accepted lazy read-only element-domain tables
*instead of* the parameter table. It therefore does not provide one combined
view of parameters and component attributes.

Every verified Core `Datastructure` owns a public ordered `attributes` mapping
for general attributes. Mesh and Graph additionally expose the declared
default-domain mappings and singular APIs already used by ADR 017's lazy
vertex/edge/face or node/edge tables. Data Details does not currently show the
general `Datastructure.attributes` mapping. General attributes supplied through
constructor `**kwargs` are intentionally not recovered by constructor-parameter
inspection.

The existing component-table contract remains deliberately narrow: only Mesh
and Graph are supported, only declared default-attribute columns are shown,
effective values are read lazily, and sparse undeclared local attributes are
omitted. VolMesh, CellNetwork, arbitrary `Data` subclasses, and a generic
inspection registry have no accepted component-domain contract.

Data is a GUID-deduplicated, non-owning projection. A shared item may have many
spatial and annotation referrers, while an unresolved row has no bound value to
inspect. Editing from Data would therefore require new ownership, validation,
atomicity, refresh-all-referrers, default/reset, and undo decisions that ADR
048 explicitly excludes. Read-only inspection can be expanded without any
Core API, serialization, schema, selection, or renderer-refresh change.
