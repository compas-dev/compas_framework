# ADR 003: Static Example Quality Gate

## Status

Accepted.

## Context

Only one active repository currently exposes its complete example tree to both
Ruff and Pyright. Public examples contain stale APIs, broad suppressions, and
patterns users are likely to copy.

## Options

1. Include every authoritative Python example in blocking Ruff and Pyright.
2. Run Ruff only.
3. Keep examples outside ordinary quality checks.

## Recommendation

Choose option 1. Optional and native examples are checked in an environment
containing their declared typing surface. Whole-file `type: ignore` is not an
accepted solution. Narrow suppressions require an adjacent, concrete rationale;
casts remain only for real narrowing. Examples use current high-level idioms
when semantics are equivalent.

Repository modernisation implements the active-ten tool configuration. This
initiative owns the authoritative inventory and content corrections exposed by
the gate.

## Consequences

- Examples become part of the public static contract.
- Optional dependency typing environments must be explicit.
- Existing suppressions and stale idioms become blocking migration work.

## Dependencies

ADR 002 and Repository Modernisation ADR 011.
