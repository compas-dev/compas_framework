# ADR 006: Framework Documentation Information Architecture

## Status

Accepted.

## Context

Documentation sites use different page names, reference roots, tutorial depth,
and navigation. Requiring identical files would fit small packages poorly and
would flatten core's established structure.

## Options

1. Standardize semantic destinations while allowing depth to vary.
2. Require identical filenames and directories everywhere.
3. Standardize MkDocs configuration only.
4. Leave each package unconstrained.

## Recommendation

Choose option 1. Every normal site provides Overview, Installation, Getting
started/tutorial, Examples/how-to, Concepts where needed, API Reference,
Development/contributing, Changelog, and License.

Use `docs/reference/` for newly organized references. Existing `docs/api/`
trees may migrate during coordinated updates but do not coexist as a second
authoritative tree. Core may retain its deeper nested hierarchy while
providing the same semantic destinations and quality gates.

## Consequences

- Users encounter consistent responsibilities without unnecessary URL churn or
  shallow core navigation.
- Core's exception concerns structure, not quality.
- Package migrations must account for public URLs where required.

## Dependencies

ADR 001.
