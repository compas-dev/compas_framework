# ADR 005: Verification and Evidence Gates

## Status

Accepted.

## Context

Source inspection or editable-install tests do not prove installed metadata,
built wheels, import isolation, optional selection, or runtime behavior. Host
packages cannot be validated by ordinary CPython CI alone.

## Options

1. Require common source, installed-metadata, fresh-process, artifact, and
   applicable runtime evidence.
2. Verify only package metadata.
3. Verify only editable installs.
4. Treat unavailable runtime evidence as a documented passing limitation.

## Recommendation

Choose option 1. A migrated package verifies installed and built metadata,
fresh-process isolation, decorator location, full parity, lazy delegation,
optional selection, real public dispatch, and direct implementation behavior.
Every admitted host package additionally requires host-runtime evidence.

## Consequences

- Completion evidence is consistent across packages.
- Missing required host evidence means incomplete and unverified, not passing.
- Editable-install success alone is insufficient.
- Generated artifacts remain isolated in temporary directories.

## Affected packages

Every package admitted to the initiative.

## Dependencies

- [ADR 001](001-authoritative-discovery.md)
- [ADR 002](002-registration-boundary.md)
- [ADR 003](003-contract-and-direct-apis.md)
- [ADR 004](004-optional-runtimes.md)
