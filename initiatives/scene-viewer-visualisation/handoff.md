# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-09

## Resume here

Current phase: `Phase 3 snap refinements verified; interactive confirmation pending`

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

The Core and Viewer candidates and the framework's exact source-installed gate
are green at the recorded revisions below. Direct use refined point feedback
and acquisition. Viewer revision
`5a25154950be63548928da956ecaff1c2f7e4d3c` adds larger bright square markers,
same-object point-footprint depth qualification for receding visible vertices,
and Mesh-edge exclusion. Local package verification, independent review, the
complete hosted Viewer workflow, and the refreshed exact source-installed
framework gate pass. Interactive confirmation of marker brightness and
steep-angle acquisition remains pending.

Exact candidate-artifact compatibility has not been run and must not be
inferred from source installation, package builds, or native probes.

Read next:

1. [Implementation plan](implementation-plan.md)
2. [Decision index](decisions/README.md)
3. [Proposal](proposal.md)
4. [Exploratory UI sketch](ui.md)

## Exact candidates

| Repository | Branch | Verified revision | Pull request | Status |
|---|---|---|---|---|
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `8fa3d05b24ca74562a4a8bff2de5c3e33d4d9b71` | [7](https://github.com/compas-dev/compas_framework/pull/7) | Snap-refinement exact source-installed gate passed |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `353cebfd21cd3623f7d950527d71f4770ff2a21c` | [1540](https://github.com/compas-dev/compas/pull/1540) | Complete hosted package workflow passed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `5a25154950be63548928da956ecaff1c2f7e4d3c` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Complete hosted package workflow passed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed | Refined Viewer candidate passed 416 tests, Ruff, format, Pyright, strict MkDocs, and independent review. |
| Native interactive probes | Partial | Earlier native macOS captures showed the point palette, winner, retained anchor, live line and label without a `QPainter` warning or crash, and a coincident completed dimension remained visible. Direct confirmation of the new square brightness and steep-angle acquisition remains pending. |
| Package CI | Passed | Core PR 1540 is green. Viewer PR 233 passed build, distributions, coverage, policy, and all nine OS/Python quality jobs at `5a25154950be63548928da956ecaff1c2f7e4d3c`. |
| Framework integration | Passed | Local direct-source execution passed 12 tests with only the exact-installed-revision assertion skipped by design; Ruff, format, Pyright, strict MkDocs, and independent review passed. Manually dispatched hosted run `42599535486` passed exact `source-installed-candidates` at framework revision `8fa3d05b24ca74562a4a8bff2de5c3e33d4d9b71`, pinned to the recorded Core and Viewer heads. |
| Candidate artifacts | Not run | No compatibility claim is made for independently built candidate artifacts. Run this layer before artifact admission or release if that claim is required. |

## Next tasks

1. Confirm marker brightness, receding-vertex behavior, and Mesh-edge exclusion
   interactively.
2. Continue the Phase 4 scope audit after that direct-use evidence is recorded.
3. Decide whether exact candidate-artifact compatibility is required before
   initiative admission.

## Approval gates

- Adding model, session, notebook, or host packages requires explicit approval.
- Session aggregation and Viewer new/open/save conveniences remain future work.
- Do not merge or publish without explicit approval.
