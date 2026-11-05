# Plugin Implementations Architecture Decisions

Decisions 001–006 are **Accepted**. Implementation is authorized for the exact
initial scope in ADR 006; later waves still require explicit admission.

| Order | ADR | Status | Depends on | Main tradeoff |
|---:|---|---|---|---|
| 1 | [001 — Authoritative discovery](001-authoritative-discovery.md) | Accepted | None | Explicit entry points versus legacy scanning or a new registry. |
| 2 | [002 — Registration boundary](002-registration-boundary.md) | Accepted | 001 | Lightweight category modules versus importing implementations during discovery. |
| 3 | [003 — Contract and direct APIs](003-contract-and-direct-apis.md) | Accepted | 002, stable core contracts | Exact core wrappers plus useful direct APIs versus divergent adapters. |
| 4 | [004 — Optional runtimes](004-optional-runtimes.md) | Accepted | 001, 002 | Accurate requirements and normal failures versus eager imports or suppression. |
| 5 | [005 — Verification and evidence](005-verification-and-evidence.md) | Accepted | 001–004 | Source, installed, artifact, and runtime evidence versus partial verification. |
| 6 | [006 — Rollout scope and package admission](006-rollout-scope.md) | Accepted | 005 | Six-package initial scope and explicit later admission versus open-ended rollout. |

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
