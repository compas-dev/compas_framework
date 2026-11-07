# ADR 006: Public Viewer Integration Facade

## Status

Accepted.

## Context

`compas_model.ModelViewer` currently reaches into concrete renderer and sidebar
objects. Viewer has command and menu composition but no equally clear public
dock or synchronization boundary. Optional consoles or assistants should not
force shell, network, or credential behavior into the Viewer core.

## Options

1. Expose a small public Viewer facade for scene, state, refresh, history,
   commands, docks, annotations, and overlays.
2. Let integrations continue using renderer and widget internals.
3. Define a large abstract Viewer/controller framework for every domain.
4. Move model navigation and inspectors into `compas_viewer`.

## Recommendation

Choose option 1. Provide public operations for:

- scene access and GUID resolution;
- selection and transient state;
- categorized refresh;
- transform transactions and undo/redo;
- command registration and menu placement;
- dock addition/removal; and
- annotation and overlay addition/removal.

`compas_model` retains its authoritative tree, projections, inspectors,
contacts, quality settings, and render cache. It consumes the facade and stops
accessing private/concrete Viewer renderer and sidebar paths. Do not create a
generic controller base class.

A future console, terminal, or assistant may use a dock and registered command
API. Arbitrary Python/shell execution, subprocesses, credentials, network
transport, and assistant policy require a separate security ADR and are not
implemented in this wave.

## Consequences

- Domain packages gain a stable, testable integration surface.
- Viewer internals can change without coordinated domain rewrites.
- Public API growth is limited to demonstrated model and feature needs.
- Dock content remains Viewer/Qt-specific; core stays UI-independent.
- Console/chat presentation becomes possible without prematurely authorizing
  execution or remote services.

## Compatibility

Preserve `ModelViewer` user-facing hierarchy, selection, visibility, quality,
cache, and inspection behavior. Internal direct renderer/sidebar access is
removed after facade coverage exists.

## Verification

- Test facade behavior with a lightweight fake UI/renderer boundary.
- Forbid private renderer/sidebar access in model integration tests.
- Verify dock and command registration/removal and duplicate-ID failures.
- Verify plugin discovery imports no Qt/OpenGL/model implementation modules.

## Affected packages

`compas_viewer`, `compas_model`, and `compas_framework`.

## Dependencies

- [ADR 001](001-ownership-boundaries.md)
- [ADR 003](003-viewer-state-and-selection.md)
- [ADR 004](004-transform-refresh-undo.md)
- [ADR 005](005-annotations-and-overlays.md)
