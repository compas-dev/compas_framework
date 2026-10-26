---
name: update-docstrings
description: Migrate or improve COMPAS Framework Python docstrings using MkDocs-compatible NumPy style without unintentionally changing runtime behavior.
---

# Update COMPAS Framework docstrings

Apply `AGENTS.md`, especially **Documentation and Public API** and **Tests and Validation**.

## Requirements

- Keep NumPy-style sections, but write their content as MkDocs-compatible Markdown.
- Omit parameter types when the signature is annotated. Keep explicit canonical Python types in `Returns`.
- Document overload returns independently and state the argument condition selecting each one.
- Document a tuple return as one tuple matching the return annotation. Omit `Returns` when a function returns `None`.
- Replace Sphinx syntax in touched docstrings with Markdown equivalents.
- Use mkdocstrings cross-references in `See Also` entries when useful.
- Document package ownership and native prerequisites in cross-package examples.
- Keep examples short, executable, deterministic, and valuable. Remove empty sections.
- Leave a blank line before the closing quotes of a multiline docstring.
- Do not change runtime behavior while editing documentation.

## Validation

Run focused doctests, Ruff on touched Python files, and `git diff --check`. Build affected MkDocs pages and inspect warnings.
