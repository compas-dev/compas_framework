# Repository Modernisation Implementation Plan

Status: approved; Phase 0 complete, Phase 2 independently reviewed Ready and
pushed, and Phase 1 locally Ready with hosted verification complete except for
`compas` and the explicitly deferred CGAL macOS Intel target

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
[baseline.md](baseline.md). Recoverable preservation remains an explicit gate
before later edits to the dirty `compas_framework` and `compas_session`
worktrees; the clean Phase 1 reference repositories are not blocked.

Record current tests, Ruff, formatter, Pyright, docs, source/wheel builds,
native imports, workflow behavior, supported matrices, and release settings for
all ten initial core repositories.
Measure the known Gmsh test gap, ShapeOp Python/ABI mismatch, libigl dependency
pinning, OCC package availability, model optional runtimes, and framework
integration/release-order constraints. Do not introduce a new blocking gate
before its failures are known.

Outputs: baseline report, exact migration file list, rollback point.

## Phase 1: correct and validate the three references

Status: locally Ready; hosted verification remains. Final local review is
recorded below. The current
`compas-actions` v2 consumer pin is
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

### Final local review state

- **`compas`: Ready locally.** The reviewed modernization checkpoint is
  `943d9fdc366bf4bc55a2942dad259d112b23ab6c` on
  `initiative/repository-modernisation`. A successful hosted run using the
  immutable shared-action pin remains required.
- **`compas_occ`: Ready, including hosted verification.** Commit `572fa1b5` on
  `initiative/typing-alignment` closes the modernization gates on top of the
  typing-alignment successor: tests, blocking Pyright, Ruff, strict docs,
  frozen lock, wheel/sdist build, and Twine checks pass locally. Draft PR 32
  passes release policy, strict docs, and the Linux, macOS, and Windows Conda
  test matrix with the pinned shared actions.
- **`compas_cgal`: Ready with bounded hosted evidence.** Modernization commit
  `d31ec0f` passes hosted Linux x86_64, Windows AMD64, and macOS ARM64 wheel
  builds, the sdist build, documentation, release-policy, and quality checks.
  macOS Intel remains explicitly deferred and unverified because a suitable
  hosted runner has not been available; this is not evidence that the target
  passes. The successor branch `initiative/typing-alignment` was created from
  `d31ec0f` so typing work can proceed without waiting for that runner.

Phase 1 is not complete. Local readiness must not be reported as hosted or
distributed migration completion.

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

Status: OCC is hosted-verified at commit `572fa1b5`; CGAL's hosted evidence at
commit `d31ec0f` covers Linux, Windows, macOS ARM, sdist, documentation, policy,
and quality. macOS Intel remains explicitly deferred and unverified because of
hosted-runner availability.

OCC's groups, uv lock, commands, Pyright/docs debt, workflows, and
PythonOCC-bounded matrix are verified locally and through draft PR 32. CGAL's dependency consolidation,
visible CMake/cibuildwheel workflows, and exact-artifact promotion flow are
locally verified. Hosted PR runs have proved the available CGAL native
wheel/sdist matrix except for macOS Intel; that target remains deferred rather
than treated as passing. Trusted-publishing configuration and any
publishing dry run remain explicitly approval-gated.

## Phase 4: pure and hybrid core repositories

In parallel where file ownership is independent:

- migrate `compas_session` to the pure uv profile and from Sphinx to MkDocs;
- migrate `compas_framework` ordinary checks to the pure profile and add a
  separate coordinated native integration/release-order job;
- after explicit approval of Proposed ADRs 014–016 in
  [`compas-gmsh.md`](compas-gmsh.md), establish meaningful `compas_gmsh`
  tests and its evidence-based external-runtime matrix; source implementation
  remains blocked until then;
- migrate `compas_model` while keeping optional Coal/OCC integration jobs
  separate and explicit;
- correct `compas_viewer` within the uv profile while preserving explicit
  Qt/OpenGL provisioning and headless tests.

## Phase 5: native core repositories

- `compas_libigl` is active in this phase as of 2026-11-05. Its
  `initiative/repository-modernisation` branch starts independently from
  `c3-upgrade` commit `70acf99`; the later typing branch is an integration
  successor and must not be duplicated into this mechanical modernization
  work.
- For libigl: replace the moving upstream `main` source with a reviewed
  immutable revision; record verified hashes for libigl, Eigen, and Clipper;
  reconcile Python dependency sources and commit `uv.lock`; preserve thin
  Invoke aliases over direct `uv run` commands; migrate Sphinx/RST to strict
  MkDocs/mkdocstrings Markdown; adopt immutable action pins and repository-owned
  native provisioning; verify all 13 native modules in every wheel and clean
  sdist; promote exact tested artifacts without rebuilding.
- Integrate the verified libigl modernization checkpoint into
  `initiative/typing-alignment` before making Pyright and typed-wheel checks
  blocking. Preserve the current Python 3.12+ and stable-ABI intent unless
  wheel evidence demonstrates a change requiring explicit approval.
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
2. Request independent review of configuration, security, and release flow.
3. Resolve findings and rerun every affected gate.
4. Publish contributor and maintainer documentation changes in the same
   repository commits as their configuration.
5. Record deviations from the standard with rationale.

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
