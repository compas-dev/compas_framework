# ADR 002: Authoritative Example Classification

## Status

Proposed.

## Context

Example roots, exclusions, and runtime expectations currently differ by
repository. Directory names such as `__temp` can hide whether a file is a
published example, draft, or unsupported test case.

## Options

1. Declare roots and classify every example explicitly.
2. Treat every `.py` file under `docs` or `examples` identically.
3. Continue relying on ignores and directory naming.

## Recommendation

Choose option 1. Every authoritative example belongs to exactly one category:
static-and-smoke, static-only interactive, static-plus-optional-runtime,
host-runtime, or non-authoritative draft/archive. Imported helper modules share
their example's static gate. Draft material is removed, moved to an explicit
non-published location, or deliberately admitted.

Use `docs/examples/` by default. Core may retain `docs/assets/examples/` as an
approved exception. Other roots require recorded justification.

## Consequences

- Published scope and verification expectations are explicit.
- `__temp` and ignore rules stop functioning as undocumented policy.
- Each repository needs a maintained example manifest or equivalent
  configuration.

## Dependencies

ADR 001.
