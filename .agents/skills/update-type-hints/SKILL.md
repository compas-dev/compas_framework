---
name: update-type-hints
description: Add, modernize, or review Python type hints in COMPAS Framework integration code for Python 3.12+ without unintentionally changing runtime behavior.
---

# Update COMPAS Framework type hints

Apply `AGENTS.md`, especially **Python and Typing**, **Framework Integration Contracts**, and **Tests and Validation**.

## Requirements

- Use Python 3.12 syntax, PEP 604 unions, built-in generics, and `Self` where appropriate.
- Use overloads for argument-dependent public return types instead of `Any`.
- Model values accepted by the runtime API; do not add conversions or validation merely to satisfy an annotation.
- Prefer precise protocols, aliases, overloads, or source annotations over `cast`, concrete runtime checks, or broad `Any`.
- Use `TYPE_CHECKING` for optional or heavy dependencies needed only for annotations.
- Preserve plugin discovery, serialization behavior, accepted inputs, return values, ordering, side effects, and exceptions unless explicitly changing them.

## Validation

Run the narrowest relevant tests first, Pyright on changed integration code, Ruff on touched files, and `git diff --check`.
