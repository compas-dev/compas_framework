# Repository Modernisation Initiative

## Objective

Define and apply one simple, explicit, and maintainable repository standard to
the core COMPAS packages. Use `compas`, `compas_occ`, and `compas_cgal` as
reference implementations, while also correcting the inconsistencies found in
those repositories rather than copying them into the wider package set.

The standard should align documentation, packaging, dependency management,
code-quality tools, shared GitHub actions, and continuous-integration workflows
without imposing unnecessary abstraction on packages with different build
requirements.

## Scope

The initial migration targets include the reference repositories:

- `compas`
- `compas_occ`
- `compas_cgal`

and the other packages declared by `compas_framework` as part of the
coordinated core installation:

- `compas_framework`
- `compas_gmsh`
- `compas_libigl`
- `compas_model`
- `compas_session`
- `compas_shapeop`
- `compas_viewer`

Host integrations (`compas_rhino`, `compas_ghpython`, and `compas_blender`)
should be assessed separately and scheduled as a later host-specific wave. The
host application runtimes and Python versions must not be forced into the
ordinary core-package matrix.

The initiative will assess and propose a consistent approach for:

- MkDocs documentation structure, configuration, API generation, examples,
  local preview, and deployment;
- PEP 517/518 packaging and project/tool configuration in `pyproject.toml`;
- `uv` for reproducible dependency installation, lock files, environments,
  development commands, and CI where appropriate;
- Ruff for linting and formatting, replacing Black and overlapping lint tools;
- current `compas-actions` releases and clearly defined shared-action
  responsibilities;
- modern GitHub Actions workflows for tests, typing, documentation, native
  builds, releases, and supported Python/platform matrices;
- the distinction between shared framework conventions and package-specific
  requirements, especially for native packages.

## Questions to resolve

1. Which repository conventions should be identical across COMPAS packages,
   and which should remain package-specific?
2. What is the canonical MkDocs configuration and documentation layout?
3. Which metadata and tool settings belong in `pyproject.toml`, and which
   configuration files should remain separate?
4. What role should `uv.lock`, dependency groups, and project environments
   have for pure-Python and native-extension repositories?
5. Which Ruff lint rules and formatting settings form the common baseline?
6. Which Black, Flake8, isort, or other overlapping configurations and
   workflows should be removed?
7. Which responsibilities belong in `compas-actions`, reusable workflows, or
   individual repository workflows?
8. What test, typing, documentation, build, release, and platform matrices are
   required for pure-Python, PythonOCC, and CGAL packages?
9. How should releases, trusted publishing, changelogs, and documentation
   deployment be secured and kept transparent?
10. In what order can repositories be migrated while keeping every step
    verifiable and reversible?

## Design principles

- Prefer a small, understandable standard over a configurable framework.
- Use current upstream conventions and supported tool features.
- Keep all important behavior visible in repository configuration.
- Share configuration only where it removes real duplication without hiding
  package-specific behavior.
- Do not add compatibility layers for obsolete tooling unless a current
  package requires them.
- Keep local development and CI commands aligned.
- Pin or constrain automation dependencies deliberately and document update
  policy.
- Treat native build, platform, and system-dependency requirements explicitly.
- Preserve release safety and artifact verification throughout migration.

## Initial deliverables

1. `inventory.md` deriving reference patterns from `compas`, `compas_occ`, and
   `compas_cgal` and comparing every initial migration target against them.
2. `proposal.md` defining the recommended repository standard, alternatives,
   migration effects, and verification strategy.
3. One Proposed ADR for every significant independent architectural choice.
4. `implementation-plan.md` with dependencies, repository ownership, rollout
   stages, and opportunities for parallel work.

## Verification target

Each migrated repository should have documented local commands equivalent to
CI and should pass its applicable:

- package and integration tests;
- Ruff lint and format checks;
- Pyright checks;
- MkDocs strict build and link/reference validation;
- source and wheel builds;
- native-extension imports and platform-specific tests;
- artifact metadata and installation smoke tests;
- release workflow validation without publishing.

## Non-goals for the initial architecture phase

- Modifying package source code or repository automation before approval.
- Requiring identical build workflows for pure-Python and native packages.
- Creating a general-purpose workflow generator.
- Making the three reference repositories identical where their runtime or
  native-build requirements differ.
