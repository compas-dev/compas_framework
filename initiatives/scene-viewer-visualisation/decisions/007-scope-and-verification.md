# ADR 007: Initial Scope and Verification

## Status

Accepted.

## Context

Core Scene is consumed by Viewer, model, notebook, session, and CAD-host
packages. Expanding the first implementation across every backend would mix
runtime-specific migrations and make completion evidence unavailable. Package
tests alone do not prove installed cross-package behavior.

## Options

1. Implement an initial core/Viewer/framework wave and compatibility-
   review adjacent consumers.
2. Migrate every visualisation and host package in one wave.
3. Change Viewer only and defer core scene alignment.
4. Accept package-local source tests as completion evidence.

## Recommendation

Choose option 1.

Initial implementation packages are `compas`, `compas_viewer`, and
`compas_framework`. Review `compas_model`, `compas_session`,
`compas_notebook`, Rhino, Grasshopper, and Blender for compatibility with core
changes, but do not modify them without a scope amendment and approval.

Require:

- focused and full applicable local tests, Ruff, Pyright, and strict docs;
- clean package CI and built-wheel checks at exact heads;
- framework CI installing exact candidates and exercising plugin discovery,
  scene and Viewer construction, indexed buffers, selection, transformations,
  annotations, serialization, and graphics-free discovery; and
- candidate-artifact CI for claims about independently built distributable
  compatibility.

Coordinate the plugin initiative's installed model/viewer registry gate rather
than creating a second competing test.

## Consequences

- The first wave remains verifiable on ordinary CI with offscreen Viewer
  support.
- Host-specific behavior remains unverified and unmodified, not implicitly
  passed.
- Core compatibility risks are still inspected before implementation.
- Later session, notebook, host, sub-object selection, advanced transform,
  and console/assistant waves require explicit decisions.

## Compatibility

Any approved core change must preserve current public scene contracts for
compatibility-only consumers or identify a concrete blocker and return for
scope/compatibility approval before implementation proceeds.

## Verification

- Record local, package, framework-integration, and candidate-artifact
  evidence separately in the handoff.
- Pin exact commit and artifact identities.
- Treat unavailable required runtime evidence as unverified, not passing.
- Keep generated files in isolated temporary directories.

## Affected packages

Initial: `compas`, `compas_viewer`, and `compas_framework`.

Later redesign consumer and regression evidence: `compas_model`.

Compatibility review only: `compas_session`, `compas_notebook`, Rhino,
Grasshopper, and Blender scene adapters.

## Dependencies

- [ADRs 001–006](README.md)
- Plugin-implementations ADR 005

## Refinement after acceptance

The initial package list previously included `compas_model` as though the
current `ModelViewer` behavior constrained this initiative. Explicit user
correction moves it to a later redesign phase. Its current serialization
failure remains valid evidence for core scene reconstruction, but its
hierarchy projections, selection behavior, cache, controller shape, and facade
usage are not initial-wave completion criteria.
