# Title: How should plugins discover and consume the unified triangle-mesh contract?

## Status

Accepted

## Context

COMPAS discovers plugins through the `compas.plugins` entry-point group.
`compas_occ` declares current entry points; `compas_cgal` retains an unused
legacy `__all_plugins__` list and lacks the inspected entry-point table. CGAL
and libigl also repeat native array conversion, with CGAL public aliases using
`int64` while wrappers commonly marshal `int32`.

Relevant sources include `../compas/src/compas/plugins.py`,
`../compas_cgal/pyproject.toml`, `../compas_cgal/src/compas_cgal/types.py`, and
`../compas_libigl/src/compas_libigl`.

## Options

1. Keep package-local public input contracts and direct APIs. This minimizes
   initial work but preserves multiple competing public surfaces.
2. Put NumPy-native array requirements in core. This centralizes conversion
   but imposes backend storage policy on general geometry representations.
3. Use current entry-point discovery, exact compatible plugin signatures, core
   `Tessellation` validation/buffer extraction, and package-local native
   coercion/validation helpers.
4. Replace the plugin mechanism with a new strategy registry. This duplicates
   existing infrastructure and expands scope.

## Recommendation

Choose option 3. CGAL must add current discovery metadata and register intended
decorated modules. Core owns validation and buffer extraction from
`Tessellation`; it does not own a heterogeneous representation adapter. CGAL
and libigl package helpers own NumPy dtype, layout, range checks, and conversion
to native inputs. Operation-specific topology validation remains explicit. The
core pluggable is the public API; backend functions implement that exact
signature and result contract but are not maintained as a second, divergent
high-level API.

## Consequences

- Plugin dispatch becomes testable through core APIs.
- Existing callers of divergent direct CGAL/libigl high-level functions must
  move to the core API; backend modules may expose clearly low-level native
  bindings, but not alternate semantic contracts.
- Runtime annotations must match actual native dtypes.
- Compatible buffers can avoid unnecessary copies, but coercion cannot promise
  zero-copy when dtype/layout changes.
- Entry-point tests and optional-backend skip behavior become framework-level
  contracts.
- Operation-specific enriched public results are deferred from the initial API
  by ADR 010. Low-level internal native data may still exist, but it is not a
  public contract.

## Affected packages

`compas`, `compas_cgal`, `compas_libigl`, `compas_occ`, and
`compas_framework`.

## Dependencies

- [008 — Triangle interoperability](008-triangle-interoperability.md)
- [011 — Planar triangulation contract](011-planar-triangulation-contract.md)
