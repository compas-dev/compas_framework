# ADR 023: Clean Break for Legacy Viewer Annotations

## Status

Accepted.

## Context

The current Viewer-owned `Tag` is a durable camera-facing text item.
`TextAnnotation` is only an alias, so serialized data still records the `Tag`
dtype. `ArrowOverlay` is also durable, world-anchored, transformable, and
serialized despite its transient-sounding name. No committed legacy JSON
fixtures exist, but current tests, documentation, and examples use both names.

Keeping aliases or legacy decoders would leave multiple public paths and retain
the misleading use of “overlay” for durable scene content.

## Options

1. Remove both legacy public types and their decoding paths when the canonical
   annotation types land.
2. Keep the old types only as aliases and serialized-data decoders.
3. Retain the old names indefinitely and add new types alongside them.

## Recommendation

Choose option 1.

Remove `Tag`, `ArrowOverlay`, and their old serialized dtype paths. Update all
package tests, examples, and documentation to the canonical types approved by
ADR 021. Do not add aliases, deprecation shims, dtype remapping, or a legacy
scene loader.

Old payloads containing `compas_viewer.scene/Tag` or
`compas_viewer.scene/ArrowOverlay` are unsupported after the change and fail
through the normal unknown-type loading boundary. Release notes and migration
documentation state the replacement construction paths explicitly.

Reserve “annotation” for durable world-anchored content and “overlay” for the
transient, non-serialized Viewer layer.

## Consequences

- The public vocabulary has one clear path per concept.
- Core and Viewer carry no permanent compatibility layer for experimental
  annotation types.
- Existing source imports and serialized payloads using the old types break
  intentionally.
- Implementation can remove obsolete concrete renderer branches instead of
  preserving parallel behavior.

## Compatibility

This is an intentional breaking change. The current initiative branches and
draft pull requests are the migration boundary. No release or main branch is
modified without the initiative's later explicit merge approval.

## Verification

- Verify old names are absent from public exports, examples, and documentation.
- Verify no legacy alias, dtype remapping, or decoder remains.
- Verify canonical annotations cover the approved visible behavior.
- Verify old serialized dtype strings fail clearly rather than being silently
  reinterpreted.

## Dependencies

- Depends on proposed ADR 021 for the canonical replacement ownership and
  names before implementation can begin.
- Refines the migration requirement of Accepted ADR 005.

## Decision

Approved on 2026-11-08. The annotation migration is a clean break: obsolete
public names and serialized-data paths are removed rather than preserved as
aliases or compatibility decoders. The rationale is to keep the system clean,
simple, efficient, and transparent, with one canonical path per concept.

