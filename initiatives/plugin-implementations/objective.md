# Plugin Implementations Initiative

## Objective

Establish one simple and verifiable pattern for plugin implementations across
the COMPAS framework. Installed packages should use the current core plugin
manager through explicit package entry points, lightweight registration
modules, lazy implementation imports, exact core contracts, and tests that
prove both discovery and invocation behavior.

The initiative consolidates existing mechanisms. It does not introduce a new
registry, plugin-specific geometry representations, compatibility scanning, or
dependency-resolution layer.

## Questions to resolve

1. Which discovery metadata is authoritative for installed packages?
2. What may a registration module import during ordinary discovery?
3. How must wrappers conform to core extension-point signatures and results?
4. When may a backend keep a directly importable implementation API?
5. How should optional native, GUI, notebook, and host runtimes affect
   registration, selection, and failure?
6. Which source, installed-metadata, wheel, and host-runtime tests are required
   before a package is considered migrated?
7. How should current packages and legacy ecosystem packages be sequenced?

## Design principles

- Use the existing `compas.plugins` entry-point group as the one installed
  discovery path.
- Keep registration modules lightweight and organized by core plugin category.
- Import implementations and optional runtimes only when a plugin is invoked.
- Preserve current core data and result contracts; do not invent plugin-only
  representations or adapters.
- Prefer exact visible wrappers over generated metadata or compatibility
  layers.
- Keep direct backend APIs only when useful and semantically consistent.
- Treat import-free discovery and usable invocation as separate contracts.
- Require host-specific evidence for host integrations.

## Deliverables

1. A cross-package inventory of discovery metadata, wrappers, implementation
   imports, tests, documentation, and compatibility risks.
2. An approved architecture and independent ADRs.
3. Reference verification in core, CGAL, libigl, and OCC.
4. A dependency-ordered initial migration of the six proposed Wave 0–1
   packages: `compas`, `compas_cgal`, `compas_libigl`, `compas_occ`,
   `compas_model`, and `compas_viewer`.
5. Canonical contributor guidance and package-specific migration notes.
6. An inventoried but unapproved roadmap for optional backends, host
   integrations, and remaining active ecosystem packages.

## Non-goals

- Replacing `PluginManager` or the entry-point mechanism.
- Restoring installed-package scanning or `__all_plugins__` compatibility.
- Changing geometry, tessellation, triangulation, or scene data models.
- Resolving unrelated algorithm correctness or native ABI work.
- Enabling incompatible legacy hooks merely by adding metadata.
- Treating archived or duplicate checkouts as release targets.
- Treating optional, host, or remaining ecosystem packages as part of the
  initial completion criteria without a scope amendment and new approval.

## Dependencies

Stable extension-point signatures from the typing-alignment and geometry work
are prerequisites for migrating corresponding implementations. Repository
modernization provides packaging, wheel, and CI infrastructure used by the
verification gates. Model, viewer, and documentation initiatives must
coordinate ownership where their files overlap. If a host package is admitted
later, host-runtime evidence is required; unavailable host validation means
that package remains incomplete.

## Current status

Reconnaissance and architecture are complete. The proposal and ADRs 001–006
await explicit approval. No implementation may begin before approval.
