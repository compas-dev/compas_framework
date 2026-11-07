# ADR 009: Later-Wave Admission

## Status

Accepted.

## Context

The later ecosystem includes active, dormant, native, Sphinx-based, and
host-specific repositories. Presence in a local checkout is not evidence that a
package is an active COMPAS 3 documentation target.

## Options

1. Admit packages individually or in explicitly approved compatibility waves.
2. Include every repository after the active ten.
3. Exclude the later ecosystem permanently.

## Recommendation

Choose option 1. Admission requires active ownership, confirmed COMPAS 3
compatibility, repository modernisation or an approved equivalent baseline, a
working documentation builder, declared example roots, Ruff/Pyright coverage,
a runtime-verification environment, and no unresolved public-contract mismatch.

Sequence active MkDocs packages first, then Sphinx-to-MkDocs migrations,
native/optional backends with artifact evidence, and finally host integrations
with host-specific validation. Archived and duplicate checkouts remain
excluded unless explicitly reactivated.

## Consequences

- The initiative can expand without becoming open-ended.
- Native and host packages cannot be declared complete from ordinary CPython
  evidence.
- Every later wave requires explicit scope approval.

## Dependencies

Successful active-ten rollout and ADRs 003, 005, and 007.
