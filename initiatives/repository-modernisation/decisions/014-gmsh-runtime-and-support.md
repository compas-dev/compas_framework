# ADR 014: Gmsh Runtime Provisioning and Support Contract

**Status:** Accepted

## Context

`compas_gmsh` imports Gmsh as a required runtime. Its metadata currently lists
an unbounded `gmsh` dependency, while Linux instructions and
`environment-linux.yml` also install Conda's `gmsh` and `python-gmsh`
packages. These paths can place different bindings and native libraries in one
environment. The existing test never initializes Gmsh, so none of the claimed
Python or platform combinations is verified.

The Gmsh project documents its official PyPI package as the normal Python SDK
installation path and currently publishes binary SDK wheels for Windows
x86-64, Linux x86-64, macOS x86-64, and macOS ARM64. COMPAS 3 requires Python
3.12 or newer.

## Options

1. **Conda is authoritative.** It can provide system libraries, but adds a
   second Python dependency authority and is unnecessary on platforms covered
   by the official SDK wheels.
2. **Support interchangeable pip and Conda environments.** This is flexible,
   but doubles resolution and test obligations and makes failure provenance
   unclear.
3. **Use the official PyPI SDK as the canonical path.** Manage the Python
   project and Gmsh SDK together through uv, while treating externally managed
   runtimes as best-effort alternatives.

## Recommendation

Choose option 3. Use uv and the official PyPI `gmsh` distribution for local
development, CI, documentation examples, and installed-artifact tests. Remove
`environment-linux.yml` after parity is demonstrated. Never install the PyPI
and Conda Gmsh bindings into the same test environment.

Publish this compatibility contract:

- Python `>=3.12`, supporting 3.12 through 3.14 while blocking jobs exercise
  the minimum and latest interpreters;
- `compas>=3,<4`;
- `numpy>=1.26`, because `compas_gmsh` imports NumPy directly; and
- `gmsh>=4.13.1,<5`, verified at the lower bound and at the lock's current
  version.

The blocking current-runtime matrix covers Linux x86-64, Windows x86-64, and
macOS ARM64 on Python 3.12 and 3.14. Python 3.12 minimum-dependency jobs verify
the declared lower bounds on all three OS/architecture targets. Python 3.13 is
inside the supported range but does not duplicate the ADR 009 minimum/latest
matrix.

The public platform floors are Windows 10+ x86-64, Linux x86-64 with glibc
2.28+, and macOS 12+ ARM64. Workflow evidence records the exact hosted runner
labels, architectures, and image releases rather than treating a generic
`latest` label as a support definition. macOS 10.15+ x86-64 becomes a blocking
framework-verified target only when a dependable runner executes the same
contract. Until then it is documented as an upstream Gmsh platform, not a
verified `compas_gmsh` target. Other architectures and source-built SDKs are
best-effort.

Every runtime job must initialize and finalize Gmsh and generate a real mesh;
import success alone is insufficient. If the proposed lower Gmsh bound fails,
on any supported platform, return with evidence and revise this ADR rather
than weakening the smoke test.

## Consequences

One lock and provisioning path governs ordinary development. The repository no
longer promises Python 3.9–3.11, COMPAS 2, Gmsh 5, or untested platforms. Gmsh
remains an external binary runtime even though uv installs its official SDK
wheel; repository workflows keep that provisioning visible. Conda users can
manage a compatible external environment, but that path is not the release
authority.

## Affected files

`pyproject.toml`, `uv.lock`, `environment-linux.yml`, `tasks.py`, installation
documentation, runtime tests, and build/release workflows.

## Dependencies

ADRs 001, 002, 003, and 009.
