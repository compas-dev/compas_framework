# Title: How should algorithms and discretization controls be selected?

## Status

Accepted

## Context

The top-level geometry namespace exports policy objects such as `Delaunay`,
`ConstrainedDelaunay`, `Native`, and `UVGrid`. Some are empty dispatch flags;
others mix unrelated producer-specific controls into universal hierarchies.
Their names look like geometry constructors or algorithms even when they only
select an implementation.

## Options

1. Keep the strategy hierarchies and top-level exports.
2. Replace empty flags only, leaving the universal tessellation hierarchy.
3. Use named algorithm functions and explicit producer-specific keyword
   controls; use a small literal only where alternatives truly share a
   contract.

## Recommendation

Choose option 3.

Expose named triangulation operations such as `delaunay_triangulation`,
`constrained_delaunay_triangulation`, and
`conforming_delaunay_triangulation`. Their names perform the operation users
expect and their parameters expose only applicable controls. They return
structural vertex/triangle buffers under ADR 012.

All Delaunay operations are restricted to planar domains. Input coordinates
must lie in one plane within the documented geometric tolerance. An optional
explicit frame defines that plane; otherwise the operation uses its documented
default plane. The implementation must not silently flatten a curved domain
and describe the result as Delaunay. Any separate decision to add native 2D
coordinate input does not change this planarity contract.

Triangulation of non-planar polygons remains a separate polygonal operation,
including the existing `PolygonalSurface` capabilities. Support for slightly
curved domains is deferred and, if added, requires a separately named
approximation contract with explicit projection, deviation, and failure rules.

Keep `tessellate()` as a convenient producer of a `Tessellation`, but replace
the universal public strategy hierarchy with keyword-only controls owned by
each geometry producer. A no-argument call uses documented defaults for generic
scene conversion. Resolution counts, approximation bounds, and numerical
tolerances remain distinct and state their units.

Use separate named polygon-triangulation functions when algorithms have
different parameters. Use `method=Literal[...]` only when implementations
share the same input and option contract. Do not retain empty nominal flags or
nested policy objects without a demonstrated serialization requirement.

## Decision

Approved on 2026-11-04. Named functions replace dispatch-only strategy classes,
and parametric producers own explicit keyword-only discretization controls.
Resolution, approximation bounds, and numerical tolerance remain separate
concepts with documented units. Delaunay operations remain planar; curved
domain approximation is not part of the approved contract.

## Consequences

- `Delaunay()` no longer masquerades as an algorithm or result.
- The top-level geometry namespace loses policy/configuration nouns.
- Producers may expose different tessellation keywords because their controls
  are materially different.
- Existing strategy imports, serialization, tests, and documentation require
  direct migration on the C3 initiative branch.
- Resolution controls mesh density; approximation bounds limit geometric
  error; tolerance remains for numerical predicates and validation.

## Affected packages

`compas`, `compas_cgal`, `compas_occ`, documentation, examples, and typed
consumer fixtures.

## Verification

- Named operations dispatch to matching plugin hooks.
- Delaunay operations reject non-planar 3D input outside the documented
  tolerance and preserve accepted source coordinates.
- Non-planar polygon triangulation remains independent of Delaunay dispatch.
- Producer defaults support generic visualization conversion.
- Every public control has documented meaning, units, validation, and failure
  behavior.
- Removed strategy symbols are absent from exports and documentation.
- Equivalent core/backend operations retain matching signatures.

## Dependencies

- [012 — Structural triangle-mesh boundaries](012-structural-triangle-mesh-boundaries.md)
