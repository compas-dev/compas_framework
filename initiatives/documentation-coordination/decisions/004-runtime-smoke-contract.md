# ADR 004: Headless Runtime Smoke Contract

## Status

Accepted.

## Context

Static checking cannot prove imports, renamed APIs, file ownership, or
meaningful results. Running every example in ordinary CI is impractical for
interactive, GUI, native, optional, and host workflows.

## Options

1. Run a declared representative headless subset.
2. Use static checking only.
3. Run every example in ordinary CI.
4. Require screenshot or golden-output tests for every example.

## Recommendation

Choose option 1. Each repository declares a representative non-interactive,
deterministic, network-independent subset that asserts meaningful results and
writes generated files only to isolated temporary directories. Optional,
native, GUI, and host examples receive separate runtime evidence in their
supported environments.

A missing required runtime is an explicit unverified limitation, not a passing
test.

## Consequences

- Primary user paths receive runtime evidence without making CI depend on
  every interactive environment.
- Repositories must document why examples are excluded from headless smoke.
- Host packages still require real host validation before completion.

## Dependencies

ADRs 002 and 003.
