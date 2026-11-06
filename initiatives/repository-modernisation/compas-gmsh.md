# `compas_gmsh` Modernisation Proposal

**Status:** Approved; implementation authorized but not yet complete

This package proposal refines the accepted repository-modernisation policy for
`compas_gmsh`. ADRs 014–016 are Accepted and authorize implementation of this
scope. Repository settings, publishing, deployment, and merging remain
separately approval-gated.

## Objective

Make `compas_gmsh` a reproducible, typed Python 3.12+ wrapper around the
official Gmsh Python SDK, with real meshing tests, strict documentation, and a
release that promotes one verified artifact set. Keep Gmsh provisioning
visible and avoid a second Python dependency authority.

## Current evidence

At baseline commit `c16725f12930659e85849640d912717bd0fe9475`:

- the only test imports `compas_gmsh` and prints its version;
- `gmsh`, `compas`, and directly imported NumPy are not bounded consistently;
- `requires-python`, classifiers, Ruff, and workflows disagree;
- Linux instructions split provisioning between pip and Conda, and
  `environment-linux.yml` installs both `gmsh` and `python-gmsh`;
- Pyright reports ten errors and the distribution has no `py.typed` marker;
- `Model.from_brep` leaks the `mkstemp` file descriptor and leaves its generated
  BRep file behind;
- project metadata names a nonexistent `LICENSE`, while `LICENSE.MIT` and a
  GPL-3.0 text coexist without an explicit project/dependency boundary;
- build and release workflows use moving shared-action tags, a token publisher,
  and matrices that do not match the package metadata; and
- MkDocs exists, but strict builds have real Griffe warnings and rely on
  network inventory resolution.

The official Gmsh project documents `pip install --upgrade gmsh` as the normal
Python SDK installation path. As of 2026-11-05, Gmsh 4.15.2 provides official
PyPI wheels for Windows x86-64, Linux x86-64, macOS x86-64, and macOS ARM64.
This evidence supports a uv/PyPI primary path; it does not prove arbitrary
platform support.

## Accepted decisions

| ADR | Decision | Status | Depends on |
|---|---|---|---|
| [014](decisions/014-gmsh-runtime-and-support.md) | Official PyPI SDK as the canonical runtime and an evidence-based support matrix | Accepted | 001, 002, 003, 009 |
| [015](decisions/015-gmsh-license-boundary.md) | MIT wrapper license separated from the GPL Gmsh dependency | Accepted | 002, 014 |
| [016](decisions/016-gmsh-verification-and-release.md) | Real-runtime gates, typed artifacts, temporary-file ownership, and exact artifact promotion | Accepted | 004–011, 014, 015 |

## Recommended package contract

Use one public installation contract:

```toml
requires-python = ">=3.12"
dependencies = [
  "compas>=3,<4",
  "gmsh>=4.13.1,<5",
  "numpy>=1.26",
]
```

The lower Gmsh bound is an implementation hypothesis that must pass the
minimum-dependency runtime job before release. If 4.13.1 cannot satisfy the
approved smoke contract, implementation must return with evidence and a new
bound proposal; it must not silently change the bound or weaken the test.

The committed `uv.lock` records the tested development environment. It is not
the published compatibility contract. `environment-linux.yml` is removed once
the uv/PyPI path passes on Linux; the repository must not install both the PyPI
SDK and Conda's Gmsh bindings into one environment. Conda can be documented as
an unsupported alternative provisioning route, but it is not a CI dependency
authority unless a demonstrated platform requirement produces a later ADR.

## Runtime and platform matrix

The blocking current-dependency matrix covers:

- CPython 3.12 and 3.14 on Linux x86-64;
- CPython 3.12 and 3.14 on Windows x86-64; and
- CPython 3.12 and 3.14 on macOS ARM64.

Run Python 3.12 minimum-dependency jobs with the declared lower bounds on all
three verified OS/architecture targets. This separates SDK availability from
the current-lock jobs instead of inferring cross-platform compatibility from a
Linux result. Python 3.13 is inside the supported range but does not need a
duplicate blocking job: per ADR 009, the matrix exercises the minimum and
latest supported interpreters.

The public platform floor follows the official binary SDK contract:

- Windows 10 or newer on x86-64;
- Linux x86-64 with glibc 2.28 or newer; and
- macOS 12 or newer on ARM64.

Workflow evidence records the exact hosted runner labels, architectures, and
image releases; it does not use a generic `latest` label as the support
definition.

Add macOS x86-64 as a blocking target only when a dependable runner is
available and the official SDK wheel passes the same runtime contract. Until
then, documentation may identify macOS 10.15+ x86-64 as an upstream Gmsh
target, but `compas_gmsh` must not report it as framework-verified. Other
architectures or source-built Gmsh installations are best-effort, not
supported targets.

The matrix verifies `gmsh.initialize()` and `gmsh.finalize()` in addition to
import. Gmsh's GUI is not opened, and tests must remain headless.

## Verification contract

Replace the dummy test with a compact suite that exercises real public
behavior:

1. initialize and finalize a named model repeatedly without leaking global
   Gmsh state;
2. construct a simple planar model, generate a two-dimensional mesh, convert it
   to a COMPAS mesh, and assert nonempty vertices/faces and valid indices;
3. construct one OCC solid and generate a three-dimensional mesh with nonempty
   tetrahedral output;
