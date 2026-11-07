# Repository Modernisation Proposal

Status: approved

This proposal defines a repository standard for the initial core scope:
`compas`, `compas_occ`, `compas_cgal`, `compas_framework`, `compas_gmsh`,
`compas_libigl`, `compas_model`, `compas_session`, `compas_shapeop`, and
`compas_viewer`. The first three provide the initial evidence and profile
examples, and also receive focused corrective work. Host repositories
`compas_rhino`, `compas_ghpython`, and `compas_blender` form a later wave.
This proposal changes no package, workflow, or repository setting. Accepted
ADRs are the implementation authority; repository settings, publishing,
deployment, and merging remain separately approval-gated.

Accepted ADR 021 records the separately discovered cross-repository candidate
artifact and credential boundary. Accepted ADR 013 requires an exact candidate
gate, while ADR 021 selects authenticated hosted candidate artifacts and their
provenance contract.

## Recommendation

Adopt one visible repository policy with three execution profiles, rather than
one configurable template:

- **Python profile (`compas`)**: uv provisions the project and all Python
  development dependencies.
- **Conda-runtime profile (`compas_occ`)**: Conda provisions PythonOCC and the
  compatible Python runtime; uv manages and runs the Python project inside that
  environment.
- **Native-wheel profile (`compas_cgal`)**: uv manages Python dependencies and
  local commands; repository-owned CMake/cibuildwheel jobs provision and build
  native artifacts on each platform.

Initial classification extends these patterns as follows:

- pure uv: `compas`, `compas_session`, and `compas_framework`, with a separate
  framework integration job for coordinated native packages;
- external-runtime hybrid: `compas_occ`, `compas_gmsh`, and `compas_model`
  where optional Coal/OCC features are tested;
- native wheels: `compas_cgal`, `compas_libigl`, and `compas_shapeop`;
- Python/GUI runtime: `compas_viewer`, using the uv profile with explicit
  Qt/OpenGL provisioning and headless-test settings.

The profiles share project metadata conventions, dependency groups, Ruff,
Pyright, MkDocs, workflow stages, release governance, permissions, and artifact
verification. Native provisioning and build commands stay explicit in each
repository.

## Canonical repository contract

### Project configuration

`pyproject.toml` is the source of truth for:

- PEP 621 project metadata and Python compatibility;
- build-system requirements and backend configuration;
- runtime dependencies and PEP 735 dependency groups;
- pytest, Ruff, Pyright, cibuildwheel, and versioning configuration where those
  tools support `pyproject.toml`.

Keep `mkdocs.yml`, workflow YAML, CMake files, and minimal system-provisioning
files separate because they describe different tools or platform resources.
Remove duplicated Python dependency lists only after their consumers use the
new groups.

### Environments and commands

Commit a current `uv.lock` for each migration target and use `uv sync --frozen`
in ordinary CI. The lock represents the tested development environment, not
the package's installation compatibility contract; `[project.dependencies]`
and `requires-python` remain that contract.

Canonical commands are direct and documented:

```text
uv sync --frozen --group dev --group docs
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
uv run mkdocs build --strict
uv build
```

OCC runs them after activating its minimal Conda environment. CGAL adds an
explicit editable/native build step and uses cibuildwheel for distributable
artifacts. Do not require Invoke or a generated command wrapper. Thin
repository-owned Invoke conveniences may remain and normally run as
`uv run invoke <task>`, but direct tool commands remain authoritative and
documented. Tasks may sequence commands; they must not own environment,
dependency, system, or native provisioning. Broader Invoke removal requires a
coordinated team decision.

### Ruff

Ruff is the only Python linter, import sorter, and formatter. Remove Black,
isort, Flake8, and obsolete configuration once Ruff covers their active role.
CI uses non-mutating `ruff check .` and `ruff format --check .`; local fix
commands are separately documented. Start from one conservative shared rule
baseline and add package-specific exclusions only with comments.

### Documentation

Use MkDocs Material and mkdocstrings, Markdown content, explicit navigation,
correct site/repository URLs, and inventories for cross-package references.
Every PR runs `mkdocs build --strict`. Release deployment uses the shared docs
action and Mike where versioned documentation is required. Remove superseded
Sphinx/RST residue after confirming it is not linked.

### Workflows and shared actions

Keep workflow orchestration visible in each repository. Shared actions should
perform bounded mechanics such as uv setup, release detection, PR validation,
artifact download/verification, GitHub release creation, and MkDocs deployment.
They should not hide package test commands, native toolchains, matrices, or
artifact build logic.

Use the same semantic workflow set where applicable:

- `build.yml`: lint, format, type, docs, tests, package build;
- `pr-checks.yml`: changelog/release-policy checks;
- `prepare-release.yml`: release pull request;
- `release.yml`: validate, build once, test artifacts, publish, release, docs;
- optional focused workflows such as coverage.

### Releases and security

Use release pull requests and one version/changelog authority. Build artifacts
once in the release run, test the exact files, then pass those files unchanged
to trusted publishing and the GitHub release. Never rebuild for publication.
Use explicit least-privilege job permissions, protected GitHub environments,
PyPI trusted publishing, concurrency controls, and immutable action commit
pins with automated update PRs.

### Support matrices

Project metadata is authoritative. Test the minimum and latest supported Python
versions plus any intermediate versions justified by user support. OCC's
matrix is bounded by available PythonOCC builds. CGAL's artifact matrix is
bounded by supported cibuildwheel platforms and its stable-ABI policy. Matrix
differences are explicit repository data, not options hidden in a generic
workflow.

