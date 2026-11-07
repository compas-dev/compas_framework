# ADR 007: General Agent Roles and Permission Ownership

## Status

Accepted.

## Context

Current custom agents are geometry-specific and some set `sandbox_mode` even
though custom agents inherit parent permissions and cannot override that
setting.

## Options

1. Generalize the five roles and respect parent-session permissions.
2. Keep geometry-specific roles for all framework initiatives.
3. Create many initiative-specific agents.

## Recommendation

Choose option 1. Retain explorer, architect, implementer, reviewer, and
documenter. Define responsibility, file ownership, evidence, and stopping
conditions. Remove unenforceable permission claims, use only documented
configuration fields and supported capability controls, and leave approval,
MCP, and sandbox policy to the parent session.

Do not add a tutor agent initially; the learner skill must work with an
ordinary agent.

## Consequences

- Role names remain familiar.
- Configuration describes behavior it can actually enforce.
- Initiative-specific facts stay in the relevant skills and proposals.

## Dependencies

ADRs 002 and 004.
