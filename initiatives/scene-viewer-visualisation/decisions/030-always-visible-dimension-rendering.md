# ADR 030: Always-Visible Persistent Dimension Rendering

## Status

Accepted.

## Context

Transient measurement feedback renders above scene geometry and remains
legible. Persistent distance dimensions were rendered in the ordinary
depth-tested world-annotation pass and could disappear behind geometry. Their
durable storage location does not determine their render-layer semantics.

## Options

1. Render persistent distance dimensions in a separate final pass without
   depth testing or depth writes.
2. Keep depth testing and increase depth bias or epsilon.
3. Reimplement persistent dimensions on the transient QWidget canvas.
4. Keep the current equal-depth world-annotation pass.

## Recommendation

Choose option 1.

Viewer renders ordinary world text and arrows with their existing depth
behavior. It then renders `DistanceDimension` objects in a separate final pass,
preserving their scene insertion order. Depth testing and depth writes are
disabled for this pass, so scene geometry cannot hide a dimension.

The pass restores the previous depth function, depth-test enablement, and
depth-write mask in all success and failure paths. It reuses the existing
dimension render geometry and does not duplicate persistent dimension drawing
on the transient QWidget canvas.

This decision is independent of annotation persistence and UI ownership.
ADR 029 may later move annotations out of the spatial hierarchy without
changing this rendering contract.

## Consequences

- Persistent and transient distance feedback remain legible over scene
  geometry.
- Dimensions no longer communicate occlusion through the depth buffer; their
  purpose is annotation rather than solid-scene geometry.
- Text and arrow annotations keep their existing behavior.
- No general render-layer or annotation-plugin framework is introduced.

## Compatibility

This changes only Viewer rendering behavior. Annotation data, serialization,
anchor resolution, and public construction APIs remain unchanged.

## Verification

- Verify ordinary world annotations render before persistent dimensions.
- Verify insertion order is preserved within each pass.
- Verify dimensions draw with depth testing and depth writes disabled.
- Verify the previous depth function, test enablement, and write mask are
  restored after success and after a draw failure.
- Verify scene geometry cannot hide a completed distance dimension.

## Dependencies

- Refines Accepted ADRs 005, 021, 024, and 026.
- Independent of Proposed ADR 029.

## Decision

Approved on 2026-11-09. Persistent distance dimensions render in a separate
final Viewer pass without depth testing or depth writes. The rationale is that
durable annotation visibility should match transient measurement legibility
without coupling render policy to spatial hierarchy or storage ownership.
