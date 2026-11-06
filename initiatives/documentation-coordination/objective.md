# Documentation Coordination Initiative

## Objective

Establish one coherent, verifiable documentation experience across the active
COMPAS 3 framework repositories. Coordinate public prose, tutorials, examples,
API-reference organization, terminology, and documentation quality without
turning documentation coordination into a second owner of public API design or
repository tooling.

The initial scope contains exactly these ten repositories:

- `compas`;
- `compas_cgal`;
- `compas_framework`;
- `compas_gmsh`;
- `compas_libigl`;
- `compas_model`;
- `compas_occ`;
- `compas_session`;
- `compas_shapeop`;
- `compas_viewer`.

Later ecosystem and host-integration repositories enter only through an
explicitly approved admission decision.

## Ownership boundary

- Repository modernisation owns making every authoritative executable Python
  example visible to Ruff and Pyright in the active ten repositories.
- Documentation coordination owns which examples are authoritative, how they
  are organized and taught, their technical accuracy, their canonical source,
  and the documentation structure around them.
- Geometry, typing, plugin, viewer, model, and other API initiatives own the
  contracts being documented.
- The skills and agent-configuration initiative may guide users through
  tutorials, but versioned package documentation remains the factual source of
  truth.

## Questions to resolve

1. Which repositories and documentation surfaces enter the first wave?
2. Which example files are authoritative and which verification category does
   each belong to?
3. Which static and runtime gates are required for executable examples?
4. Which package and COMPAS version must an example describe and test?
5. Which documentation destinations and page responsibilities must be
   consistent across packages?
6. When may core or another package retain a deeper or different information
   architecture?
7. Where is the canonical source of an example shown in multiple places?
8. How are semantically significant API migrations distinguished from
   mechanical documentation cleanup?
9. What evidence is required before a later package or host integration enters
   scope?

## Design principles

- Document implemented and approved behavior, never speculative APIs as
  available features.
- Preserve algorithm selection, mutation, units, approximation controls,
  tolerances, runtime requirements, and known limitations during migrations.
- Use MkDocs/mkdocstrings-compatible NumPy-style docstrings with Markdown.
- Prefer one canonical executable example over copied variants or duplicated
  snippets.
- Include authoritative Python examples in both Ruff and Pyright.
- Execute a representative deterministic headless subset rather than treating
  every interactive, native, or host example as an ordinary smoke test.
- Write generated files only to isolated temporary directories.
- Keep raw NumPy and structural backend examples when they demonstrate a valid
  public boundary; do not force unnecessary core-object conversions.
- Keep documentation structure semantically consistent without imposing one
  shallow directory layout on packages of very different size.

## Deliverables

1. A cross-repository inventory of documentation builders, information
   architecture, examples, static gates, runtime gates, obsolete idioms,
   suppressions, and source duplication.
2. An approved architecture and independent ADRs.
3. An authoritative example manifest and classification for every in-scope
   repository.
4. Consistent semantic navigation and page responsibilities.
5. One canonical source for every executable example.
6. Blocking static checks and declared runtime evidence for authoritative
   examples.
7. Coordinated migration guidance for approved cross-package API changes.
8. Cross-package documentation, link, version, and terminology verification.

## Non-goals

- Redesigning public APIs in documentation.
- Retaining removed APIs through compatibility aliases solely for examples.
- Immediately migrating the complete COMPAS ecosystem.
- Treating ordinary CPython CI as evidence for Rhino, Blender, Grasshopper, or
  another host runtime.
- Requiring screenshots or golden images for every example.
- Introducing notebooks or generated Markdown as a new universal source
  system without a separate approved requirement.
- Merging, publishing, deploying documentation, or changing repository
  settings without explicit approval.

## Dependencies

Repository modernisation supplies package commands, locks, workflows, and the
active-wave Ruff/Pyright example gates. Typing ADRs 015–017 and Geometry ADRs
022–024 govern the structural buffers, triangulation, and conversion examples.
Gmsh ADRs 014–016 and ShapeOp ADRs 017–019 gate implementation in those
repositories. Plugin, viewer, and model initiatives own their corresponding
public contracts.

## Current status

Phase 1 reconnaissance and Phase 2 architecture are complete. ADRs 001–009 are
Accepted, and the active-ten implementation is authorized subject to the
existing merge, publication, deployment, and repository-setting boundaries.
