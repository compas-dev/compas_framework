# ADR 034: Mesh-Vertex Snapping Independent of Vertex Glyphs

## Status

Proposed.

## Context

Semantic snapping already enumerates every Mesh vertex while a measurement
tool is active. In practice, vertices become unreliable when normal vertex
glyphs are hidden because the instance/depth pass loses their dedicated point
footprint. Nearby faces or edges may happen to provide qualifying pixels, so
the current result is geometry-dependent.

Normal rendering preferences and measurement eligibility are separate
concerns. A measurement guide can make a candidate visible without requiring
the ordinary vertex display to remain enabled.

## Options

1. Add a measurement-only acquisition footprint for Mesh vertices.
2. Require normal vertex glyphs to be visible.
3. Accept every projected vertex without depth qualification.
4. Add edge and face snapping at the same time.

## Recommendation

Choose option 1.

`show_vertices` controls ordinary Mesh vertex glyphs only. During an active
measurement, every vertex of an effectively visible Mesh is a semantic
candidate and may appear as a hollow-square guide even when normal vertex
glyphs are off.

Viewer renders a measurement-only point footprint into the offscreen
instance/depth acquisition pass. It never appears in ordinary rendering. The
nearest vertex within the existing 18-logical-pixel radius wins only when its
measurement footprint passes the existing same-object depth qualification.

`show=False`, including effective ancestor hiding, remains a hard exclusion. A
Mesh with no visible face, edge, or vertex representation is not discoverable
solely because measurement mode is active. Faces and edges may establish
visibility and occlusion but remain non-candidates and create no attraction.
Partial ordinary vertex-display lists do not restrict measurement candidates.

## Consequences

- Users can snap to vertices of the normal face-only Mesh display.
- Measurement feedback, not ordinary glyph configuration, communicates snap
  availability.
- Occluded vertices and other objects' pixels remain ineligible.
- No new public API, general snapping framework, or edge/face snapping is
  introduced.

## Verification

- Verify hidden ordinary Mesh vertices remain semantic candidates.
- Verify face-only and edge-only visible Meshes produce guides and a qualified
  winner.
- Verify front/silhouette vertices pass while back, depth-mismatched, and
  externally occluded vertices do not.
- Verify hidden whole objects and Meshes with no visible representation produce
  no candidates.
- Verify no edge or face result is introduced and the 3–4–5 regression remains
  exact.

## Dependencies

- Amends Accepted ADR 026's visible-discrete-point acquisition wording.
- Preserves Accepted ADR 028's anchor semantics.

## Decision

Pending explicit approval.
