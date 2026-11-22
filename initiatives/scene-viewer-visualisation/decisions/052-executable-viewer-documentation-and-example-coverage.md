# ADR 052: Executable Viewer Documentation and Example Coverage

## Status

Accepted on 2026-11-14. Implemented and locally verified in the uncommitted
Viewer working tree based on `0f263f1`; no runtime change is authorized by this
decision.

## Context

The initiative now has a broad public surface spanning scene and data
inspection, Viewer configuration, selection and transforms, annotations,
serialization, overlays, dynamic updates, and optional geometry backends.
Documentation has grown alongside individual runtime decisions, but the
initiative has not decided what makes that documentation authoritative,
executable, or sufficiently complete.

This is independent of the runtime ownership decisions. Accepted ADR 049 owns
setup-time sidebar and settings composition. Accepted ADR 050 owns the Data
Details expansion, and Accepted ADR 051 owns the Scene Object Details
expansion. This decision governs only how implemented and verified
behavior is documented. It cannot introduce, amend, or complete those runtime
contracts.

An uncommitted candidate already replaces the placeholder tutorial, adds an
executable Viewer Settings example, corrects the Object Inspection composition
example, and improves affected public docstrings and Python 3.12 annotations.
That work is evidence for this proposal, not an Accepted decision or a
completed documentation program.

## Options

1. Adopt one maintained executable documentation contract with a canonical
   tutorial, focused workflow examples, and layered automated and manual
   verification.
2. Continue adding ad-hoc prose and examples with no common coverage or
   execution contract.
3. Publish one prose-only tutorial and leave examples illustrative.
4. Require a separate executable example for every public symbol.

## Recommendation

Choose option 1.

Maintain one end-to-end Viewer tutorial backed by one authoritative runnable
script under `docs/examples/`. The tutorial should provide the shortest useful
path through the current Viewer architecture and link to focused examples for
deeper workflows. The script, not a duplicated code block, is the tutorial's
source of executable code.

Examples should cover approved public feature areas at workflow or category
level. They do not need to demonstrate every class, method, field, or private
helper. Each example should use the public API that a user is expected to use,
end in a directly runnable result, and remain small enough for its ownership,
inputs, mutation, and expected outcome to be clear.

Public APIs changed or added by this initiative, and Python APIs touched while
maintaining their documentation, should have MkDocs/mkdocstrings-compatible
NumPy-style docstrings and Python 3.12 annotations. Documentation-facing
signatures, examples, and annotations must agree. Private helpers need
docstrings or additional annotations only when their behavior or boundary is
otherwise unclear; exhaustive private coverage is not required.

Documentation claims must describe implemented, verified behavior. A runtime
gap discovered while writing or executing documentation returns to the ADR
that owns that behavior. Documentation work must not patch a gap
speculatively, invent an alias, or present ADR 050 or ADR 051 behavior as
available before the relevant decision is implemented and verified.

## Required Coverage

The maintained tutorial and focused examples should jointly cover the current
major public areas as follows. “Automated evidence” is representative rather
than a promise that a headless environment proves native rendering or focus.

| Area | Required documentation and example coverage | Automated evidence | Separate native or optional evidence |
|---|---|---|---|
| Scene/content domains and inspection boundaries | Explain Scene, Data, and Annotations ownership; distinguish Object Settings, Object Details, Data Details, editable opt-in Scene Attributes, and Viewer Settings; update the inspection material only when ADR 050 or 051 behavior is implemented | Run the authoritative tutorial script and representative inspection/composition examples headlessly; assert the advertised components are actually present | Report modal/modeless focus, scrolling, selection, and visual layout separately |
| Viewer Settings and configuration | Show configuration values, `sidebar_items` and `settings_items` setup-time composition, first-construction singleton behavior, section navigation, reuse, and the difference between persistent configuration and transient window state | Execute the tutorial/Viewer Settings example; check effective copied composition and supported section behavior | Report modeless focus, Escape ownership, high-DPI layout, and native reuse separately |
| Selection, transforms, and refresh | Show shared selection concepts, public transform operations, and the geometry/appearance/transform refresh categories used by dynamic callbacks | Execute representative scripts and assert callback refresh categories without entering the visible event loop | Confirm viewport picking and visual transform results separately where needed |
| Measurements and annotations | Show transient measurement versus durable annotations, fixed/associative ownership, snapping restrictions, format defaults, and durable style/state | Run representative construction and contract tests without claiming that offscreen execution proves interaction or rendering | Report point acquisition, focus, placement, label/background, and rendering checks separately |
| Serialization | Show supported scene and annotation round trips, retained identity/reference behavior, and the exclusion of transient Viewer state | Execute representative round-trip or contract tests | Label backend- or renderer-dependent outcomes explicitly |
| Overlays | Show public scale, legend, and screen-text workflows plus their transient ownership | Perform construction/state smoke checks where meaningful | Verify visual placement, contrast, and resizing in a supported native renderer |
| Dynamic examples | Show public callbacks and categorized refresh for geometry, appearance, and transforms | Execute callbacks and assert the requested public refresh operations | Verify animation cadence and visible results separately |
| Optional geometry backends | Keep BRep, NURBS, and similar examples on stable COMPAS facades and state the required optional backend | Require static Ruff/Pyright checks; run only when the declared optional dependency is available | Label unavailable optional runtime evidence rather than treating it as a pass |

