---
name: update-docs
description: Update COMPAS repository documentation, navigation, tutorials, examples, API pages, license, or changelog coverage without changing runtime behavior.
---

# Update COMPAS documentation

Apply `AGENTS.md`, accepted documentation decisions, and the owning
repository's existing structure. Change only the documentation required by the
request; do not turn a focused edit into a full documentation rewrite.

## Requirements

- Preserve the repository's MkDocs navigation and established information
  architecture unless the approved task changes them.
- Keep examples as direct, step-by-step scripts. Introduce functions only when
  they prevent substantial repetition or clarify a reusable operation.
- Use high-level current APIs and replace obsolete idioms in touched examples.
- Keep public claims aligned with implemented, verified behavior and matching
  package versions. Label limitations and proposed work explicitly.
- Use `--8<-- "LICENSE"` and `--8<-- "CHANGELOG.md"` where the repository
  exposes license and changelog pages through MkDocs snippets.
- Apply the `update-docstrings` skill when docstrings, rendered signatures, or
  API-facing examples are changed.

## Computational and Numerical Functionality

When documenting computational geometry, numerical algorithms, or spatial data structures:

- Explain the implemented methodology at a level that makes its behavior independently verifiable.
- Distinguish approximate, conservative, broad-phase, and precise results.
- State tolerance and boundary semantics, false-positive and false-negative guarantees, backend assumptions, and known limitations.
- Describe relevant cache invalidation or acceleration-structure behavior when it affects correctness.
- Include commands or tests that verify the documented behavior.
- Add the primary technical sources and backend documentation that informed the implementation to the top-level `REFERENCES.md`.
- Keep claims scoped to what is actually implemented, and clearly label sources associated only with planned work.

## Validation

- Run `git diff --check`.
- Run focused doctests and Ruff when Python examples or docstrings change.
- Build affected documentation with strict MkDocs settings.
- Report warnings or unavailable dependencies; do not claim a clean build if
  the required command could not run.
