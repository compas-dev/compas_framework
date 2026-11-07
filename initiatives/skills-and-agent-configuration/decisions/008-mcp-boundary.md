# ADR 008: No Baseline COMPAS MCP Server

## Status

Accepted.

## Context

No audited workflow currently requires live COMPAS data, authentication, or a
controlled remote action. Local source, docs, tests, and skills provide the
identified static knowledge.

## Options

1. Add no MCP server in the baseline.
2. Build a COMPAS documentation server immediately.
3. Bundle repository and publishing actions into a broad server.

## Recommendation

Choose option 1. The initiative still delivers an admission and secure local
configuration template covering a named live use case, tool inventory,
read/write classification, authorization points, credential ownership, and
verification. A later server requires its own ADR and threat model. Prefer
read-only access, least privilege, explicit allowlists, and credentials outside
version control. MCP belongs to the parent session; custom agent files cannot
override it.

## Consequences

- The initial initiative has no server deployment or authentication burden.
- Skills remain useful offline and in source checkouts.
- GitHub, documentation search, or framework services may be admitted later
  when their live value is demonstrated.

## Dependencies

ADRs 002 and 004.
