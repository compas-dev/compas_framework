# Documentation Coordination Architecture Decisions

ADRs 001–009 are **Proposed**. No package documentation implementation is
authorized until the relevant decisions are explicitly accepted.

| Order | ADR | Status | Depends on | Main tradeoff |
|---:|---|---|---|---|
| 1 | [001 — Scope and ownership](001-scope-and-ownership.md) | Proposed | None | Active ten and explicit ownership versus an open-ended ecosystem cleanup. |
| 2 | [002 — Example classification](002-example-classification.md) | Proposed | 001 | Declared authoritative categories versus implicit directory exclusions. |
| 3 | [003 — Static example gate](003-static-example-gate.md) | Proposed | 002, Modernisation 011 | Ruff and Pyright for public examples versus unchecked sample code. |
| 4 | [004 — Runtime smoke contract](004-runtime-smoke-contract.md) | Proposed | 002–003 | Representative headless execution versus static-only or indiscriminate execution. |
| 5 | [005 — Version and API baseline](005-version-and-api-baseline.md) | Proposed | stable public contracts | Exact branch/release behavior versus version-ambiguous examples. |
| 6 | [006 — Information architecture](006-information-architecture.md) | Proposed | 001 | Semantic consistency with a core exception versus identical directory trees. |
| 7 | [007 — Canonical example sources](007-canonical-example-sources.md) | Proposed | 002, 006 | One executable source versus copied variants. |
| 8 | [008 — Migration policy](008-migration-policy.md) | Proposed | 003, 005, 007 | Contract-aware review versus mechanical replacement. |
| 9 | [009 — Later-wave admission](009-later-wave-admission.md) | Proposed | active-ten completion | Explicit compatibility waves versus silent ecosystem expansion. |

## Dependency graph

```text
001 -> 002 -> 003 -> 004
 |      |      \
 |      |       008
 |      |      /   \
 |      +-> 007     009
 |          /
 +-> 006 --+

stable API contracts -> 005 -> 008
active-ten completion --------> 009
```
