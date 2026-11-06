# Repository Modernisation Implementation Plan

Status: implementation in progress. Phases 0–3 are complete through reviewed
initiative branches and hosted draft-PR evidence. Phase 4 is active, Phase 5
has a hosted-verified libigl checkpoint, and Phase 6 remains pending. No
initiative changes have been merged into a target/default branch or published.

## Dependencies

All work depends on accepted ADRs. Phase 2 shared-action capability work was the
prerequisite for completing the reference workflow migration in Phase 1. The
bounded `compas-actions` v2 implementation is independently reviewed Ready and
pushed, so reference workflows use its immutable remotely resolvable commit.
Trusted-publisher and protected-environment setup requires repository-owner
access and explicit approval.

## Phase 0: record baselines

Status: complete. The measured results, exact Phase 1 debt manifests, migration
surfaces, rollback commits, and environmental limitations are recorded in
[baseline.md](baseline.md). The session and framework changes use isolated
worktrees, preserving the original local branches and the dirty framework
coordination worktree. The clean Phase 1 reference repositories are not
blocked.

Record current tests, Ruff, formatter, Pyright, docs, source/wheel builds,
native imports, workflow behavior, supported matrices, and release settings for
all ten initial core repositories.
Measure the known Gmsh test gap, ShapeOp Python/ABI mismatch, libigl dependency
pinning, OCC package availability, model optional runtimes, and framework
integration/release-order constraints. Do not introduce a new blocking gate
before its failures are known.

Outputs: baseline report, exact migration file list, rollback point.

## Phase 1: correct and validate the three references

Status: complete through local review and hosted draft-PR verification. The
current `compas-actions` v2 consumer pin is
`5c64e6e2b576a1232d28fed47d9478ca8eb63b2d`; it is pushed and remotely
resolvable.

1. Correct `compas` dependency groups/lock, Black residue, Ruff semantics,
   Python metadata, strict docs, direct commands, and workflow security.
2. Establish OCC's accurate minimal Conda boundary and measured Pyright/docs
   baseline without hiding PythonOCC availability constraints.
3. Replace CGAL's stale lock, document the authoritative native path, and add
   parity checks before removing competing dependency paths.
4. Use the reviewed Phase 2 bounded shared actions to finish the reference
   workflows and verify all three profile definitions through package, docs,
   artifact, and dry-run release gates.

This phase proves the profiles and fixes known reference defects. Direct local
commands remain the canonical developer and CI command interface. That decision
does not mean abandoning shared actions: bounded shared actions may implement
repeated CI mechanics while repository workflows keep orchestration,
provisioning, matrices, and the underlying direct commands visible. Thin
repository-owned Invoke conveniences may remain, normally run as
`uv run invoke <task>`, when they only sequence those commands. They must not
own environment, dependency, system, or native provisioning, and broader Invoke
removal requires a coordinated team decision.

### Reviewed and hosted-verified checkpoints

