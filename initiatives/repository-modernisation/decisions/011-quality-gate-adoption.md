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

Executable Python examples are part of the public contract and are included in
both Ruff and Pyright. Repositories configure their example directories
explicitly, repair outdated framework idioms, and prove that the configured
commands actually enumerate those files. Optional runtime examples may use a
focused execution environment, but they are not excluded from static checks.

## Consequences

Repositories with debt need preparatory work. Progress reports must distinguish
baseline, advisory transition, and completed blocking state. Regression tests
cover configuration as well as package behavior. Example cleanup prefers the
current high-level framework API over equivalent low-level attribute access;
for example, use `mesh.vertex_point(vertex)` instead of constructing
`Point(*mesh.vertex_attributes(vertex, "xyz"))`.

## Affected repositories

All core repositories.

## Dependencies

ADR 005, ADR 006, ADR 009.

## Clarification

On 2026-11-06, explicit user direction made executable-example Ruff and
Pyright coverage part of the blocking migration gate. Broader prose and
cross-framework example coordination may be organized as a separate
documentation initiative, but that does not defer checking executable examples
in repositories already being modernized.
