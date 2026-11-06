# ADR 003: Canonical Source and Distribution

## Status

Proposed.

## Context

Current framework skills are copied unevenly across repositories and have
already diverged.

## Options

1. Author one portable, namespaced bundle in the coordination repository.
2. Copy every shared skill into every package repository.
3. Put all shared skills in core COMPAS.
4. Create a dedicated public repository immediately.

## Recommendation

Choose option 1. Use names such as `compas-get-started` and
`compas-verify-change`. Package repositories retain only package-specific
skills or thin routing. Provide one bootstrap path and keep the bundle
structurally movable to a dedicated repository or public plugin later.

## Consequences

- Shared workflows have one source of truth.
- CI can reject copied or diverged framework-wide skills.
- Public packaging remains possible without being required in the first wave.

## Dependencies

ADRs 001 and 002.
