# ADR 047: Editable Parametric Shape Resolution

## Status

Accepted on 2026-11-11; the resolution controls are implemented, locally
verified, and independently reviewed. The settings-only refresh and wireframe
wording amendment is implemented, locally verified, and independently
reviewed. Native user retesting passed on 2026-11-11; hosted verification
remains pending.

## Context

Core already stores durable `u` and `v` resolution values on `ShapeObject`
and `SurfaceObject`. Both default to `16`, round-trip with the scene, and are
consumed by Viewer when it builds polygonal representations. They are not
currently editable, so Object Settings cannot change representation density
after construction.

One scalar `resolution` cannot represent existing objects whose `u` and `v`
differ. Exposing both axes indiscriminately would show controls that do nothing
for fixed-topology or single-axis producers.

## Options

1. Expose the existing durable `u` and `v` fields only where the represented
   producer consumes them.
2. Add one scalar `resolution` alias.
3. Add `u_resolution` and `v_resolution` aliases.
4. Expose `u` and `v` for every shape regardless of effect.
5. Add automatic screen-space level of detail.

## Recommendation

Choose option 1.

Keep the existing durable fields, defaults, and serialization. Mark applicable
fields editable and present them as **U Resolution** and **V Resolution**.
Viewer filters ineffective axes according to the represented object:

| Represented object | Controls | Validation |
|---|---|---|
| `Box` | None | Fixed topology does not consume resolution. |
| `Cone`, `Cylinder` | U | Integer at least `3`. |
| `Sphere`, `Torus` | U and V | Each integer at least `3`. |
| `Capsule` | U and V | U at least `3`; V at least `4` and even. |
| Parametric `Surface` | U and V | Each integer at least `1`. |
| Unknown `Shape` producer | None initially | Current conversion consumes neither axis. |

Values must be whole integers and booleans are rejected. Validation and
assignment are atomic. Invalid input restores durable values and triggers no
refresh.

A successful changed value rebuilds only the selected object's polygonal
representation, render buffers, and bounds; updates the renderer; and refreshes
Scene details once. It does not mutate the represented analytic shape, affect
other objects, or change selection. Edited values retain existing scene
round-trip behavior.

Do not add another serialized field, compatibility alias, schema version, or
resolution abstraction. Existing `u` and `v` remain the one public path.

### Settings-only refresh and wireframe wording amendment

High-resolution direct use showed that ordinary appearance edits follow the
same tessellation and global buffer rebuild path as topology edits. The
accepted correction distinguishes the two classes of edit:

- `show`, `show_points`, `show_lines`, `show_surfaces`, opacity, point size,
  and line width update the selected render object's settings texture once and
  request one redraw;
- these settings-only edits do not tessellate geometry, rebuild global render
  buffers, or rebuild the Scene tree unless displayed tree content changed;
- `u` and `v` remain topology edits and retain the one-object tessellation,
  buffer, bounds, renderer, and Scene-details refresh defined above; and
- color edits retain the current appearance-data path. Optimizing that path is
  deferred pending measured need and a separately approved contract.

ShapeObject and SurfaceObject forms present the existing line controls as
**Show wireframe**, **Wireframe color**, and **Wireframe width**. MeshObject and
GraphObject retain edge terminology. This is UI wording only: durable field
names, serialization, and public APIs do not change.

## Consequences

- Users can trade representation density against rendering cost after adding
  a supported shape.
- Independent U/V resolution remains available where supported.
- Controls are absent when changing them would have no effect.
- Existing scenes and defaults remain unchanged.
- Analytic geometry remains authoritative; only its Viewer representation and
  derived bounds are rebuilt.

## Verification

- Verify the exact controls for every listed producer.
- Verify labels, initial value `16`, whole-integer editing, and keyboard use.
- Reject booleans, fractions, below-minimum values, and odd Capsule V without
  mutation or refresh.
- Verify valid changes alter expected vertex/face counts, buffers, and bounds.
- Verify exactly one affected-object data refresh, renderer update, and Scene
  details refresh.
- Verify every settings-only field updates one object settings texture and
  requests one redraw without tessellation, global buffer rebuild, or Scene
  tree rebuild when displayed tree content is unchanged.
- Verify ShapeObject and SurfaceObject use wireframe wording while MeshObject
  and GraphObject retain edge wording; verify durable names are unchanged.
- Verify analytic geometry, unrelated objects, and selection are unchanged.
- Verify scene round-trip preserves edited U and V.
- Run Core and Viewer tests, Ruff, Pyright, strict MkDocs, and framework
  integration.

## Exclusions

- Circle and ellipse polyline counts.
- BRep- or backend-specific tessellation tolerances.
- Camera-distance or screen-space adaptive level of detail.
- Global resolution defaults.
- A speculative maximum-resolution cap.

## Dependencies

- Uses Accepted ADRs 015–016's normalized editable-attribute contract.
- Uses ADR 004's existing data/buffer refresh ownership.
- Preserves ADR 002's indexed representation contract.

## Decision

Approved on 2026-11-11. Implementation and local verification pass. An exact
native macOS subprocess changed a Torus U resolution from 16 to 64 with a valid
OpenGL context. The subsequent interactive crash was traced to Qt emitter
lifetime and fixed; direct user retesting confirmed the fix at U resolution 64.

The settings-only refresh and wireframe wording amendment was approved on
2026-11-11. Implementation, local verification, and independent review pass.
The Viewer suite passes 656 tests with two expected offscreen native-OpenGL
skips. Native direct use on 2026-11-11 confirms that a Torus at U resolution
64 toggles **Show wireframe** off and on responsively, accepts the wireframe
wording, and preserves the resolution crash fix.
