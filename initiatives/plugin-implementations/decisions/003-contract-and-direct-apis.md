# ADR 003: Contract Parity and Direct API Policy

## Status

Accepted.

## Context

Discovery metadata can activate wrappers whose signatures or results no longer
match core. Backend packages may also expose useful direct APIs, but a second
divergent high-level contract makes dispatch and documentation ambiguous.

## Options

1. Require exact core wrappers and retain semantically compatible direct APIs.
2. Permit backend-specific wrappers plus adapters.
3. Remove every direct backend API.
4. Introduce plugin-specific geometry representations.

## Recommendation

Choose option 1. Wrappers exactly match the core extension point in category,
name, parameters, defaults, structural inputs, result, and failure behavior.
Useful direct APIs remain undecorated. Clearly named low-level APIs may differ
only when their low-level contract is explicit.

## Consequences

- Contract migration precedes metadata for incompatible legacy plugins.
- Native normalization remains in implementation modules.
- Existing geometry, tessellation, triangulation, BRep, and scene contracts
  remain authoritative.
- No new representation or generic adapter is introduced.

## Affected packages

Every plugin provider and the core extension points it implements.

## Dependencies

- [ADR 002](002-registration-boundary.md)
- Stable contracts from typing and geometry initiatives.