The matrix is a category contract. It does not require one page per API symbol,
one smoke test per example, or runtime execution of an optional backend that is
not installed.

## Executability and Verification

All authoritative Python examples live under `docs/examples/` and are checked
with the package's configured Ruff and Python 3.12 Pyright commands. Drafts,
archives, and intentionally incomplete fragments must stay outside that tree
or be clearly excluded by the documented gate rather than silently skipped.

The documentation suite should provide:

- representative headless smoke or contract tests for the canonical tutorial
  script and important workflow categories;
- focused assertions that examples advertise effective behavior, not merely
  import or construct dead definitions;
- focused doctests where public docstrings contain executable examples;
- strict MkDocs builds with navigation, internal-link, and snippet-path
  validation, plus `git diff --check`; and
- explicit reporting of offscreen skips, unavailable optional dependencies,
  and checks that were not run.

Headless tests prove construction and contracts only. Native OpenGL rendering,
visual presentation, platform focus, keyboard behavior, scrolling, and
high-DPI behavior remain separate manual or native-platform evidence. A pass in
one layer must not be used to infer a pass in the other.

## Maintenance and Failure Ownership

`compas_viewer` owns the Viewer tutorial, Viewer examples, rendered API pages,
and their package-local checks. A public behavior change is incomplete until
its owning runtime ADR, code, tests, types, docstrings, tutorial or focused
example coverage, and applicable verification evidence agree.

A failing example is maintained with the public workflow it demonstrates. If
the documented contract is wrong, fix the documentation. If the implementation
violates an accepted contract, return the failure to the owning runtime ADR and
tests. If the desired behavior is not accepted, propose or amend an ADR before
changing runtime code. Optional-dependency failures should identify the
missing backend and remain distinct from failures in the default supported
environment.

`compas_framework` may verify representative cross-package documentation
contracts, but it does not become the owner of Viewer prose or examples.

## Alternatives and Tradeoffs

Ad-hoc prose and examples have the lowest immediate cost, but they do not
identify stale scripts, missing feature areas, or claims that outrun runtime
behavior.

A prose-only tutorial provides a coherent narrative but duplicates code that
can drift and offers no executable evidence that the demonstrated workflow
still builds.

An example for every public symbol maximizes enumeration but creates a large,
repetitive maintenance surface. It also encourages artificial snippets instead
of the public workflows users need. Focused category coverage plus API
reference documentation is simpler and more durable.

The recommended layered approach has a modest test and maintenance cost. It
accepts that headless automation cannot prove native visual behavior and makes
that limitation explicit instead of hiding it.

## Compatibility

This decision is documentation-only. It changes no runtime API, behavior,
schema, serialization, configuration, ownership boundary, compatibility alias,
or migration requirement. Docstrings and annotations must describe the
existing public contract without changing runtime semantics.

## Implementation Evidence

The uncommitted Viewer working tree now contains the maintained end-to-end
tutorial backed by `docs/examples/ui/viewer_settings.py`, focused workflow
examples and a coverage matrix for every required category, updated navigation
and prose, and aligned public docstrings and Python 3.12 annotations. The
documentation-example suite passes 20 tests, including effective Viewer
Settings composition, Object/Data inspection, serialization, measurements,
and overlays. All `docs/examples/` Python passes Ruff, formatting, and Pyright;
the strict Viewer MkDocs build and `git diff --check` pass.

The independent review found the runtime and documentation structure sound and
requested follow-up coverage for durable annotation serialization plus two
wording/status corrections. Those findings were corrected and revalidated in
the working tree. Native OpenGL rendering, picking, focus, scrolling, high-DPI
layout, animation cadence, overlay placement, and optional BRep/NURBS backend
execution remain separately reported evidence rather than inferred passes.

## Dependencies

- Documents implemented behavior governed by Accepted ADRs 001–049 without
  changing their ownership or runtime contracts.
- ADR 049 remains the sole owner of setup-time Viewer composition and settings
  behavior.
- ADRs 050 and 051 remain independent Accepted runtime decisions. Their
  behavior enters documentation only after it is implemented and verified.
- ADR 052 may be implemented and verified independently of ADRs 050 and 051,
  except for documentation that describes their runtime behavior.

## Acceptance Scope

The user accepted the executable documentation contract, category coverage
matrix, and layered verification boundary on 2026-11-14. Acceptance authorizes
documentation, docstring, annotation, example, and documentation-test
maintenance only; it does not authorize any runtime behavior change or by
itself establish that the documentation program is complete.
