# ADR 002: Authority and Ownership Boundaries

## Status

Proposed.

## Context

Framework policy, public documentation, initiative decisions, skills, scripts,
and agent prompts can easily become competing sources of truth.

## Options

1. Assign one responsibility to each artifact layer.
2. Repeat all relevant rules in every skill and repository.
3. Treat skills as the authoritative documentation system.

## Recommendation

Choose option 1. Documentation owns factual public behavior. The initiative
that approves a framework contract owns its developer guidance. This
initiative owns packaging, discovery, routing, validation, and agent/MCP
configuration. `AGENTS.md` holds durable invariants and skill triggers; skills
link to maintained references rather than duplicating them.

## Consequences

- Contract changes update one authoritative source.
- Documentation coordination, typing, geometry, and plugin initiatives retain
  their existing ownership.
- Skills may orchestrate authoritative material but cannot redefine it.

## Dependencies

ADR 001.
