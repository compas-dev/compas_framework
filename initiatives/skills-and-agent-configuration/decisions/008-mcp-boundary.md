# ADR 008: No Baseline COMPAS MCP Server

## Status

Proposed.

## Context

No audited workflow currently requires live COMPAS data, authentication, or a
controlled remote action. Local source, docs, tests, and skills provide the
identified static knowledge.

## Options

1. Add no MCP server in the baseline.
2. Build a COMPAS documentation server immediately.
3. Bundle repository and publishing actions into a broad server.

## Recommendation

Choose option 1. A later server requires a named live use case, its own ADR,
threat model, tool inventory, authorization policy, and verification. Prefer
read-only access, least privilege, explicit allowlists, and credentials outside
version control.

## Consequences

- The initial initiative has no server deployment or authentication burden.
- Skills remain useful offline and in source checkouts.
- GitHub, documentation search, or framework services may be admitted later
  when their live value is demonstrated.

## Dependencies

ADRs 002 and 004.