- Migrating every COMPAS ecosystem or host-integration repository in the first
  implementation wave.
- Publishing packages, deploying documentation, or changing repository
  settings without explicit approval.

## Current status

Implementation is in final integration. ADRs 001–021 are Accepted. Phases 0–5
are complete through reviewed initiative branches and hosted draft-PR
evidence; Phase 6 remains open because the coordinated native-candidate
positive gate has not yet run with its protected credential boundary. No
initiative branch has been merged into a target/default branch and no package
or documentation site has been published.

The bounded `compas-actions` v2 prerequisite is independently reviewed Ready.
Commit `5c64e6e2b576a1232d28fed47d9478ca8eb63b2d` is pushed on
`initiative/repository-modernisation` and is the immutable consumer pin. Direct
local commands remain canonical; shared actions retain bounded repeated CI
mechanics without hiding repository-owned orchestration.

The current package checkpoints are carried by draft PRs and remain outside
`main`:

- core [PR 1539](https://github.com/compas-dev/compas/pull/1539) at
  `99b82a6673ff7d05c1c323c8921135c274993f11`;
- OCC [PR 32](https://github.com/compas-dev/compas_occ/pull/32) at
  `7fdf2ffb57d1de16308020e14ec626d79e65a034`;
- CGAL [PR 81](https://github.com/compas-dev/compas_cgal/pull/81) at
  `7537d58154f62f38c0b2d4118972d0a326f86c9b`;
- libigl [PR 47](https://github.com/compas-dev/compas_libigl/pull/47) at
  `710b2b6714839a203fc8a6c62c437c0f6735ba0e`;
- model [PR 68](https://github.com/BlockResearchGroup/compas_model/pull/68) at
  `83df4167f7ba1539ae205a837e0238afecc0a36b`;
- viewer [PR 232](https://github.com/compas-dev/compas_viewer/pull/232) at
  `cf5a5195bda840a511319d6b7201978af68c15e3`;
- Gmsh [PR 7](https://github.com/compas-dev/compas_gmsh/pull/7) at
  `c47af195bf04d0d2e874255bfe9c5f351beda672`;
- ShapeOp [PR 7](https://github.com/compas-dev/compas_shapeop/pull/7) at
  `930619a9aecd3e37515be9ce342ac20746ccf6d3`; and
- session [PR 1](https://github.com/BlockResearchGroup/compas_session/pull/1) at
  `e0bdd02aa8490248c6f2f36042651d8ebfc4442b`.

All cited package PR heads except the current CGAL head have complete green
hosted evidence. CGAL run `42224203204` completed with Linux and both macOS
wheel-smoke jobs passing, but Windows 3.12 and 3.14 failed installed
`--verifytypes` with `No py.typed file found` and zero symbols. A corrected
fresh successful run is required before CGAL artifact provenance can enter the
live manifest.

Accepted ADR 021 is implemented on framework draft
[PR 2](https://github.com/compas-dev/compas_framework/pull/2) at
`df97253f2797490bca3f027fc70d7f5154cadfe3`. Its schema, provenance,
security-negative, offline-installation, runtime/type integration, JUnit, and
public-release-order contracts pass locally and the ordinary credential-free
PR contracts pass on both push and pull-request events; release metadata also
passes. The live four-package manifest remains intentionally
absent until the superseding CGAL run supplies successful, unexpired artifact
evidence. The trusted hosted positive then still requires an explicitly
configured, protected GitHub App environment; ADR 021 does not authorize that
repository-owner configuration.

ShapeOp ADRs 022–023 are Proposed in the separate follow-up draft PR and are
not prerequisites for completing the accepted packaging modernization. They
cover the misleading correspondence flags and post-initialization point-buffer
lifecycle respectively; neither contract is implemented by the green ShapeOp
modernization checkpoint.

A larger future refactor may narrow `compas_gmsh` to COMPAS meshing
infrastructure rather than modeling features. `compas_fea2` is explicitly
outside that future initiative: it is only a known deferred external consumer
while its independent refactor proceeds. No `compas_fea2` migration,
compatibility layer, or coordinated source change is authorized here.
