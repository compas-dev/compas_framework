# Documentation Coordination Inventory

Inventory date: 2026-11-06.

## Audited scope

The audit covered the ten active repository-modernisation repositories and a
later-wave ecosystem sample under `/Users/vanmelet/Code`. Temporary worktrees,
build output, sites, environments, and Git internals were excluded from file
counts.

## Executable example coverage

The active ten contain 160 standalone Python example files:

| Repository | Current example root | Files | Ruff includes examples | Pyright includes examples |
|---|---|---:|---|---|
| `compas` | `docs/assets/examples` | 17 | Yes | No |
| `compas_cgal` | `docs/examples` | 28 | Yes | No |
| `compas_framework` | None | 0 | N/A | N/A |
| `compas_gmsh` | `docs/examples` | 4 | No | No |
| `compas_libigl` | `docs/examples` | 16 | Yes | Yes |
| `compas_model` | `examples` | 14 | No | No |
| `compas_occ` | `docs/examples` | 44 | Yes | No |
| `compas_session` | None | 0 | N/A | N/A |
| `compas_shapeop` | `examples` | 7 | No | No |
| `compas_viewer` | `docs/examples` | 30 | No | No |

Only `compas_libigl` currently exposes its example tree to both static tools in
the visible checkout. Several repositories delegate to shared Invoke tasks
whose default Ruff scope is only `src tests`; those tasks do not prove example
coverage.

The later ecosystem contains another 141 standalone Python examples across 18
repositories. No later-wave example tree has a discovered Pyright gate. This
evidence supports a bounded active-ten rollout rather than silently admitting
the complete ecosystem.

## Known stale or inconsistent idioms

The audit found examples that still depend on the pre-initiative geometry
surface, including:

- `Point(*mesh.vertex_attributes(vertex, "xyz"))` instead of the high-level
  `mesh.vertex_point(vertex)` accessor;
- copy-plus-mutating triangulation instead of the final approved
  `mesh.triangulated(...)` contract;
- `FaceTriangulation`, `DiagonalSplit`, and `EarClipping` strategy objects;
- `Native`, `UGrid`, `UVGrid`, and `Deflection` conversion strategies;
- `.polygonize(...)` and `.tessellate(...)` rather than the approved producer
  conversions;
- examples that use explicit algorithms but would change behavior if migrated
  mechanically to a default triangulator.

Examples using raw coordinate/index arrays or `(vertices, faces)` tuples are
not intrinsically stale. CGAL and libigl expose valid structural numerical
boundaries, and those examples should remain direct rather than construct core
geometry objects merely for documentation uniformity.

## Suppressions and narrowing

The active examples contain 50 `# type: ignore` directives in the audited
checkouts:

- core: 13;
- CGAL: 1;
- Gmsh: 1;
- libigl: 3;
- OCC: 29;
- viewer: 3.

Many core and OCC directives are whole-file or broad suppressions. Model has
eight example `cast(...)` calls. Some casts may express real narrowing of a
broad model contract; they require contract-aware review rather than blanket
removal.

## Documentation builders and organization

Eight active repositories use MkDocs in the visible checkouts. Session and
ShapeOp still use Sphinx there, although isolated modernization work has
already converted Session and ShapeOp remains approval-gated.

API reference roots are inconsistent: core and model use `reference`, while
several other packages use `api`. Executable examples appear under
`docs/examples`, `docs/assets/examples`, or root-level `examples`.

Against the existing `update-docs` skill's expected page responsibilities:

- Gmsh, model, and OCC have overview, installation, license, changelog, and
  tutorial pages;
- CGAL lacks a tutorial page;
- framework lacks top-level changelog and tutorial pages;
- libigl and viewer lack changelog pages;
- core has a deliberately deeper nested information architecture rather than
  the small-package filename pattern.

The inconsistency is not purely cosmetic. Some packages have substantial
example collections but skeletal tutorials, while others duplicate or route
content without a clearly declared canonical source.

## Version and dependency risks

The visible checkouts do not all target the same landed geometry contract.
Examples may therefore be current for their checked-out dependency while stale
relative to the approved COMPAS 3 target. Final migrations must use exact
candidate pins until the coordinated API is released, and released
documentation must not present candidate-only behavior as generally
available.

Native, GUI, optional-backend, and host examples require their actual runtime
or an explicit unverified classification. Static success alone does not prove
PythonOCC, CGAL, libigl, Qt/OpenGL, Rhino, Blender, or Grasshopper behavior.

## Existing useful patterns

- Strict MkDocs builds already exist in several modernized repositories.
- Core's executable asset pattern supports one source file included by prose.
- Native packages already have separate runtime jobs that can host optional
  example evidence.
- Repository-modernisation ADR 011 requires executable examples to enter Ruff
  and Pyright, so this initiative can define the inventory while modernization
  owns the underlying active-wave tool setup.
- The repository-local `update-docstrings` and `update-docs` skills encode the
  required Markdown/NumPy docstring style and computational-methodology
  documentation expectations.

## Architecture decisions required

1. Initial repository scope and cross-initiative ownership.
2. Authoritative example roots and explicit example categories.
3. Blocking Ruff/Pyright policy and suppression rules.
4. Representative headless runtime smoke evidence.
5. Branch, package, dependency, and API version baseline.
6. Framework documentation page responsibilities and core's structural
   exception.
7. Canonical source ownership for examples and snippets.
8. Contract-aware migration and review policy.
9. Later-wave and host-package admission.

## Risks

1. Documentation cleanup silently changes algorithms or result semantics.
2. Examples type-check against a different dependency version than users run.
3. Copied examples diverge and only one copy is verified.
4. Whole-file suppressions conceal stale public APIs.
5. A uniform shallow file layout makes core navigation worse without improving
   consistency.
6. Native or host documentation is reported complete without runtime evidence.
7. Documentation coordination duplicates API ownership instead of consuming
   accepted contracts.
