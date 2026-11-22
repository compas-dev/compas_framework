# Title: Which abstraction owns tessellation of trimmed NURBS surfaces?

## Status

Accepted

## Context

Core `NurbsSurface` stores the underlying parametric surface but no trim loops.
`BrepFace` owns ordered boundary loops, orientation, and the supported surface.
OCC's BRep mesher tessellates actual trimmed faces, whereas
`OCCBrep.to_meshes(u, v)` samples underlying rectangular surface domains and
does not visibly apply trims.

Relevant sources are
`../compas/src/compas/geometry/surfaces/nurbs.py`,
`../compas/src/compas/geometry/brep/face.py`, and
`../compas_occ/src/compas_occ/brep/brep.py`.

## Options

1. Add trim loops to `NurbsSurface`. This gives one surface API but conflates
   geometry with BRep topology and changes serialization across backends.
2. Pass optional trim loops to generic surface tessellation. This is flexible
   but creates an unowned trim representation and difficult orientation rules.
3. Keep standalone `NurbsSurface` explicitly untrimmed; place trim-aware
   tessellation on `BrepFace`/`Brep`, using their topology and orientation.
4. Introduce a new `TrimmedSurface` abstraction first. This may eventually be
   useful but is a larger unproven hierarchy change.

## Recommendation

Choose option 3. Add/standardize trim-aware tessellation on BRep owners and
document that extracting the underlying NURBS surface loses trimming context.
Do not invent generic trimmed-surface ownership in this initiative.

## Consequences

- OCC can use its native trimmed-face mesher without flattening topology into a
  surface object.
- Generic `NurbsSurface.tessellate(strategy)` remains a rectangular-domain
  operation.
- BRep results must preserve face winding and relevant boundary polylines.
  Trim/source provenance is deferred by ADR 010 and requires a future ADR and
  separately named operation-specific API.
- Tests need holes, curved trims, reversed faces, boundaries, seams, and
  watertightness assumptions.
- Documentation must warn that underlying-surface conversion is not
  trim-preserving.

## Affected packages

`compas`, `compas_occ`, `compas_model`, and `compas_framework`.

## Dependencies

- [003 — Strategy objects](003-strategy-objects.md)
- [004 — Error contracts](004-error-contracts.md)
- [006 — Tessellation API](006-tessellation-api.md)
