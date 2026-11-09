# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-09

## Resume here

Current phase: `Phase 3 follow-up verified; ADR 029/031 decisions and interactive confirmation pending`

The scene foundation, contextual settings, Viewer configuration and tables,
selection, and reversible transformations governed by Accepted ADRs 001–020
are implemented and verified. The architectural watchpoint remains active:
the accepted `Data`/scene-state/extension model is authoritative, but concrete
contrary evidence should be brought back for an explicit amendment rather than
handled through speculative abstractions.

Phase 3 is implemented under Accepted ADRs 021–028 and 030. Core owns narrow durable
text, arrow, and distance annotation data (ADR 021). Persistent dimensions
snapshot declared unit and precision without implicit conversion (ADR 022).
Legacy `Tag` and `ArrowOverlay` names and serialized paths are removed without
aliases or legacy decoding (ADR 023). Live distance inspection is transient,
while explicit fixed and associative modes create durable dimensions
(ADRs 024 and 028). Viewer owns one ordered, non-serialized scale/legend layer
(ADR 025), nearest eligible discrete-point acquisition and one-shot
measurement tools (ADR 026), and the editable Units and Measurement
presentation settings with read-only global tolerance (ADR 027). Interactive acquisition is limited to
visible Point, Mesh-vertex, and Graph-node guides with no invisible fallback.
Persistent dimensions use ADR 030's always-visible final pass. Proposed ADR
029 would move annotations out of the spatial hierarchy, add a flat
Annotations UI, and own a narrow durable dimension style; it is not approved
or implemented. Proposed ADR 031 would expose the existing spatial-object
deletion command in the default Edit menu while preserving subtree removal,
independent data, transform-history invalidation, and unresolved associative
dimensions.

The Core and refreshed Viewer candidate and framework gate are green at the
revisions below. Viewer restricts acquisition to visible discrete guides,
uses an 18-logical-pixel snap radius, proves the 4 × 3 diagonal equals 5,
renders persistent dimensions above geometry, and removes the Attributes tab
from the default sidebar while retaining opt-in custom use. Local package
verification, independent review, complete Viewer package CI, and the exact
framework source-installed gate pass.

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
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `de3cb19b2db9b2635668151b7986225391e8b4e6` | [7](https://github.com/compas-dev/compas_framework/pull/7) | Contracts and exact source-installed gate passed |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `353cebfd21cd3623f7d950527d71f4770ff2a21c` | [1540](https://github.com/compas-dev/compas/pull/1540) | Complete hosted package workflow passed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `68548b478b9c2642ec734495e0c3ae85f8d5f1fb` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Complete hosted package workflow passed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed | Current Viewer candidate passed 412 tests, Ruff, format, Pyright, strict MkDocs, and `git diff --check`; independent review approved it without remaining findings. The direct-source framework gate passed 12 tests with the exact-revision assertion skipped as designed. |
| Native interactive probes | Partial | Earlier native macOS captures showed the point palette, winner, retained anchor, live line and label without a `QPainter` warning or crash. Direct confirmation of 18-pixel attraction, discrete-only acquisition, and the final persistent-dimension pass remains pending. |
| Package CI | Passed | Core PR 1540 is green. Viewer PR 233 passed build, coverage, policy, distributions, and all nine Python/OS quality jobs for `68548b478b9c2642ec734495e0c3ae85f8d5f1fb` in run `42607751694`. |
| Framework integration | Passed | Framework PR 7 passed contracts and exact source-installed candidate run `42607915821` at `de3cb19b2db9b2635668151b7986225391e8b4e6`. |
| Candidate artifacts | Not run | No compatibility claim is made for independently built candidate artifacts. Run this layer before artifact admission or release if that claim is required. |

## Next tasks

1. Resolve Proposed ADR 029 before changing annotation storage, UI, or style.
2. Resolve Proposed ADR 031 before exposing spatial deletion in the default
   Edit menu.
3. Confirm point attraction, exact diagonal, discrete-only acquisition, and
   persistent-dimension visibility interactively.

## Approval gates

- Adding model, session, notebook, or host packages requires explicit approval.
- Session aggregation and Viewer new/open/save conveniences remain future work.
- Do not merge or publish without explicit approval.
