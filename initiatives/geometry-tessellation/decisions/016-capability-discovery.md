# Title: Should tessellation expose runtime capability and error-schema APIs before they have consumers?

## Status

Accepted

## Context

ADR 004 introduced `tessellation_capabilities()`, `TessellationCapability`,
`ErrorContract`, and `ApproximationError` so callers could discover supported
strategies and distinguish requested, estimated, and guaranteed error.

The implementation audit found no production consumer of this API. Shape and
Surface operations validate strategies directly. The principal BRep backend,
`compas_occ`, does not implement the capability pluggable, so BRep discovery is
not operational outside isolated mocked tests. No tessellation operation
returns `ApproximationError`, and no backend currently supplies achieved-error
metadata through this schema.

Keeping the types would preserve a speculative contract whose shape has not
been tested by a real caller or backend result. Backward compatibility is not a
priority for this initiative.

## Options

1. Keep the complete discovery and error-schema API in anticipation of future
   consumers. This avoids later additions but commits COMPAS to an unused
   abstraction and a nonfunctional BRep discovery boundary.
2. Keep capability discovery but remove the unused error schema. This retains
   runtime discovery, although current producers already validate strategies
   and no caller uses discovery.
3. Remove the complete speculative API without replacement. Producers validate
   supplied strategies directly and document supported strategies statically.
   Runtime discovery and measured-error results return only with a concrete
   consumer and backend data.

## Recommendation

Choose option 3.

Remove:

- `Shape.tessellation_capabilities()` and
  `Surface.tessellation_capabilities()`;
- BRep and BRepFace capability forwarding methods;
- the `brep_tessellation_capabilities` pluggable;
- `TessellationCapability`, `ErrorContract`, and `ApproximationError`;
- corresponding exports, tests, documentation, and framework assertions.

Do not replace them with another discovery facade. Each producer accepts an
explicit strategy, validates it, and raises a precise `TypeError` or
`ValueError` when unsupported. Supported strategies are documented per
geometry type and backend. `Deflection` values remain requested targets and do
not imply measured or guaranteed error.

Retain all accepted strategy types, including `Adaptive`. A future runtime
capability or enriched error-reporting API requires a concrete consumer,
available backend information, and a separate ADR.

Upon acceptance, this decision supersedes the capability method and error
schema selected by ADR 004. ADR 010's broader rule remains: enriched operation
results are introduced only for a concrete operation and consumer, through a
separate decision.

## Consequences

- The public API becomes smaller and reflects only executable behavior.
- Strategy validation remains local to the operation that consumes it.
- Callers cannot query support in advance; they rely on documentation or handle
  precise validation errors.
- No error-strength vocabulary is reserved before a backend can report it.
- Core, BRep, framework integration, tests, documentation, and public exports
  require coordinated removal.
- There is no compatibility alias or deprecation period under ADR 013.

## Affected packages

`compas`, `compas_occ`, and `compas_framework` documentation and tests.

## Dependencies

- [003 — Strategy objects](003-strategy-objects.md)
- [004 — Error contracts](004-error-contracts.md), superseded in part if this
  decision is accepted
- [010 — Metadata and provenance](010-metadata-provenance.md)
- [013 — Compatibility](013-compatibility.md)