4. exercise one boolean operation and assert resulting entity dimensions;
5. import a committed, read-only STEP fixture;
6. preserve `Model.from_brep(Brep)`, export through the core-supported
   `Brep.to_step` path into a scoped intermediate, and prove that the file and
   descriptor are released on success and failure;
7. cover option round-trips that are part of the public API; and
8. run a clean installed-wheel consumer from outside the source tree.

Tests own every generated path through `tmp_path` or `tmp_path_factory`.
Runtime code that needs an intermediate BRep owns a scoped temporary directory
and removes it after `gmsh.open` returns or raises. Committed fixtures are
read-only inputs. Mocks may isolate exceptional paths but do not replace the
real Gmsh smoke gates.

The ordinary Gmsh matrix does not acquire an implicit OCC dependency. A
separate Linux integration job installs `compas_occ` and verifies the real
`COMPAS Brep backed by compas_occ -> Brep.to_step -> Model.from_brep` path.
Focused unit tests may use a small duck-typed exporter to prove cleanup
failures. Requiring native BREP serialization instead of the core STEP
contract would be a new input-protocol decision and is outside this proposal.

## Typing and public API scope

Add `py.typed`, type every exported `compas_gmsh` function and method, and make
Pyright blocking for `src`, tests, and a strict installed-wheel consumer. Gmsh
does not need a repository-maintained full stub package. A narrow configuration
exception for the external generated `gmsh` module is acceptable; it must not
exclude `compas_gmsh` modules or turn public results into `Any`.

Typing cleanup may modernize annotations and remove inaccurate ignores, but it
does not authorize behavioral API redesign. Genuine CSG or lifecycle defects
found while typing require focused regression tests; broader model API changes
return to proposal rather than entering as incidental modernization.

## Documentation scope

Keep MkDocs and make `mkdocs build --strict` reproducible and blocking. Correct
site URLs and navigation, remove superseded RST residue, resolve all Griffe
warnings, and ensure the build does not depend on a live documentation
inventory. Installation documentation must show the uv/PyPI path first,
identify the exact supported platform matrix, explain the separate Gmsh GPL
license, and distinguish upstream Gmsh support from framework-verified support.

Examples should cover planar meshing, solid meshing, and deterministic cleanup.
They must write outputs to a user-selected or temporary directory. When package
docstrings or rendered signatures are touched, the implementation owner must
apply the repository-local `update-docstrings` skill and run its doctest, Ruff,
diff, and affected strict-MkDocs checks.

## Work packages

### G1 — Metadata and environment

- align Python classifiers and Ruff with Python 3.12+;
- declare `compas`, `gmsh`, and NumPy bounds;
- add PEP 735 development, test, and docs groups plus `uv.lock`;
- remove duplicated requirements and `environment-linux.yml` only after parity;
- retain thin repository-owned Invoke aliases over documented `uv run`
  commands, with no environment or Gmsh provisioning inside tasks.

### G2 — Runtime tests and lifecycle corrections

- replace the dummy test with the real-runtime contract above;
- make Gmsh global-state cleanup deterministic;
- repair BRep intermediate-file ownership and add success/failure regressions;
- keep all generated artifacts under pytest temporary directories.

### G3 — Blocking typing and documentation

- resolve the measured Pyright debt and add `py.typed`;
- add source and installed-artifact typing consumers;
- complete the strict MkDocs cleanup and installation/license guidance;
- verify public examples against the supported runtime.

### G4 — Workflows and artifacts

- keep OS/runtime provisioning and test commands visible in repository YAML;
- use immutable action pins, least-privilege permissions, concurrency, and
  temporary runner directories;
- run Ruff, format check, Pyright, strict docs, minimum/current runtime tests,
  and package checks as blocking jobs;
- build the pure-Python wheel and sdist once, inspect metadata and contents,
  install the exact wheel with dependencies in a clean environment, and run
  the installed runtime and typing consumers;
- pass the unchanged verified artifacts to trusted publishing and the GitHub
  release, then deploy documentation from the same verified release revision,
  only after repository settings are configured and publication is separately
  approved.

## Compatibility implications

- Python 3.9–3.11 leave the supported contract, matching COMPAS 3.
- COMPAS 2 and future COMPAS 4 are outside the declared range.
- Gmsh 5 is excluded until its API is reviewed and tested.
- the project remains MIT; installing it also installs a separately licensed
  GPL-2.0-or-later Gmsh runtime.
- users relying on Conda-only environment files move to the documented uv path
  or manage an external Gmsh environment themselves.
- no public `compas_gmsh` model method is removed or renamed by this proposal.

## Completion evidence

The package is modernized only when all accepted ADRs are implemented and:

- frozen uv sync, Ruff check/format, Pyright, pytest, and strict MkDocs pass;
- minimum and current Gmsh runtime jobs satisfy the same smoke contract;
- wheel and sdist metadata contain the approved Python, dependency, and license
  contracts plus `py.typed`;
- the exact wheel passes clean installed runtime and strict typing consumers;
- tests and workflows leave no generated files in the checkout;
- workflow YAML is independently reviewed for pinning, permissions, artifact
  identity, and publish isolation; and
- no merge, deployment, or publication has occurred without explicit approval.

## Sources

- [Gmsh stable manual: obtaining and installing Gmsh](https://gmsh.info/doc/texinfo/#Obtaining-Gmsh)
- [Official Gmsh PyPI distribution](https://pypi.org/project/gmsh/)
- [Gmsh downloads and platform requirements](https://gmsh.info/#Download)
