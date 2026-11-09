# Scene, Viewer, and Visualisation Handoff

Last updated: 2026-11-09

## Resume here

Current phase: `Phase 3 ADRs 036 and 040–042 implemented and verified`

The scene foundation, contextual settings, Viewer configuration and tables,
selection, and reversible transformations governed by Accepted ADRs 001–020
are implemented and verified. The architectural watchpoint remains active:
the accepted `Data`/scene-state/extension model is authoritative, but concrete
contrary evidence should be brought back for an explicit amendment rather than
handled through speculative abstractions.

The implemented Phase 3 foundation follows Accepted ADRs 021–028 and 030.
Core owns narrow durable text, arrow, and distance annotation data (ADR 021).
Persistent dimensions snapshot declared unit and precision without implicit
conversion (ADR 022).
Legacy `Tag` and `ArrowOverlay` names and serialized paths are removed without
aliases or legacy decoding (ADR 023). Live distance inspection is transient,
while explicit fixed and associative modes create durable dimensions
(ADRs 024 and 028). Viewer owns one ordered, non-serialized scale/legend layer
(ADR 025), nearest eligible discrete-point acquisition and one-shot
measurement tools (ADR 026), and the editable Units and Measurement
presentation settings with read-only global tolerance (ADR 027). Interactive
acquisition is limited to visible Point, Mesh-vertex, and Graph-node guides
with no invisible fallback.
Persistent dimensions use ADR 030's always-visible final pass. Accepted ADR
029 moves annotations out of the spatial hierarchy, adds a flat Annotations UI,
and owns a narrow durable dimension style. Accepted ADR 031 exposes the
existing spatial-object deletion command in the default Edit menu while
preserving subtree removal, independent data, transform-history invalidation,
and unresolved associative dimensions. Both implementations pass local package,
documentation, independent review, refreshed package CI, and the exact
source-installed framework gate.

Direct-use feedback shows that the current stacked sidebar resizes unrelated
panels, presents independent spatial and annotation contexts ambiguously, hides
annotation naming, and does not provide consistent background-click or Escape
deselection. Accepted ADR 032 replaces it with stable Scene, Annotations, and
System domains. The implementation, documentation, 441-test Viewer suite,
Ruff, Pyright, strict MkDocs, framework direct-source gate, and independent
review pass. Hosted package and exact source-installed integration checks also
pass.

Direct use then exposed a Qt lifecycle crash when an annotation visibility
checkbox rebuilt and deleted its own emitting tree item, plus repeated
`vertexsize` errors caused by treating an `(int, float)` field as integer-only
when its current value happened to be an integer. Both causes are fixed. The
Viewer now passes 445 tests, Ruff, Pyright, strict MkDocs, independent review,
hosted package CI, and the refreshed framework exact source-installed gate at
the revision below.

Further direct use produced ADRs 033–039. They cover the resizable
Scene inspector and Details dialog, vertex snapping with ordinary glyphs
hidden, deterministic spatial dimension offsets, screen-pinned viewport text,
label backgrounds, contextual deletion, and moving the existing geometry Add
hierarchy under Scene. ADR 036 is Accepted and implemented with a screen-pinned,
non-persistent, programmatic-first contract. Accepted ADRs 040–042 add synchronized default-toolbar selectors, a
Grid and Units System section with consistent two-column field alignment and no
tolerance UI, and transient selected-object area and volume inspection. The
four implementations pass 501 Viewer tests, Ruff, formatting, Pyright, strict
MkDocs, independent review, the complete hosted Viewer matrix, and the exact
source-installed framework gate.
The other follow-ups remain Proposed and require explicit approval.

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
| `compas-dev/compas_framework` | `initiative/scene-viewer-visualisation` | `f7ac4ce02a3d20f17a5c10246f0e905cc9b9232e` | [7](https://github.com/compas-dev/compas_framework/pull/7) | Hosted contracts and exact source-installed gate passed |
| `compas-dev/compas` | `initiative/scene-viewer-visualisation` | `70aeb1e408772f0a84213c280658d4d594bf12ea` | [1540](https://github.com/compas-dev/compas/pull/1540) | Local verification, independent review, and hosted package CI passed |
| `compas-dev/compas_viewer` | `initiative/scene-viewer-visualisation` | `efbb7991c9f60aef2e8225813c5050190b5cfb0b` | [233](https://github.com/compas-dev/compas_viewer/pull/233) | Local and hosted package verification passed |
| `BlockResearchGroup/compas_model` | `c3-upgrade` | `83df4167f7ba1539ae205a837e0238afecc0a36b` | None | Compatibility consumer only; no source changes authorized |

## Verification evidence

| Layer | Status | Evidence |
|---|---|---|
| Local package checks | Passed | Core remains at its verified candidate. Viewer passed 501 tests, Pyright, Ruff, format, strict MkDocs, and independent review. The updated direct-source framework gate passed 15 tests with the exact-revision assertion skipped as designed. |
| Native interactive probes | Partial | Earlier native macOS captures showed the point palette, winner, retained anchor, live line and label without a `QPainter` warning or crash. Direct confirmation of 18-pixel attraction, discrete-only acquisition, and the final persistent-dimension pass remains pending. |
| Package CI | Passed | Core PR 1540 remains green. Viewer PR 233 passes build, coverage, policy, distributions, and all nine OS/Python quality jobs. |
| Framework integration | Passed | Framework PR 7 passes contracts and the exact source-installed Viewer gate. |
| Candidate artifacts | Not run | No compatibility claim is made for independently built candidate artifacts. Run this layer before artifact admission or release if that claim is required. |

## Next tasks

1. Reconfirm the new toolbar, Grid and Units layout, screen text, and scalar
   inspection interactively.
2. Obtain explicit decisions on Proposed ADRs 033–035 and 037–039.

## Approval gates

- Adding model, session, notebook, or host packages requires explicit approval.
- Session aggregation and Viewer new/open/save conveniences remain future work.
- Do not merge or publish without explicit approval.