### Quality-gate adoption

New checks must ultimately be blocking, but a migration may use an explicit,
time-bounded baseline phase. Measure existing failures, fix them in scope, and
then enable the gate. Do not suppress broad paths, silently ignore failures, or
claim completion while a target gate is non-blocking.

## Alternatives considered

### Copy `compas` into every repository

Simple initially, but incorrect for Conda-only PythonOCC and CGAL native wheel
builds. It would hide or discard real provisioning and artifact requirements.

### One highly parameterized reusable workflow

Reduces YAML lines but moves important package behavior into remote inputs and
conditionals. Native failures become harder to reproduce locally. Prefer
shared bounded actions and visible repository orchestration.

### Keep Pixi or Conda as the universal manager

Both can provision more system software than uv, but they add a second Python
dependency authority to repositories that do not need it. Retain Conda only
where it provides PythonOCC; retain explicit native tooling for CGAL.

### Do not commit library lock files

This maximizes resolver freshness but prevents exact local/CI reproduction.
The proposed lock is explicitly a tested development snapshot; package
compatibility continues to be validated through declared bounds and dedicated
resolution jobs.

### Keep Invoke as the authoritative command API

It offers short names, but duplicates tool commands and couples workflows to a
Python task layer. Direct uv/tool commands are clearer and portable, so Invoke
is not the authority. This does not reject thin repository-owned convenience
tasks that only sequence the documented direct commands.

## Package-specific migration effects

### `compas`

- Remove obsolete Black configuration.
- Make lint/format checks non-mutating and cover agreed repository paths.
- Add and document the uv development lock/workflow.
- Align classifiers and CI matrix; make docs strict.
- Pin actions immutably without changing release semantics.

### `compas_occ`

- Reduce `environment.yml` to accurate Conda runtime provisioning and align
  its Python/COMPAS constraints.
- Add uv dependency groups/lock and Pyright configuration.
- Migrate legacy build/docs/PR/release workflows to current release governance
  while retaining Conda provisioning.
- Enable strict docs and trusted publishing only after repository/environment
  prerequisites are verified.

### `compas_cgal`

- Replace stale lock and competing Python dependency authorities with
  pyproject groups plus a current uv lock.
- Preserve explicit CMake, compiler, editable rebuild, cibuildwheel, stable-ABI,
  sdist, and multi-platform behavior.
- Build release artifacts once and reuse them for testing/publication.
- Remove obsolete requirement/Pixi/Conda/RST paths only after parity checks.

### Other initial core repositories

- `compas_libigl`, `compas_session`, and `compas_shapeop` require actual
  Sphinx-to-MkDocs content/configuration migration, not only standardization.
- `compas_libigl` must replace unpinned FetchContent tracking of an upstream
  main branch with a reviewed immutable version before claiming reproducible
  native artifacts.
- `compas_shapeop` must resolve its Python-support and native-ABI inconsistency
  before its metadata and wheel matrix can be aligned. The approved package
  proposal and Accepted ADRs 017–019 are in
  [`shapeop-modernisation-proposal.md`](shapeop-modernisation-proposal.md).
  Newly exposed public correspondence-flag and point-buffer lifecycle changes
  remain blocked on Proposed ADRs 022–023.
- `compas_gmsh` needs a meaningful test baseline and evidence-based support
  matrix before workflow modernization can make tests authoritative. The
  approved package proposal and Accepted ADRs 014–016 are in
  [`compas-gmsh.md`](compas-gmsh.md), and implementation may proceed within
  their boundaries.
- `compas_model` must keep optional Coal/OCC runtime provisioning explicit;
  those integrations do not belong in its ordinary pure-Python job.
- `compas_framework` keeps ordinary pure-Python checks separate from a
  coordinated native-package integration/release-order job. Its incompatible
  COMPAS 2 host extras and root-lock conflict are resolved by Accepted
  [ADR 020](decisions/020-framework-host-extras.md) before the ordinary
  modernization patch is committed.
- `compas_viewer` keeps its current modular actions and uv profile, while
  removing Black residue, temporary COMPAS branch installation, mutating lint,
  and non-strict docs; Qt/OpenGL provisioning stays explicit.

### Host integrations

`compas_rhino`, `compas_ghpython`, and `compas_blender` are excluded from the
initial implementation wave. Their host runtimes require separate evidence and
architecture after the core standard is proven.

## Verification

For each repository:

1. create a clean environment from the documented frozen inputs;
2. run Ruff check/format, Pyright, tests, and strict MkDocs locally and in CI;
3. build sdist and wheels;
4. inspect artifact metadata and install artifacts into clean environments;
5. run package/native import smoke tests from outside the source tree;
6. for CGAL, test each produced wheel platform and the sdist build path;
7. validate release jobs without publishing;
8. confirm workflow permissions and pins mechanically;
9. verify local commands and CI invoke the same underlying operations.

## Documentation deliverables

- one concise contributor setup and command reference per profile;
- a release-maintainer guide covering release PRs and recovery;
- native prerequisites and editable rebuild instructions for CGAL;
- Conda/uv boundary explanation for OCC;
- shared-action input/output and security documentation.

## Approval boundary

Implementation may proceed only under Accepted ADRs. Gmsh ADRs 014–016 and
ShapeOp ADRs 017–019 authorize their scoped source work. Proposed ShapeOp ADRs
022–023 do not authorize the corresponding public-contract changes.
Repository settings, trusted-publisher configuration, deployment, publishing,
merging, and removal of active environment paths require explicit execution
approval in their implementation phase.
