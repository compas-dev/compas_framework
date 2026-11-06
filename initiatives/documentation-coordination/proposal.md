# Documentation Coordination Proposal

## Summary

Coordinate documentation across the ten active COMPAS 3 repositories through
declared authoritative examples, blocking static checks, representative
runtime evidence, consistent semantic navigation, canonical source ownership,
and contract-aware migrations. Keep the underlying Ruff/Pyright wiring in
repository modernisation and keep API behavior in the initiative that owns the
contract.

## Initial scope

The first wave contains only `compas`, `compas_cgal`, `compas_framework`,
`compas_gmsh`, `compas_libigl`, `compas_model`, `compas_occ`,
`compas_session`, `compas_shapeop`, and `compas_viewer`.

Gmsh and ShapeOp documentation follow their accepted modernisation contracts
and the behavior actually implemented on their initiative branches. Other
ecosystem and host repositories are roadmap candidates, not completion
criteria.

## Authoritative example model

Each repository declares every authoritative Python example root. Every Python
file under that root is authoritative by default, and each root or subtree has
one default category:

1. **static-and-smoke** — Ruff, Pyright, and deterministic headless execution;
2. **static-only interactive** — Ruff and Pyright plus documented manual
   behavior;
3. **static-plus-optional-runtime** — static checks in the declared dependency
   environment plus native/optional runtime evidence where supported;
4. **host-runtime** — meaningful static checks and mandatory host evidence once
   the package is admitted;
Record only exceptions to the root or subtree default. Draft and archive
material belongs outside authoritative roots and is excluded from published
navigation and blocking example gates.

`__temp`, ignored files, or directory names do not implicitly create a
category. Helper modules imported by authoritative examples enter the same
static gate.

Use `docs/examples/` as the normal root. Core may retain
`docs/assets/examples/` because its established documentation machinery treats
those files as executable assets. Any other exception requires a recorded
reason.

## Static and runtime verification

Every authoritative Python example participates in both Ruff and Pyright
through the owning repository's blocking commands. Whole-file ignores are not
an accepted solution. Narrow suppressions require an adjacent rationale tied
to an actual unsupported boundary. Casts remain only when they express real
narrowing.

Do not execute every example indiscriminately. Each repository declares a
representative headless smoke subset covering its primary documented workflow.
Smoke examples are deterministic, non-interactive, network-independent unless
separately authorized, use isolated temporary output, and assert meaningful
results. Optional, GUI, native, and host examples receive their appropriate
runtime evidence instead of being reported as ordinary headless successes.

## Version and migration contract

Documentation on a branch describes the package produced by that branch and
the dependency range it declares. Coordinated unreleased work uses exact
candidate pins. Released documentation does not describe candidate-only APIs
as available.

Migration preserves semantics, not just syntax. Explicit triangulators migrate
to equivalent named callables. Structural NumPy backend examples remain direct.
Producer controls retain their units and approximation meaning.
`Mesh.triangulated()` examples follow Accepted Geometry ADR 024 once its
representation-preserving implementation is present in the documented branch.
No compatibility alias is added solely to preserve an obsolete example.

## Information architecture

Every normal package site provides these semantic destinations:

1. Overview;
2. Installation;
3. Getting started or tutorial;
4. Examples/how-to guides;
5. Concepts/background where needed;
6. API Reference;
7. Development/contributing guidance;
8. Changelog;
9. License.

Use `docs/reference/` for newly organized API reference pages. Existing
`docs/api/` trees may migrate during their package's coordinated update; do not
maintain both trees as competing sources.

Core is an explicit structural exception. It may retain its deeper nested
getting-started and reference hierarchy, but it supplies the same semantic
destinations and meets the same quality gates. The exception concerns depth
and filenames, not content obligations.

## Canonical source ownership

Every executable example has one canonical `.py` source. Documentation pages
include or link it rather than maintain a second runnable copy. Small inline
snippets may remain when they are not presented as complete programs.
Substantial runnable snippets are extracted so the exact code users see enters
Ruff, Pyright, and the applicable runtime category.

## Documentation migration records

Every coordinated migration records:

- the old and new idiom;
- any change to behavior, algorithm, mutation, representation, units,
  dependency, or runtime requirement;
- the affected pages and examples;
- the commands and environments that verify the result.

Mechanical replacement is allowed only when semantics are equivalent. Public
behavior changes update docstrings, API pages, examples/tutorials, and
changelog coverage together.

## Verification contract

For every admitted repository:

- strict MkDocs passes without unexplained warnings;
- Ruff and Pyright enumerate every authoritative Python example;
- the declared headless smoke subset passes;
- optional/native examples pass their declared runtime job or remain
  explicitly unverified;
- doctests pass where present;
- generated files use isolated temporary directories;
- navigation, links, includes, and example references resolve;
- public signatures match the built package;
- obsolete APIs, strategy names, and whole-file suppressions are absent;
- documentation and changelog describe the same public contract; and
- independent review finds no unresolved factual or cross-package mismatch.

Cross-package documentation builds use the same exact candidate set as runtime
and typing integration.

## Rollout

1. Accept ADRs 001–009.
2. Freeze the active-ten example inventory and classifications.
3. Let repository modernisation complete Ruff/Pyright enumeration.
4. Resolve final typing and geometry contracts before affected example
   migrations.
5. Normalize page responsibilities and canonical sources in
   modernization-ready repositories.
6. Add representative headless smoke subsets.
7. Run cross-package terminology, API, links, and candidate-version review.
8. Admit later packages only through the approved admission contract.

## Alternatives

### Absorb documentation into repository modernisation

Rejected. Tooling and documentation quality have different ownership and
lifecycles. Modernisation should provide the gate; this initiative governs the
content exposed by it.

### Include the complete ecosystem immediately

Rejected. Many repositories lack confirmed COMPAS 3 compatibility, active
ownership, or modern documentation infrastructure.

### Require identical file trees everywhere

Rejected. It would create URL churn and make core harder to navigate without
improving semantic consistency.

### Run every example in ordinary CI

Rejected. Interactive, native, optional, GUI, and host examples require
different environments. A declared representative smoke subset is more
truthful and maintainable.

### Static checking only

Rejected. Static tools do not prove imports, renamed APIs, file ownership, or
meaningful runtime results.

## Compatibility implications

- Published URLs may change when `docs/api/` migrates to `docs/reference/`;
  package-specific migrations should preserve redirects where required by an
  approved release policy.
- Stale examples may stop working until their owning API initiative lands; they
  remain explicitly pending rather than receiving compatibility shims.
- Exact candidate pins prevent unreleased cross-package examples from being
  mistaken for released behavior.
- Native and host packages cannot claim completion without their actual runtime
  evidence.

## Approval boundary

ADRs 001–009 are Accepted. Their approval authorizes only the active-ten
rollout described above. It does not authorize later ecosystem admission,
merges, publication, deployment, or repository-setting changes.
