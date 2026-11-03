# Title: How should adaptive requests and approximation guarantees be expressed?

## Status

Accepted — superseded by ADR 016

ADR 016 removes the runtime capability-discovery method and the unused
capability/error schemas selected here. This record remains as historical
rationale and is no longer implementation authority for those APIs.

## Context

Uniform core sampling has no error bound. OCC accepts kernel deflection values
but the wrapper performs no independent measurement. CGAL refinement exposes
maximum edge length while its native minimum-angle input is not currently
wired into criteria. No common API distinguishes a target, post hoc estimate,
or mathematically guaranteed bound.

The objective requires error-controlled strategies without overstating
guarantees. The proposal introduces `Adaptive` as request vocabulary but does
not assume a core adaptive algorithm already exists.

## Options

1. Treat every requested deviation/angle as a guaranteed bound. This is simple
   but inaccurate for current implementations.
2. Expose controls without describing their strength. This preserves backend
   freedom but gives callers no reliable contract.
3. Classify supported controls as target, estimated, or guaranteed, and reject
   unsupported fields. Introduce the `Adaptive` contract before or separately
   from any implementation.
4. Block all strategy work until one universal adaptive algorithm exists. This
   delays compatible count/deflection improvements unnecessarily.

## Recommendation

Choose option 3. Approve the interoperable `Adaptive` configuration contract,
but make the first adaptive implementation a separately reviewed slice.
Producers must state capability and guarantee level; unsupported requests must
fail rather than degrade silently.

Define the following error-contract values:

```python
class ErrorContract(Enum):
    NONE = "none"
    TARGET = "target"
    ESTIMATED = "estimated"
    GUARANTEED = "guaranteed"
```

Define two serializable `compas.data.Data` metadata types:

```python
class TessellationCapability(Data):
    strategy: str
    supported_parameters: tuple[str, ...]
    error_contract: ErrorContract


class ApproximationError(Data):
    linear: float | None = None
    angular: float | None = None
    contract: ErrorContract = ErrorContract.ESTIMATED
    method: str | None = None
```

`TessellationCapability.strategy` is the COMPAS dtype string of the supported
strategy. `supported_parameters` names exactly the public strategy fields the
producer implements. `ApproximationError.linear` is in model units;
`ApproximationError.angular` is in public degrees. When present, `method`
identifies how the value was assessed.

`ApproximationError` reports achieved or assessed error and is distinct from
the requested strategy. `TARGET` normally belongs on
`TessellationCapability`, because a target is not an achieved-error
measurement. `GUARANTEED` is used only when the backend actually guarantees
the stated bound. `NONE` states that no error contract is offered, while
`ESTIMATED` identifies a non-guaranteed assessment.

Every surface-like geometry instance exposes exactly one discovery method:

```python
geometry.tessellation_capabilities() -> tuple[TessellationCapability, ...]
```

Discovery is instance-level because the concrete geometry type and active
backend may change which `TessellationStrategy` subclasses and parameters are
supported. `TessellationCapability.strategy` stores the COMPAS dtype string of
that strategy. There is no parallel `supports_tessellation(...)` or other
convenience predicate; callers inspect the returned capability tuple.

If a future `TessellationReport` combines these metadata types with a
`Tessellation`, the report remains ephemeral because `Tessellation` is
ephemeral. ADR 010 defers such enriched-result APIs from the initial
implementation.

## Consequences

- APIs and docs cannot use “tolerance” or “guarantee” loosely.
- Error metadata has stable serializable fields, public model-unit/degree
  conventions, an assessment method, and an explicit contract class.
- Capability discovery is serializable and names strategy support without
  implying that requested values were achieved.
- Capability discovery is instance-specific and has one canonical method,
  avoiding duplicated convenience APIs with potentially inconsistent answers.
- Tests need backend-appropriate monotonicity and measurement assertions rather
  than identical connectivity.
- A later adaptive implementation needs dedicated singularity, trim, and error
  fixtures and does not block base interoperability work.
- Tests must prevent `TARGET` from being presented as achieved error and must
  reserve `GUARANTEED` for backends with a documented guarantee.
- No required `TessellationReport` API or persistent report serialization is
  authorized by this ADR.
- Tests must cover backend/type-dependent capability tuples, COMPAS dtype
  strings, exact supported-parameter names, and the absence of a second
  convenience discovery method.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, optionally `compas_gmsh`, and
`compas_framework`.

## Dependencies

- [001 — Terminology](001-terminology.md)
- [003 — Strategy objects](003-strategy-objects.md)
