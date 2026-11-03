# Title: What guarantees should bounding boxes of continuous geometry provide?

## Status

Accepted

## Context

`Geometry.aabb` and `Geometry.obb` are abstract properties. `Shape` currently
implements both by applying point-cloud bounding-box algorithms to vertices
from its default discretization. Consequently the result depends on stored
resolution and may fail to enclose the continuous curved geometry. `Surface`
does not currently implement either property.

The analytic parameters and frame provide exact world-axis extrema for `Box`,
`Cylinder`, `Cone`, `Sphere`, `Torus`, and `Capsule`, without tessellation.
Closed-form full-domain extrema are also available for the analytic surface
types, although partial domains are substantially more complex. A NURBS
surface needs a certified backend result or validated convex-hull assumptions;
ordinary UV sampling cannot guarantee containment.

The existing oriented-bounding-box function promises minimum volume. A
deterministic box aligned with a shape's parameter frame is an exact enclosure,
but is not proven to be the global minimum-volume box for every shape.

## Options

1. Continue deriving bounds from an implicit default tessellation. This is
   simple but resolution-dependent and cannot guarantee containment.
2. Define `aabb` as a strategy-free continuous enclosure, while retaining the
   minimum-volume meaning of `obb` and reporting unsupported cases honestly.
3. Define both properties analytically, but redefine `obb` to mean the
   deterministic parameter-frame enclosure. This is broadly implementable but
   silently weakens the existing minimum-volume contract.
4. Require a discretization strategy for all bounds. This makes approximation
   explicit but makes bounds approximate operations rather than properties of
   the continuous geometry.

## Recommendation

Choose option 2.

Define `aabb` as a strategy-free `Box` guaranteed to enclose the continuous
geometry and tight along world XYZ where an exact analytic implementation is
provided. It must never use an ordinary tessellation or sampling resolution.

Implement exact parameter-derived AABBs for `Box`, `Cylinder`, `Cone`,
`Sphere`, `Torus`, and `Capsule`, including rotated frames and supported
degeneracies. Implement exact full-native-domain AABBs for `PlanarSurface`,
`CylindricalSurface`, `ConicalSurface`, `SphericalSurface`, and
`ToroidalSurface`. Do not add domain arguments to the property; partial-domain
bounds, if required, are a separate future operation. Unbounded domains must
raise a clear unsupported or unbounded error rather than being sampled.

For `NurbsSurface`, return an AABB only when the implementation can certify a
continuous enclosure: through a backend-provided certified bound or a
control-net convex-hull bound whose required weight assumptions have been
validated. Such a result may be conservative and must be documented as such.
If no guarantee can be established, raise `NotImplementedError`.

Retain the minimum-volume semantic meaning of `obb`. Initially implement it
only where the continuous minimum-volume result is established, such as `Box`
and `Sphere`; leave other continuous shapes and surfaces unsupported. Do not
fall back to hidden tessellation. If a parameter-frame enclosure gains a
concrete consumer, introduce it separately instead of weakening `obb`.

## Consequences

- Bounding results no longer depend on resolution or caches and cannot
  under-bound curves merely because extrema fall between sample points.
- AABB tests must cover rotated frames, exact extrema, containment, parameter
  changes, and permitted degeneracies.
- Surface tests must distinguish exact finite, unbounded, conservative, and
  unsupported results.
- NURBS documentation must state tightness, containment guarantees, and weight
  or backend assumptions.
- Existing sampled `Shape.obb` behavior is removed; several continuous types
  initially have no `obb` implementation.
- Parameter-frame enclosures and partial-domain bounds remain separate future
  APIs rather than being conflated with `obb` or tessellation.

## Affected packages

`compas` and geometry backends that can certify NURBS bounds, initially
`compas_occ`.

## Dependencies

- [014 — Continuous geometry materialization](014-continuous-geometry-materialization.md)
