# ADR 011: Adoption of New Blocking Quality Gates

**Status:** Accepted

## Context

Strict MkDocs and Pyright are desired, but some repositories have existing
warning or typing debt. Enabling a failing required check immediately can halt
unrelated work; permanently non-blocking checks provide no contract.

## Options

1. Make every new gate blocking immediately.
2. Keep debt-heavy gates advisory indefinitely.
3. Measure a baseline, fix or narrowly record existing debt, then make the
   complete target gate blocking within the same migration phase.

## Recommendation

Use an explicit, time-bounded baseline phase. Do not add broad exclusions or
silent failure. A repository is not considered migrated until its applicable
Ruff, Pyright, tests, strict docs, and artifact gates are blocking and pass.

## Consequences

Repositories with debt need preparatory work. Progress reports must distinguish
baseline, advisory transition, and completed blocking state. Regression tests
cover configuration as well as package behavior.

## Affected repositories

All core repositories.

## Dependencies

ADR 005, ADR 006, ADR 009.
