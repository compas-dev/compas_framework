# Repository Modernisation Inventory

## Scope

This inventory compares `compas`, `compas_occ`, and `compas_cgal` using their
checked-in configuration, documentation, tasks, and GitHub workflows. No
package or automation files were modified.

## Executive summary

All three reference repositories already use MkDocs, PEP 517/621-style
`pyproject.toml` configuration, and Ruff. The initiative is therefore primarily
about completing and aligning earlier migrations.

- `compas` is the strongest general baseline: MkDocs Material, consolidated
  metadata, Ruff, uv-backed CI, modular `compas-actions@v1`, release pull
  requests, and trusted PyPI publishing.
- `compas_occ` has modern package/docs configuration but legacy CI and release
  workflows. Its Conda-only `pythonocc-core` dependency prevents a uv-only
  environment model.
- `compas_cgal` has strong native-build configuration but several competing
  dependency/task systems. Its checked-in `uv.lock` is stale. cibuildwheel,
  CMake, compilers, and platform SDKs remain essential.

The evidence supports one common policy with three explicit profiles:

1. pure Python with uv;
2. Conda-provisioned runtime plus uv-managed Python project;
3. native wheel and source-distribution builds.

## Comparison

| Concern | `compas` | `compas_occ` | `compas_cgal` |
|---|---|---|---|
| Docs | MkDocs Material + mkdocstrings | MkDocs Material + mkdocstrings + Mike | MkDocs Material + mkdocstrings + Mike |
| Packaging | setuptools, PEP 621 | setuptools, PEP 621 | scikit-build-core + nanobind, PEP 621 |
| Python baseline | `>=3.12`; CI 3.12–3.14 | `>=3.9`; CI 3.10–3.12 | `>=3.12`; stable ABI cp312 |
| Lint/format | Ruff; obsolete Black table remains | Ruff | Ruff |
| Typing | Pyright configured | no Pyright configuration/task | Pyright configured |
| Environment | uv in CI; local docs use Conda/pip | Conda required for PythonOCC; no uv | Pixi + stale uv lock + Conda + requirements files |
| Shared actions | modular `compas-actions@v1` | legacy monolithic build action | legacy action plus bespoke native jobs |
| Publishing | trusted publishing | incomplete current publish path | trusted publishing, old release orchestration |
| Release model | release PR on main | tag-driven GitHub release | tag-driven duplicated wheel/sdist build |

## `compas`: baseline and corrections

### Strengths

- `pyproject.toml` contains PEP 621 metadata, setuptools, dependency extras,
  pytest, Ruff, Pyright, and versioning settings.
- `mkdocs.yml` and `docs/` use Material, mkdocstrings, explicit navigation,
  inventories, and MathJax.
- `.github/workflows/` separates build, coverage, documentation, PR checks,
  release preparation, and release.
- Workflows use modular `compas-dev/compas-actions/*@v1` and uv-backed setup.
- PyPI publication uses trusted publishing; release preparation is PR-based.

### Gaps not to copy

- An obsolete `[tool.black]` table remains although Ruff is the formatter.
- The shared lint task applies `ruff check --fix`; CI checks should not mutate
  the checkout.
- Ruff tasks scan only `src` and `tests`, omitting task files and executable
  docs examples.
- MkDocs CI is not strict.
- Project classifiers and the CI Python matrix disagree.
- uv is used in CI while contributor docs still describe Conda/pip.
- There is no committed `uv.lock`; the library lock policy is unresolved.
- Ruff/mkdocstrings line-length and effective lint settings are inconsistent.
- Actions use moving tags rather than immutable commit SHAs.

## `compas_occ`: hybrid environment

### Strengths

- `pyproject.toml` centralizes setuptools/PEP 621 metadata, plugin entry points,
  pytest, Ruff, versioning, and docs/dev/visualization extras.
- `mkdocs.yml` uses Material, mkdocstrings, inventories, and Mike.
- Ruff already replaces Black.

### Gaps

- Build uses legacy `compas-actions.build@v4` and an older Python matrix.
- Docs installation/deployment are manual and PRs do not validate docs.
- PR/release workflows use obsolete checkout/changelog/create-release actions.
- Release does not implement current artifact validation, trusted publishing,
  GitHub release, and versioned docs sequencing.
- Workflow permissions are not consistently explicit and minimal.
- Pyright has no repository configuration or task.
- Python requirements, classifiers, Ruff target, and CI coverage disagree.
- `environment.yml` has no Python pin and requests `compas>=2.4`, conflicting
  with the current `compas>=3,<4` project requirement.
