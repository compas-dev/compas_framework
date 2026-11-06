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

Implementation is in progress. ADRs 001–013 are Accepted. Phases 0–3 are
complete through reviewed initiative branches and hosted draft-PR evidence;
the initial migration wave and final integration are not complete. The bounded
`compas-actions` v2 prerequisite is independently reviewed Ready. Its initial
commit is
`42216af0d21a53f0c234996b2fe664b1548af9eb`; reviewed follow-up commit
`5c64e6e2b576a1232d28fed47d9478ca8eb63b2d` adds prepared Conda documentation
environments and is the current consumer pin. Both commits are on branch
`initiative/repository-modernisation` and have been pushed. The follow-up SHA
is the current remotely resolvable action pin.

The three reference checkpoints are covered by fully green hosted successor
draft PRs: core PR 1539 at
`4973c5fcfc53f0217a5fca20d0765e74b30459e2`, OCC PR 32 at
`5a4cf9701007266e517996181c8476488c4030d9`, and CGAL PR 81 at
`a46eecab71de5dfea6df7380d2eafb7185cc789a`. CGAL's macOS Intel wheel and
smoke jobs now pass, closing the former runner gap. Direct local commands remain
canonical; shared actions retain bounded repeated CI mechanics without hiding
repository-owned orchestration.

Phase 4 is active. `compas_session` modernization commit
`10b2d6332eed42b16b57c4d95c7866844cfb90bd` is reviewed and pushed. The
ordinary `compas_framework` patch is independently reviewed, committed, and
pushed as `ae3b28e`; it implements Accepted ADR 020 and keeps candidate
publication structurally disabled. Its native integration contract is likewise
authorized by Accepted Geometry ADRs 022–023 and Typing ADRs 015–017, while
its cross-repository artifact provenance and credential boundary remains
blocked on Proposed ADR 021. Gmsh ADRs 014–016
and ShapeOp ADRs 017–019 remain Proposed. Model and viewer migration,
final cross-package integration, repository settings, publishing, deployment,
and merges remain pending or explicitly approval-gated.

`compas_libigl` joined the active modernization scope on 2026-11-05 from
`c3-upgrade` commit `70acf99`. Its successor draft PR 47 at
`86e3f1e0e02d6dc7cf9ad8049ac57c4c7d801877` now passes policy, quality,
typing, sdist, wheel-typing, and Linux, Windows, and macOS ARM64 wheel/smoke
checks. The additional native-stub truthfulness and completeness work discovered
later is tracked by Accepted Typing ADR 017 rather than being retroactively
claimed by this modernization checkpoint.
