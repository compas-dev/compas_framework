# Skills and Agent Configuration Architecture Decisions

ADRs 001–010 are **Accepted**. ADR 011 is **Proposed**. The approved rollout may
proceed subject to the publication, MCP, external-connection, merge, and
release boundaries in the proposal; ADR 011 adds no authorization until it is
explicitly accepted.

| Order | ADR | Status | Depends on | Main tradeoff |
|---:|---|---|---|---|
| 1 | [001 — Skill families](001-skill-families.md) | Accepted | None | Separately installable user and developer workflows versus one catch-all surface. |
| 2 | [002 — Authority boundaries](002-authority-boundaries.md) | Accepted | 001 | Clear ownership versus duplicated rules. |
| 3 | [003 — Source and distribution](003-source-and-distribution.md) | Accepted | 001, 002 | One canonical source and two installable bundles versus repository copies. |
| 4 | [004 — Portability](004-portability.md) | Accepted | 003 | Portable skills plus adapters versus Codex-only workflows. |
| 5 | [005 — Learner curriculum](005-learner-curriculum.md) | Accepted | 001, 002, 004 | One core-only guided vertical slice versus immediate topic proliferation. |
| 6 | [006 — Maintainer baseline](006-maintainer-baseline.md) | Accepted | 001–004 | Four proven workflows versus speculative skill growth. |
| 7 | [007 — Agent roles](007-agent-roles.md) | Accepted | 002, 004 | General roles and parent permissions versus ineffective local claims. |
| 8 | [008 — MCP boundary](008-mcp-boundary.md) | Accepted | 002, 004 | No baseline server versus speculative live infrastructure. |
| 9 | [009 — Safety and artifacts](009-safety-and-artifacts.md) | Accepted | 001, 002 | Explicit ownership and authorization versus convenience mutations. |
| 10 | [010 — Validation and lifecycle](010-validation-and-lifecycle.md) | Accepted | 001–009 | Behavioral evidence versus Markdown-only validation. |
| 11 | [011 — Initiative-first proposals](011-initiative-first-proposals.md) | Proposed | 002, 006, 007, 010 | Architecture-first framework intake versus code-first proposals or ceremony for every edit. |

## Dependency graph

```text
001 -> 002 -> 003 -> 004
001, 002, 004      -> 005
001, 002, 003, 004 -> 006
002, 004           -> 007
002, 004           -> 008
001, 002           -> 009
001–009            -> 010
002, 006, 007, 010 -> 011
```
