# Plugin Implementations Architecture Decisions

Decisions 001–006 are **Proposed**. No implementation is authorized until they
are explicitly approved.

| Order | ADR | Status | Depends on | Main tradeoff |
|---:|---|---|---|---|
| 1 | [001 — Authoritative discovery](001-authoritative-discovery.md) | Proposed | None | Explicit entry points versus legacy scanning or a new registry. |
| 2 | [002 — Registration boundary](002-registration-boundary.md) | Proposed | 001 | Lightweight category modules versus importing implementations during discovery. |
| 3 | [003 — Contract and direct APIs](003-contract-and-direct-apis.md) | Proposed | 002, stable core contracts | Exact core wrappers plus useful direct APIs versus divergent adapters. |
| 4 | [004 — Optional runtimes](004-optional-runtimes.md) | Proposed | 001, 002 | Accurate requirements and normal failures versus eager imports or suppression. |
| 5 | [005 — Verification and evidence](005-verification-and-evidence.md) | Proposed | 001–004 | Source, installed, artifact, and runtime evidence versus partial verification. |
| 6 | [006 — Rollout scope and package admission](006-rollout-scope.md) | Proposed | 005 | Six-package initial scope and explicit later admission versus open-ended rollout. |

## Dependency graph

```text
001
 |
002
 |\
003 004
 \ /
 005
  |
 006
```
