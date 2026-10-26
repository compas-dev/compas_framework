# COMPAS Framework Agent Guide

## Scope and Principles

These instructions apply to the entire repository.

- Treat this repository as the integration and release layer for `compas`,
  `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_gmsh`,
  `compas_viewer`, `compas_model`, `compas_shapeop`, and `compas_session`.
  Treat `compas_rhino`, `compas_ghpython`, and `compas_blender` as optional
  host integrations.
- Keep package-specific implementations in their owning repositories. Add code here only when it tests, documents, benchmarks, or demonstrates interactions across package boundaries.
- Preserve unrelated working-tree changes and keep patches focused.
- Prefer the simplest implementation that expresses the required contract. Avoid speculative abstractions and compatibility layers.
- Update integration tests, documentation, serialization fixtures, and change notes together when changing a shared contract.
- Record deferred design work in `TODO.md`; do not mix it into unrelated work.

## Python and Typing

- Support Python 3.12 and newer, as declared in `pyproject.toml`.
- Use modern Python syntax, zero-argument `super()`, PEP 604 unions, built-in generics, and `Self` for subclass-preserving returns.
- Annotate the values accepted by the runtime API. Do not add conversions or validation merely to satisfy a type checker.
- Prefer precise structural types and protocols over `Any`, concrete runtime type checks, or casts.
- Use `TYPE_CHECKING` for dependencies imported only for annotations, especially optional or heavy geometry and GUI dependencies.
- Do not hide integration problems behind broad exception handling or optional imports. Skip tests only for explicitly optional system capabilities.

## Framework Integration Contracts

- Exercise plugins through public COMPAS plugin APIs. Do not call backend implementation modules directly merely to make an integration test pass.
- Test discovery with the full framework and with meaningful subsets where graceful absence is part of the contract.
- Data roundtrips must verify semantic equivalence, not only successful serialization. Cover dtype, shape, topology, orientation, attributes, precision, and object type where relevant.
- Keep reusable fixtures small, deterministic, and human-readable. Store large generated or benchmark data outside Git.
- Performance tests must separate setup from the measured operation, include a correctness assertion, and use stable thresholds or comparative baselines.
- Examples should demonstrate workflows spanning at least two framework packages. Package-local examples belong in the owning package.
- Keep GUI tests headless where possible. Mark tests requiring a display, native library, or unusually long runtime explicitly.

## Documentation and Public API

- Write MkDocs/mkdocstrings-compatible NumPy-style docstrings using Markdown.
- Use backticks for code and identifiers, Markdown links and footnotes, and `$...$` or `$$...$$` for mathematics. Do not introduce Sphinx roles or directives.
- Keep executable examples valid as doctests and identify which framework package owns each object or operation.
- Document supported package combinations and native prerequisites explicitly.
- The `compas_framework` package is release metadata and integration support; do not re-export APIs from constituent packages.

## Tests and Validation

- Run the smallest relevant tests first, then broaden validation in proportion to risk.
- Use the commands in `.github/CONTRIBUTING.md`: `invoke test`,
  `invoke check`, `invoke typecheck`, `invoke docs`, and `invoke format`.
- Always run `git diff --check` for changed patches.
- Mark integration, roundtrip, performance, GUI, and native-backend tests so they can be selected independently.
- Test public behavior rather than implementation metadata. Prefer capability checks over platform-name checks.
- Build relevant MkDocs pages when changes affect examples, API documentation, signatures, or navigation.
