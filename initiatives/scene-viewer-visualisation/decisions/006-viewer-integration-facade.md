# ADR 006: Public Viewer Integration Facade

## Status

Accepted.

## Context

Viewer-owned commands and components reach into concrete renderer and widget
objects. Viewer has command and menu composition but no equally clear public
dock or synchronization boundary. Optional consoles or assistants should not
force shell, network, or credential behavior into the Viewer core.

## Options

1. Expose a small public Viewer facade for scene, state, refresh, history,
   commands, docks, annotations, and overlays.
2. Let integrations continue using renderer and widget internals.
3. Define a large abstract Viewer/controller framework for every domain.
4. Design the facade around the current draft `ModelViewer` controller.

## Recommendation

Choose option 1. Provide public operations for:

- scene access and GUID resolution;
- selection and transient state;
- categorized refresh;
- transform transactions and undo/redo;
- command registration and menu placement;
- dock addition/removal; and
- annotation and overlay addition/removal.

The facade is defined only by approved Viewer-owned tools, commands, state,
annotations, overlays, refresh, and UI composition. Do not create a generic
controller base class or add operations solely to match a current external
consumer.

A future console, terminal, or assistant may use a dock and registered command
API. Arbitrary Python/shell execution, subprocesses, credentials, network
transport, and assistant policy require a separate security ADR and are not
implemented in this wave.

## Consequences

- Viewer-owned components gain a stable, testable integration surface that
  later consumers may reuse.
- Viewer internals can change without coordinated domain rewrites.
- Public API growth is limited to demonstrated Viewer feature needs.
- Dock content remains Viewer/Qt-specific; core stays UI-independent.
- Console/chat presentation becomes possible without prematurely authorizing
  execution or remote services.

## Compatibility

The current draft `ModelViewer` has no compatibility requirements under this
ADR. Its later redesign may consume the proven facade but may not enlarge it
without a demonstrated requirement and approval.

## Verification

- Test facade behavior with a lightweight fake UI/renderer boundary.
- Forbid private renderer/widget access in Viewer-owned command, tool, and
  component tests.
- Verify dock and command registration/removal and duplicate-ID failures.
- Verify plugin discovery imports no Qt/OpenGL or optional-consumer
  implementation modules.

## Affected packages

`compas_viewer` and `compas_framework`. `compas_model` is a later redesign
consumer.

## Dependencies

- [ADR 001](001-ownership-boundaries.md)
- [ADR 003](003-viewer-state-and-selection.md)
- [ADR 004](004-transform-refresh-undo.md)
- [ADR 005](005-annotations-and-overlays.md)

## Refinement after acceptance

The original context and compatibility clauses relied too heavily on the
current `compas_model.ModelViewer`. Explicit user correction establishes that
controller as a draft that may be redesigned freely. The accepted decision is
therefore narrowed to a small Viewer-owned public boundary justified by
Viewer's own approved capabilities; no ModelViewer behavior or controller
shape is preserved.
