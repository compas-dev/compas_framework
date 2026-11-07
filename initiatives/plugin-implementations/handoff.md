# Plugin Implementations Handoff

Last updated: 2026-11-07

## Resume here

Current phase: `implementation`

Status: Reconnaissance and architecture are complete. ADRs 001–006 are
Accepted, Waves 0–1 are authorized, and source migration is substantially
implemented. Selection, package-owned artifact, model/viewer coordination, and
final installed cross-package gates remain open.

Read next:

1. [Objective](objective.md)
2. [Implementation plan](implementation-plan.md), starting with Phase 1
3. [ADR 005 — Verification and evidence](decisions/005-verification-and-evidence.md)
4. [ADR 006 — Rollout scope and package admission](decisions/006-rollout-scope.md)

Do not reread the full inventory or proposal unless a finding changes the
accepted design or proposed scope.

## Decisions and approvals

- Accepted: [ADRs 001–006](decisions/README.md).
- Unresolved: no ADR blocks the authorized Wave 0–1 tasks.
- Scope boundary: only `compas`, `compas_cgal`, `compas_libigl`, `compas_occ`,
  `compas_model`, and `compas_viewer` are authorized. Later waves require an
  explicit scope amendment and approval. Do not merge or publish without
  explicit approval.

## Working state

| Repository | Branch | Exact head | Pull request | Status |
|---|---|---|---|---|
| `compas-dev/compas` | `initiative/typing-alignment` | `99b82a6673ff7d05c1c323c8921135c274993f11` | [1539](https://github.com/compas-dev/compas/pull/1539) | Pushed draft |
| `compas-dev/compas_cgal` | `initiative/typing-alignment` | `bb3624e714719d543c61768320d91811ba96cc6c` | [81](https://github.com/compas-dev/compas_cgal/pull/81) | Pushed draft |
| `compas-dev/compas_libigl` | `initiative/typing-alignment` | `710b2b6714839a203fc8a6c62c437c0f6735ba0e` | [47](https://github.com/compas-dev/compas_libigl/pull/47) | Pushed draft |
| `compas-dev/compas_occ` | `initiative/typing-alignment` | `7fdf2ffb57d1de16308020e14ec626d79e65a034` | [32](https://github.com/compas-dev/compas_occ/pull/32) | Pushed draft |
| `BlockResearchGroup/compas_model` | `initiative/repository-modernisation` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | [68](https://github.com/BlockResearchGroup/compas_model/pull/68) | Pushed draft |
| `compas-dev/compas_viewer` | `initiative/repository-modernisation` | `cf5a5195bda840a511319d6b7201978af68c15e3` | [232](https://github.com/compas-dev/compas_viewer/pull/232) | Pushed draft |
| `compas-dev/compas_framework` | `initiative/candidate-artifact-integration` | `663a4438902e479e2b14c3a2319649030a314ce7` | [2](https://github.com/compas-dev/compas_framework/pull/2) | Pushed draft; clean |

Before editing any package, verify that its recorded head is still current and
inspect that repository for unrelated dirty paths.

## Completed at this checkpoint

- CGAL uses lightweight category entry points, binds requirements to compiled
  modules, and keeps orphan direct APIs undecorated.
- Model and viewer discovery are requirement-gated and import-light; their
  package workflows inspect installed entry points.
- Protected framework run
  [42347847450](https://github.com/compas-dev/compas_framework/actions/runs/42347847450)
  verifies exact candidate retrieval and secret-free installed execution at
  framework head `663a4438902e479e2b14c3a2319649030a314ce7`: four runtime
  contracts pass and Pyright reports zero errors and warnings.
- The temporary framework retrieval secrets have been removed. `main` remains
  untouched; all listed pull requests remain draft and unmerged.

## Next tasks

1. Implement and verify the core requirement-selection matrix, including
   module-name and callable requirements, non-selection, defaults, and
   `PluginNotInstalledError`.
2. Add libigl compiled-runtime requirements and complete representative public
   dispatch, lazy delegation, unavailable-runtime, and built-wheel evidence.
3. Replace OCC synthetic-only artifact evidence, then run the coordinated
   model/viewer registration and final installed cross-package review.

## Blockers and approval gates

- Model/viewer coordination must follow their package architecture and geometry
  conversion contracts; do not invent lifecycle behavior here.
- Optional backends, host integrations, and later ecosystem waves remain out of
  scope until separately approved.
- Merging or publishing any initiative branch still requires explicit approval.

## Verification

Last verified:

- Framework focused candidate contracts — 46 passed at `663a443`.
- Strict framework MkDocs, Ruff, formatting, Pyright, actionlint, and diff
  checks passed at the recorded checkpoint.
- [Native integration run 42347847450](https://github.com/compas-dev/compas_framework/actions/runs/42347847450)
  — retrieve, build, and execute succeeded; four tests passed; Pyright reported
  zero errors and warnings.

Run next:

```text
/Users/vanmelet/miniforge3/envs/compas3/bin/python -m pytest <focused plugin tests>
/Users/vanmelet/miniforge3/envs/compas3/bin/python -m ruff check <changed paths>
/Users/vanmelet/miniforge3/envs/compas3/bin/python -m pyright
```
