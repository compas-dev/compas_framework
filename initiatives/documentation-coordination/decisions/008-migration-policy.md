# ADR 008: Documentation Change and Migration Policy

## Status

Accepted.

## Context

API cleanup can look mechanical while changing algorithms, mutation, result
representations, units, approximation, optional dependencies, or failure
behavior.

## Options

1. Review documentation migrations as contract changes where applicable.
2. Apply mechanical search-and-replace whenever syntax changed.
3. Delay documentation until after all package source work.

## Recommendation

Choose option 1. Every migration records the old and new idiom, semantic
effects, affected examples/pages, and verification commands. Mechanical
replacement is allowed only when behavior is equivalent. Explicit algorithms,
native prerequisites, optional dependencies, controls, units, tolerances, and
known limitations remain visible.

Public behavior changes update docstrings, API pages, tutorials/examples, and
changelog coverage together. COMPAS docstrings use MkDocs-compatible NumPy
style with Markdown, never Sphinx or reStructuredText markup.

## Consequences

- Documentation review detects behavior drift instead of merely broken names.
- Cross-package API initiatives remain authoritative.
- Some cleanup waits for final contracts rather than being applied twice.

## Dependencies

ADRs 003, 005, and 007.
