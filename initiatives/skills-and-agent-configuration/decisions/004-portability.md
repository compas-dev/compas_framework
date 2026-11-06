# ADR 004: Portable Skills and Client Adapters

## Status

Accepted.

## Context

Learners and maintainers may use different agent hosts. Current repository
configuration is Codex-specific, but ordinary skill workflows need not be.

## Options

1. Keep portable `SKILL.md` workflows and isolate client-specific adapters.
2. Make every skill depend on Codex agents and configuration.
3. Define separate skill bodies for every client.

## Recommendation

Choose option 1. Ordinary skills must remain correct without MCP or subagents.
Codex-specific agent definitions and configuration stay under `.codex/` and may
improve orchestration without changing the workflow contract.

## Consequences

- Skills can be reused by compatible hosts.
- Client adapters remain small and replaceable.
- Unsupported client features cannot be hidden prerequisites.

## Dependencies

ADR 003.