- `site_url` points to the repository rather than the published docs site.

### Constraint

`pythonocc-core` is supplied through Conda. uv can manage Python project
dependencies inside that environment, but cannot be the sole runtime
provisioner. The Python/platform matrix must follow available PythonOCC builds.

## `compas_cgal`: native build

### Strengths

- `pyproject.toml` contains PEP 621, scikit-build-core/nanobind, pytest, Ruff,
  Pyright, cibuildwheel, versioning, and Pixi configuration.
- CMake requires C++20 and builds multiple native modules.
- cibuildwheel covers Linux, Windows, and macOS x86_64/arm64.
- The CPython 3.12 stable ABI and macOS deployment target are explicit.
- PyPI publication already uses trusted publishing.
- MkDocs Material, mkdocstrings, inventories, and Mike are configured.

### Gaps

- Dependencies are fragmented across `pyproject.toml`, Pixi/`pixi.lock`,
  `uv.lock`, `requirements*.txt`, and `environment.yml`.
- `uv.lock` is stale: it records Python `>=3.9` and COMPAS 2.x, while the
  project requires Python `>=3.12` and COMPAS 3.x.
- Pixi currently handles editable native rebuilds and build isolation more
  completely than uv.
- Build mixes Conda, a legacy action, and bespoke wheel/sdist jobs; build logic
  is duplicated in release.
- Docs install several redundant requirement sources and deploy manually.
- PR/release workflows use obsolete actions.
- Parallel obsolete RST documentation remains beside canonical Markdown.
- Development docs offer Conda, uv, and Pixi without one source of truth.

### Constraints

- uv does not provision compilers, CMake, SDKs, or every platform tool.
- Editable native development requires an explicit rebuild path.
- Build isolation and preinstalled build-backend behavior matter.
- Clean CMake builds download CGAL, Boost, and Eigen.
- Wheel migration must preserve platform coverage, stable ABI, artifact tests,
  and sdist validation.

## Shared workflow architecture

The current `compas` workflows provide a useful common sequence:

1. detect release PRs and avoid redundant CI;
2. provision the selected environment profile;
3. run non-mutating lint, format, typing, tests, docs, and build checks;
4. prepare a release PR from version/changelog policy;
5. build artifacts once and validate them;
6. publish through trusted publishing;
7. create the GitHub release;
8. deploy versioned documentation.

Before OCC and CGAL adopt it, `compas-actions@v1` must support their profiles or
allow explicit package jobs to participate without duplicating release policy.

## Additional core migration targets

### `compas_framework`

Profile: pure-Python metapackage with a separate cross-package/native
integration responsibility.

- PEP 621, MkDocs, Ruff, and Pyright are already configured.
- Obsolete Black configuration, Conda/pip contributor instructions, and legacy
  v4/v3 build/docs/publish actions remain.
- CI/release Python matrices conflict with the declared Python `>=3.12` range;
  the release matrix cannot currently install the project.
- The ordinary project can use uv, but framework integration must separately
  install and identify sibling/native backends and respect package release
  ordering.

### `compas_gmsh`

Profile: Python package with an externally supplied Gmsh runtime.

The current clean baseline is `c16725f12930659e85849640d912717bd0fe9475`.
The package-specific architecture is recorded in
[`compas-gmsh.md`](compas-gmsh.md); implementation is authorized by Accepted
ADRs 014–016 and remains incomplete.

- PEP 621, MkDocs, and Ruff exist; uv and Pyright do not.
- Python metadata, classifiers, Ruff target, and CI matrix disagree.
- Gmsh/COMPAS dependencies are unconstrained and Linux installation is split
  across pip, Conda, and an incomplete environment file.
- Tests currently verify only that a version exists; meaningful initialization
  and meshing smoke coverage is required before CI modernization is verifiable.
- Docs metadata/deployment, task code, PR checks, and token-based release
  workflows are legacy; obsolete RST examples coexist with Markdown.

### `compas_libigl`

Profile: native nanobind/cibuildwheel package.

- PEP 621/735, scikit-build-core, Ruff, and cibuildwheel are present.
- This repository still requires a real Sphinx/RST to MkDocs migration.
- Black remains in configuration and requirements; no Pyright configuration or
  uv lock exists.
- Python declarations range from 3.8/3.9/3.10 through the cp312 stable ABI.
- Native dependency sources overlap across pyproject groups, requirements,
  Conda, and tasks.
- libigl is fetched from the moving `main` branch, making clean builds
  non-reproducible.
- Build and release independently rebuild native artifacts; the release
  workflow uses obsolete orchestration despite trusted PyPI publishing.