- **`compas`: Ready on the initiative successor.** The reviewed modernization
  checkpoint is `943d9fdc366bf4bc55a2942dad259d112b23ab6c`. Draft
  [PR 1539](https://github.com/compas-dev/compas/pull/1539) at
  `4973c5fcfc53f0217a5fca20d0765e74b30459e2` passes the full Linux, macOS,
  and Windows Python 3.12–3.14 matrix, minimum/current NumPy jobs, coverage,
  changelog, release-metadata, and package-build checks.
- **`compas_occ`: Ready on the initiative successor.** Modernization checkpoint
  `572fa1b5` is included in draft
  [PR 32](https://github.com/compas-dev/compas_occ/pull/32) at
  `5a4cf9701007266e517996181c8476488c4030d9`. Its strict docs,
  release-metadata, and Linux, macOS, and Windows PythonOCC test jobs pass.
- **`compas_cgal`: Ready on the initiative successor.** Modernization checkpoint
  `d31ec0f` is included in draft
  [PR 81](https://github.com/compas-dev/compas_cgal/pull/81) at
  `a46eecab71de5dfea6df7380d2eafb7185cc789a`. Quality, policy, sdist,
  Linux, Windows, macOS ARM64, and macOS Intel wheel and smoke jobs all pass.
  The earlier macOS Intel evidence gap is therefore closed.

This evidence proves the Phase 1 repository and workflow gates at the cited
heads. It is not evidence of a merge, published distribution, documentation
deployment, or repository-setting configuration.

## Phase 2: prepare shared actions

Status: implementation complete and independently reviewed Ready. The initial
local implementation commit is
`42216af0d21a53f0c234996b2fe664b1548af9eb`. The reviewed follow-up commit
`5c64e6e2b576a1232d28fed47d9478ca8eb63b2d` adds prepared Conda documentation
environments and is the current consumer pin. Both are on branch
`initiative/repository-modernisation`, based on rollback/start commit
`12ff286e`.

Audit `compas-actions@v1` against the accepted boundary. Add only missing
bounded mechanics required by the profiles, with contract tests and examples:

- uv setup/frozen sync;
- release detection and PR checks;
- artifact download and verification;
- GitHub release and MkDocs/Mike deployment;
- support for callers that provision Conda or build native artifacts in their
  own visible jobs.

Do not create a universal workflow generator.

The tested `compas-actions` v2 contract unblocks the workflow portion of Phase
1. Both commits have been pushed to `initiative/repository-modernisation`, and
reference workflows use the current immutable SHA. The action is not tagged or
published as a release. No consumer workflow may be treated as verified until
its hosted run succeeds with that SHA.

## Phase 3: finish OCC and CGAL workflow migration

Status: complete through hosted draft-PR verification. OCC's modernization
checkpoint `572fa1b5` is covered by the fully green PR 32 successor head, and
CGAL's `d31ec0f` checkpoint is covered by the fully green PR 81 successor head,
including macOS Intel.

OCC's groups, uv lock, commands, Pyright/docs debt, workflows, and
PythonOCC-bounded matrix are verified locally and through draft PR 32. CGAL's
dependency consolidation, visible CMake/cibuildwheel workflows, exact-artifact
promotion, full native wheel matrix, and sdist path are verified locally and
through draft PR 81. Trusted-publisher and protected-environment settings, any
publication, and merges remain explicitly outside this evidence.

## Phase 4: pure and hybrid core repositories

Status: in progress. `compas_session` is reviewed, committed, and pushed;
`compas_framework` has a reviewed but uncommitted ordinary modernization patch;
Gmsh has approval-ready package ADRs; model and viewer remain pending.

In parallel where file ownership is independent:

- `compas_session`: modernization commit
  `10b2d6332eed42b16b57c4d95c7866844cfb90bd` is pushed on
  `initiative/repository-modernisation`. Its frozen lock, 16-test suite,
  Pyright, Ruff, doctest, strict MkDocs, wheel/sdist verification, Twine, and
  isolated installed-wheel import passed locally and independent review found
  no remaining code findings. Protected environments, trusted publishing,
  required checks, and Pages/Mike settings remain owner configuration work;
- migrate `compas_framework` ordinary checks to the pure profile and add a
  separate coordinated native integration/release-order job; the ordinary
  patch is independently reviewed and locally green. Accepted
  [ADR 020](decisions/020-framework-host-extras.md) now authorizes removal of
  its incompatible COMPAS 2 host extras and regeneration of the root lock; the
  patch remains uncommitted pending that implementation. The separate native
  integration contract is authorized by Accepted Geometry ADRs 022–023 and
  Typing ADRs 015–017, but its cross-repository artifact provenance and
  credential mechanism remains blocked on Proposed
  [ADR 021](decisions/021-cross-repository-candidate-artifacts.md);
- after explicit approval of Proposed ADRs 014–016 in
  [`compas-gmsh.md`](compas-gmsh.md), establish meaningful `compas_gmsh`
  tests and its evidence-based external-runtime matrix; source implementation
  remains blocked until then;
- migrate `compas_model` while keeping optional Coal/OCC integration jobs
  separate and explicit;
- correct `compas_viewer` within the uv profile while preserving explicit
  Qt/OpenGL provisioning and headless tests.

## Phase 5: native core repositories

Status: in progress. The libigl modernization/typing successor is hosted
verified; ShapeOp source work remains blocked on Proposed ADRs 017–019.

- `compas_libigl` entered this phase on an independent
  `initiative/repository-modernisation` branch from `c3-upgrade` commit
  `70acf99`; the later typing branch is its integration successor. Draft
  [PR 47](https://github.com/compas-dev/compas_libigl/pull/47) at
  `86e3f1e0e02d6dc7cf9ad8049ac57c4c7d801877` passes policy, quality,
  typing, sdist, wheel typing, and Linux, Windows, and macOS ARM64 wheel/smoke
  checks. This closes the modernization artifact evidence at that checkpoint;
  the newly Accepted native-stub completeness work belongs to typing ADR 017.
- That checkpoint uses reviewed immutable libigl, Eigen, and Clipper sources,
  reconciled dependency metadata and lock, thin Invoke aliases, strict MkDocs,
  immutable workflow pins, repository-owned native provisioning, native-module
  wheel and clean-sdist verification, and exact tested-artifact promotion.
- The modernization checkpoint is integrated into
  `initiative/typing-alignment`; Pyright and typed-wheel checks are blocking at
  the cited PR head. Preserve the current Python 3.12+ and stable-ABI intent
  unless later wheel evidence demonstrates a change requiring explicit
  approval.
- After explicit approval of Proposed ADRs 017–019 in
  [`shapeop-modernisation-proposal.md`](shapeop-modernisation-proposal.md),
  resolve ShapeOp's Python-support/native-ABI inconsistency, migrate its Sphinx
  docs to MkDocs, then modernize and verify its wheel matrix; source
  implementation remains blocked until then.
- Reuse the native-wheel policy proven by CGAL, but keep each repository's
  build commands and dependency versions visible.

## Phase 6: integration and documentation

1. Run clean-environment verification for all ten core repositories and every
   profile.
2. Verify that Ruff and Pyright enumerate every executable Python example, and
   modernize stale framework idioms exposed by those gates.
3. Request independent review of configuration, security, and release flow.
4. Resolve findings and rerun every affected gate.
5. Publish contributor and maintainer documentation changes in the same
   repository commits as their configuration.
6. Record deviations from the standard with rationale.

## Later wave: host integrations

Inventory `compas_rhino`, `compas_ghpython`, and `compas_blender` after core
completion. Produce host-specific ADRs where the proven core profiles do not
fit. Do not infer host-runtime behavior from ordinary Python CI.

## Parallel work

During the corrected Phase 1/Phase 2 sequence:

- shared-action v2 contract work and reference-repository non-workflow cleanup
  can proceed in parallel;
- CGAL dependency inventory/parity tests can proceed independently;
- independent pure/hybrid repository audits and Sphinx-to-MkDocs content work
  can proceed in parallel with separate owners;
- libigl dependency pinning and ShapeOp ABI evidence gathering are independent;
- docs cleanup and Python-matrix evidence gathering are package-local;
- reference workflow completion waits for required shared-action v2
  capabilities;
- repository-setting changes remain serial and owner-controlled.

## Ownership boundaries

- one implementer owns each package repository;
- one implementer owns `compas-actions`;
- no two agents edit the same workflow or dependency file concurrently;
- a reviewer owns final cross-repository validation;
- a documenter verifies contributor/release documentation against commands.

## Completion criteria

The initial wave is complete only when all ten core repositories pass their
accepted blocking gates, artifact tests, strict docs, and dry-run release
validation; obsolete active paths are removed; framework integration verifies
the coordinated package set and release order; documentation matches CI; and
no publish, deployment, or merge has occurred without explicit approval.
