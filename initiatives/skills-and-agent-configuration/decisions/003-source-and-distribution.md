# ADR 003: Canonical Source and Distribution

## Status

Accepted.

## Context

Current framework skills are copied unevenly across repositories and have
already diverged.

## Options

1. Author one canonical source in the coordination repository and expose
   separate user and developer bundles.
2. Copy every shared skill into every package repository.
3. Put all shared skills in core COMPAS.
4. Create a dedicated public repository immediately.

## Recommendation

Choose option 1. Expose `compas-user-skills`, initially containing
`compas-get-started`, and `compas-developer-tools`, containing contributor
skills. Maintain optional repo-scoped `.codex/` agent and configuration
adapters separately in the same canonical source; do not present them as
portable Agent Plugin contents. Package repositories retain only
package-specific skills or thin routing. Use local or repository marketplace
configuration for development; do not copy skill bodies or depend on
machine-specific symlinks. Keep both skill bundles structurally movable to a
dedicated repository. Public publication requires separate approval.

## Consequences

- Shared workflows have one source of truth.
- CI can reject copied or diverged framework-wide skills.
- Users do not receive contributor mutation workflows by default.
- Public packaging remains possible without being required in the first wave.

## Dependencies

ADRs 001 and 002.