### `compas_model`

Profile: pure-Python base with optional Coal/OCC integration.

- PEP 621, Python 3.12+, MkDocs, and Ruff are already present.
- uv is absent; a Conda environment currently makes optional native
  integrations part of the default setup.
- Pyright is installed but not configured as a repository gate.
- Docs contain stale metadata and an installation extra that does not exist.
- Base CI should use uv; optional native integrations should have an explicit
  separate job.
- Workflows are legacy and token-published. The repository is hosted outside
  `compas-dev`, so trusted-publisher and environment governance must be set up
  in its actual organization.

### `compas_session`

Profile: pure Python.

- Packaging is only partially consolidated: runtime/dev dependencies are
  dynamically read from requirements files.
- Documentation remains Sphinx/RST.
- Black and Ruff coexist; uv and Pyright are absent.
- Tasks contain nonexistent GHUser component paths, apparently template
  residue.
- All CI/docs/PR/release workflows use legacy actions and token publishing.
- An unrelated untracked source file exists locally and must be preserved
  during any mechanical migration.

### `compas_shapeop`

Profile: native scikit-build-core/nanobind/cibuildwheel package.

The current clean baseline is `9f57579`. An explicit import outside the
checkout with the required `compas3` interpreter fails because the package is
not installed there, so no local native baseline is claimed. The
package-specific architecture is recorded in
[`shapeop-modernisation-proposal.md`](shapeop-modernisation-proposal.md);
implementation is authorized by Accepted ADRs 017–019 but has not started.

- Runtime dependency metadata is missing from built-project configuration even
  though a requirements file declares COMPAS 2.x.
- Documentation remains Sphinx/RST; Black and Ruff coexist; uv/Pyright are
  absent.
- Python `>=3.9`, a cp312 stable ABI, cibuildwheel selection, CMake Python 3.8,
  and a single Python 3.10 CI job are mutually inconsistent. This blocks a
  correct wheel matrix.
- Native build/release jobs duplicate wheels and sdists, and GitHub releases
  can be created before artifacts succeed.
- Trusted publishing exists, but surrounding PR/docs/release actions are old.
- CMake/compiler/OpenMP provisioning and editable rebuild behavior must remain
  explicit.

### `compas_viewer`

Profile: pure Python with Qt/OpenGL system-library and headless-test needs.

- PEP 621, MkDocs, Ruff, Pyright, uv-backed modular v1 actions, release PRs,
  and trusted publishing already closely match the modern reference.
- Obsolete Black configuration remains and the shared lint task mutates CI via
  `ruff check --fix` while omitting format and type-check gates.
- CI hardcodes a development branch of COMPAS and project metadata still
  permits COMPAS 2.x.
- MkDocs builds are non-strict, release does not deploy docs, and local uv/lock
  policy is undocumented.
- Qt/OpenGL Linux libraries and headless execution must be represented as an
  explicit test profile rather than hidden in generic setup.

### Host integrations

The local `compas_rhino`, `compas_ghpython`, and `compas_blender` directories
are source directories rather than standalone Git repositories with their own
project/workflow/docs configuration. Their canonical repository ownership and
release units must be identified before the later host-specific wave can be
planned or migrated.

## Significant architecture questions

1. Whether uv is canonical and whether library development locks are committed.
2. How uv composes with Conda for OCC and native toolchains for CGAL.
3. Whether Invoke remains the local command facade or tools run directly.
4. The Ruff baseline, scanned paths, and separation of check/fix commands.
5. Strict MkDocs, versioning, inventories, and deployment conventions.
6. What belongs in `pyproject.toml` versus separate native/docs files.
7. The boundary between shared actions and visible repository workflows.
8. Release-PR semantics, version/changelog authority, and artifact reuse.
9. Action pinning, automated updates, permissions, and trusted publishing.
10. Python support and package-specific platform matrices.
11. How new gates handle existing typing or documentation-warning debt.

## Risks and conclusion

- Copying `compas` verbatim would obscure OCC and CGAL provisioning.
- Treating CGAL's stale lock as authoritative installs the wrong COMPAS major.
- Removing environment files before transferring their responsibilities makes
  native development incomplete.
- Release-PR migration changes maintainer practice and branch protection.
- Trusted publishing must be configured per PyPI project before token removal.
- Strict docs or Pyright need measured migrations where debt already exists.
- Artifacts should be built once, tested, and then published unchanged.

Use `compas` as the policy and pure-Python reference after correcting its known
inconsistencies. Keep OCC and CGAL provisioning explicit and package-owned.
