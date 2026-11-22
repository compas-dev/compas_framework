# ADR 006: Rollout Scope and Package Admission

## Status

Accepted.

## Context

The inventory spans current reference packages, partially migrated COMPAS 3
packages, optional backends, host integrations, and many ecosystem packages.
An open-ended approval would make completion ambiguous and could activate
incompatible legacy plugins without repository ownership or runtime evidence.

## Options

1. Limit initial implementation to Waves 0–1 and require explicit admission
   for every later package.
2. Approve all inventoried waves as one initiative scope.
3. Implement only the reference packages and omit model and viewer.
4. Allow packages to enter implicitly when maintainers begin work.

## Recommendation

Choose option 1. Initial implementation and completion cover exactly:

- `compas`
- `compas_cgal`
- `compas_libigl`
- `compas_occ`
- `compas_model`
- `compas_viewer`

Optional backends, host integrations, and remaining ecosystem packages stay on
the roadmap. Adding any of them requires a documented scope amendment, package
ownership, compatibility evidence, and new user approval.

## Consequences

- Initial completion is finite and independently verifiable.
- Waves 2–4 do not block the initial initiative.
- Later packages cannot enter silently.
- An admitted host package must satisfy ADR 005 host evidence; unavailable
  validation leaves it incomplete.

## Affected packages

Initial scope: the six packages listed above. Later packages are affected only
after explicit admission.

## Dependencies

- [ADR 005](005-verification-and-evidence.md)
