# Title: How should partially supported BRep queries report their results?

## Status

Accepted

## Context

Typing the OCC BRep plugins exposed a semantic mismatch that annotations cannot
repair. Core currently groups classification and topology into complete records.
Their public properties promise semantic answers, including that a closed BRep
has no naked boundaries and that the topology record contains its parametric
trims.

The OCC implementation cannot currently satisfy the complete records:

- `TopoDS_Shape` orientable, closed, infinite, and convex flags are native
  shape flags, not demonstrated computations of the documented COMPAS
  predicates;
- manifoldness is hardcoded to `False`;
- OCC has no `BrepTrim` implementation and returns an empty trim list even for
  trimmed faces.

Casting these values to the core records makes Pyright pass while presenting
unknown or unsupported results as authoritative `False` or empty values. This
violates the approved rule that annotations and plugin results describe actual
public behavior.

## Options

1. Preserve the current OCC flags, hardcoded value, and empty trim list.
2. Change the record fields to optional values or make their keys optional.
3. Implement every promised classification algorithm and OCC trim type before
   exposing any BRep classification or topology query.
4. Keep truthful public properties, but separate unsupported semantic queries
   from grouped supported results. Implement a query only where the backend can
   satisfy its documented meaning; otherwise raise a documented
   `NotImplementedError` for that query alone.

## Recommendation

Choose option 4.

Unknown must not be represented as `False` or `[]`. Preserve the existing
public property meanings and isolate unsupported capabilities so that one
unsupported query, such as convexity, manifoldness, or trims, does not disable
reliable queries such as type, validity, vertices, edges, loops, faces, shells,
and solids.

The implementation should make the smallest core plugin-contract adjustment
that permits independent failure. It should not add a general capability
framework, compatibility aliases, or nominal runtime type checks. OCC should
implement each query only with a native operation or algorithm that is tested
against the documented COMPAS meaning.

WP3 may align and verify the other curve, surface, and BRep plugin signatures
independently. The OCC implementations of `brep_classification` and
`brep_topology` must follow this decision and must not encode the known
placeholders as truthful results.

## Consequences

- Unsupported BRep properties fail explicitly rather than silently returning a
  plausible but incorrect value.
- Supported topology and classification queries remain usable independently.
- Core and backend plugin contracts, tests, and documentation require a narrow
  coordinated update after approval.
- Full classification algorithms and an OCC trim representation can be added
  later without changing the meaning of existing boolean or list results.
- This may expose previously silent OCC limitations as documented runtime
  errors.

## Affected packages

`compas` and `compas_occ`.

## Dependencies

- [006 — Plugin conformance](006-plugin-conformance.md)
- [007 — Backend substitutability](007-backend-substitutability.md)
- [008 — Return normalization](008-return-normalization.md)
