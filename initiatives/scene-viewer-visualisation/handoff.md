# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-09

## Resume here

Current phase: `Phase 3 implementation and source integration complete`

The scene foundation, contextual settings, Viewer configuration and tables,
selection, and reversible transformations governed by Accepted ADRs 001–020
are implemented and verified. The architectural watchpoint remains active:
the accepted `Data`/scene-state/extension model is authoritative, but concrete
contrary evidence should be brought back for an explicit amendment rather than
handled through speculative abstractions.

Phase 3 is implemented under Accepted ADRs 021–028. Core owns narrow durable
text, arrow, and distance annotation data (ADR 021). Persistent dimensions
snapshot declared unit and precision without implicit conversion (ADR 022).
Legacy `Tag` and `ArrowOverlay` names and serialized paths are removed without
aliases or legacy decoding (ADR 023). Live distance inspection is transient,
while explicit fixed and associative modes create durable dimensions
(ADRs 024 and 028). Viewer owns one ordered, non-serialized scale/legend layer
(ADR 025), prioritized screen-space snapping and one-shot measurement tools
(ADR 026), and the editable Units and Measurement presentation settings with
read-only global tolerance (ADR 027). Associative point/vertex/node and
parameterized line/edge anchors never silently fall back; unsupported or
removed references remain visibly unresolved.

Core and Viewer package CI and the framework's exact source-installed gate are
green at the revisions below. Exact candidate-artifact compatibility has not
been run and must not be inferred from source installation or package build
jobs. A stronger real-raster integration check would be useful additional
evidence, but was not a blocker for the approved Phase 3 source contract.

Read next:

1. [Implementation plan](implementation-plan.md)
2. [Decision index](decisions/README.md)
3. [Proposal](proposal.md)
4. [Exploratory UI sketch](ui.md)

## Exact candidates

| Repository | Branch | Verified revision | Pull request | Status |
|---|---|---|---|---|
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `8b45ab56a6e6d332c7ec67a588e21bc007c0828b` | [7](https://github.com/compas-dev/compas_framework/pull/7) | Phase 3 gate revision; contracts and exact source-installed candidates passed |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `353cebfd21cd3623f7d950527d71f4770ff2a21c` | [1540](https://github.com/compas-dev/compas/pull/1540) | Complete hosted package workflow passed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `eb018d6ed2c8651a5294e2cd3d98c468cb3bd3e2` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Complete hosted package workflow passed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed | Viewer passed 396 tests, Ruff, format, Pyright, strict MkDocs, and independent review. |
| Package CI | Passed | Core PR 1540 is green. Viewer PR 233 passed build, distributions, coverage, policy, and all nine OS/Python quality jobs. |
| Framework integration | Passed | Local direct-source execution passed 11 tests with only the exact-installed-revision assertion skipped by design; Ruff, format, Pyright, and independent review passed. Hosted PR 7 passed both `contracts` and exact `source-installed-candidates`, pinned to the recorded Core and Viewer heads. |
| Candidate artifacts | Not run | No compatibility claim is made for independently built candidate artifacts. Run this layer before artifact admission or release if that claim is required. |

## Next tasks

1. Audit the remaining Phase 4 public-operation and example scope and either
   close it with existing evidence or implement only demonstrated gaps.
2. Decide whether exact candidate-artifact compatibility is required before
   initiative admission; run it if required.
3. Request explicit merge approval after the remaining applicable evidence is
   recorded.

## Approval gates

- Adding model, session, notebook, or host packages requires explicit approval.
- Session aggregation and Viewer new/open/save conveniences remain future work.
- Do not merge or publish without explicit approval.
