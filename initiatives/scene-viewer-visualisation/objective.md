# Scene, Viewer, and Visualisation Initiative

## Objective

Establish a simple, coherent, and scalable visualisation architecture across
COMPAS core scenes and `compas_viewer`. Users should be able to visualise large indexed datasets,
select and transform objects consistently, add measurements and annotations,
and extend the viewer UI without coupling durable scene data to a particular
renderer or Qt widget hierarchy.

The initiative should clarify ownership before adding features. Core scene
data, renderer-facing geometry, persistent configuration, transient tool and
selection state, and domain-specific controllers must each have one clear
home and contract.

## Questions to resolve

1. Which data and behavior belong to backend-neutral `compas.scene`, the
   viewer renderer, viewer application state, and package-specific adapters?
2. What indexed point, line, and triangle buffer contract supports efficient
   visualisation without requiring heavyweight core geometry objects?
3. How should selection, element picking, hover, and multi-selection be shared
   by the viewport, scene graph, and programmatic consumers?
4. What mutation and undo contract supports single- and multi-object
   transformations?
5. Which annotations, measurements, scale indicators, legends, and overlays
   are durable scene data, and which are transient tool or UI state?
6. How should persistent configuration be separated from reactive session,
   tool, and UI state?
7. Which stable extension boundary can support docks, consoles, terminals, or
   optional assistants without embedding those concerns in core scene data?
8. Which public Viewer operations are required by its own tools, UI components,
   and independent future consumers?
9. Which local, package, framework-integration, and artifact evidence is
   required for each approved wave?

## Design principles

- Keep core scene infrastructure backend-neutral.
- Preserve indexed data and batch rendering where possible; do not expand a
  large edge or triangle set into one Python object per primitive.
- Keep raw NumPy-compatible buffers valid inputs without forcing conversion
  through COMPAS geometry or data objects.
- Separate durable scene state, persistent viewer configuration, and transient
  interaction state.
- Provide one observable selection path for viewport, scene graph, and code.
- Prefer explicit, small data contracts over renderer-specific base classes or
  speculative extension frameworks.
- Keep plugin discovery graphics-free and optional UI/runtime imports lazy.
- Reuse accepted tessellation, typing, plugin, and repository-modernisation
  contracts rather than duplicating them.
- Make high-level convenience APIs simple while keeping ownership and
  performance costs visible.

## Refined initial scope

- `compas`: scene hierarchy, scene-object identity and transformations, and
  any approved backend-neutral contracts.
- `compas_viewer`: render buffers, GPU lifecycle, viewport interaction,
  selection, overlays, commands, and UI state.
- `compas_framework`: installed cross-package verification.

## Deliverables

1. A verified cross-package inventory and approved architecture decisions.
2. Clear ownership and state boundaries across core scene and Viewer runtime
   concerns.
3. Efficient convenience APIs for indexed points, edges, and triangles.
4. Consistent observable selection and transformation contracts.
5. An extensible annotation, measurement, and overlay foundation.
6. Public integration boundaries for Viewer tools, components, and optional
   UI extensions.
7. Package-local and framework-level tests, examples, and documentation.

## Non-goals without a later scope decision

- Replacing the core plugin manager or accepted geometry conversion APIs.
- Making Qt, OpenGL, or viewer-specific state a core COMPAS dependency.
- Implementing a chatbot service, shell execution engine, or remote transport
  before the UI extension and security boundaries are approved.
- Migrating notebook, Rhino, Grasshopper, or Blender adapters in the initial
  wave.
- Turning `compas_session` into a general reactive application store without
  a separate persistence decision.
- Preserving the current draft `compas_model.ModelViewer` controller shape or
  behavior. It is a later redesign consumer, not an architectural constraint.
- Adding modeling functionality to the viewer or duplicating domain data
  structures in the scene graph.

## Dependencies

- Geometry-tessellation ADRs 022 and 024 govern transfer-oriented
  `Tessellation`, producer conversions, and representation-preserving mesh
  triangulation.
- Typing-alignment decisions govern structural NumPy-compatible inputs.
- Plugin-implementations decisions govern lightweight Viewer-context
  registration and leave coordinated model/viewer lifecycle evidence open.
- Repository-modernisation decisions govern package workflows and artifact
  verification.

## Current status

Reconnaissance is complete. ADRs 001–007 are Accepted, but Proposed amendment
ADRs 008–009 block implementation pending approval. The current draft
`ModelViewer` is evidence and a later redesign target, not a contract.
