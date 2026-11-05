# ADR 019: ShapeOp Distribution and Quality Contract

**Status:** Proposed

## Context

The `compas_shapeop` Python wrapper imports NumPy and COMPAS, but project
metadata declares neither runtime dependency. Requirements files still target
COMPAS 2 and mix runtime, build, test, documentation, and release tools. The
repository has one checkout-based solver smoke test, no Pyright contract, no
PEP 561 marker, and Sphinx/RST documentation.

For a native package, source-tree tests alone cannot prove that a wheel contains
the extension, dependency metadata, typing files, licenses, or the sources
needed to rebuild an sdist. The current release workflow also creates or
rebuilds artifacts through separate paths rather than promoting one tested
set.

## Options

1. **Preserve requirements files and checkout-based tests.** This minimizes
   migration work but leaves package metadata and published artifacts
   unverified.
2. **Declare dependencies but treat native artifact and typing checks as
   advisory.** This improves installation while leaving the distribution
   contract unenforced.
3. **Make `pyproject.toml` authoritative and require source plus installed-
   artifact gates.** Verify public behavior, native import, metadata, typing,
   documentation, wheels, and sdist before considering the migration complete.

## Recommendation

Choose option 3.

- Declare direct runtime dependencies `compas>=3,<4` and `numpy>=1.26` in
  project metadata. Keep CMake, Ninja, nanobind, scikit-build-core,
  cibuildwheel, test, type, and documentation tools in explicit PEP 735 groups,
  with a committed uv lock for development and CI.
- Remove superseded requirements files only after every consumer has moved to
  the authoritative metadata and parity is proven.
- Keep `_shapeop` private. The supported import paths remain
  `compas_shapeop.shapeop.Solver` and
  `compas_shapeop.meshsolver.MeshSolver`; this modernization does not add
  root-level re-exports, a plugin, or a second low-level public API.
- Add behavioral tests for accepted point-array shape, finite output,
  constraint and force effects, `fix_vertex` target proximity within the
  documented finite-weight tolerance, and numerical repeatability within
  documented tolerances. Preserve and test only invalid-input failures that
  the existing wrappers or native binding already expose; do not add broad
  runtime validation or promise new exception semantics as part of this
  modernization. Tests must use temporary paths for generated files and
  artifacts.
- Test installed wheels and the sdist-built wheel from outside the checkout.
  Assert that the imported package and native extension originate in the
  isolated environment.
- Mark the distribution with `py.typed` and provide a private `_shapeop.pyi`
  matching the nanobind surface used by the wrappers. Run strict Pyright over
  source and tests and against representative calls in a clean installed-wheel
  consumer. The private stub supports verification; it does not make
  `_shapeop` public.
- Migrate to MkDocs/mkdocstrings Markdown under ADR 006. Apply the
  repository-local `update-docstrings` skill to touched public docstrings and
  keep documentation-only edits behavior-neutral. Document numerical
  methodology, tolerance/iteration semantics, mutation and memory ownership,
  native build prerequisites, known limitations, and primary ShapeOp sources.
  Record those primary sources in top-level `REFERENCES.md`, keep claims scoped
  to verified wrapper behavior, and include both package license texts from the
  documentation license page.
- Use one release artifact set: build once, inspect and install the exact
  files, then pass them unchanged to trusted publishing and the GitHub release.
  Publishing and repository-setting changes remain separately approval-gated.

## Consequences

Normal installation receives every direct Python dependency. Contributor and
CI environments become reproducible. The native extension remains an
implementation detail while the typed Python wrapper is verifiable both from
source and from the actual wheel.

The migration is larger than a metadata-only update: existing typing and
documentation debt must be resolved before Pyright and strict MkDocs become
blocking. This work must preserve solver behavior unless a separate public API
decision is approved.

## Verification

- Validate the frozen lock and clean dependency-group sync.
- Run Ruff check/format, strict Pyright, source tests, focused doctests, and
  strict MkDocs.
- Inspect wheel and sdist metadata for Python/runtime requirements, licenses,
  `py.typed`, `_shapeop.pyi`, and the native module.
- Install exact artifacts into clean environments outside the checkout and run
  public solver and strict typing consumers.
- Verify workflow permissions, immutable action pins, temporary artifact
  locations, and unchanged artifact promotion.
- Obtain independent code and documentation review before reporting the
  package Ready.

## Dependencies

ADRs 002, 003, 004, 005, 006, 008, 010, 011, 013, 017, and 018.
