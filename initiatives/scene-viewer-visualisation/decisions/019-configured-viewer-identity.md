# ADR 019: Configured Viewer Identity

## Status

Accepted.

## Context

Viewer configuration has a `WindowConfig.title`, but application identity and
startup window behavior are not consistently applied before Qt application
construction. Icon selection also needs a clear packaged-default and
custom-file contract.

## Options

1. Use startup-only `WindowConfig` fields as the single configured Viewer
   identity.
2. Add separate application-name, display-name, and window-title fields.
3. Keep identity hardcoded and let callers mutate Qt objects after startup.

## Recommendation

Choose option 1.

The existing `WindowConfig.title` supplies all three startup identity values:

- Qt application name;
- Qt application display name; and
- main window title.

`WindowConfig.icon` is either:

- `None`, which selects the packaged Viewer icon; or
- an absolute filesystem path to a custom icon.

Relative paths are invalid. Identity, icon, dimensions, and fullscreen are
startup-only configuration. Viewer validates and applies the configuration
before constructing `QApplication` and the main window. The existing
`fullscreen` field is honored during startup rather than remaining inert.

This decision does not add a runtime identity mutation API.

## Consequences

- One title cannot diverge across application and window identity surfaces.
- Packaged applications get a default icon without configuring a path.
- Custom identity is deterministic but cannot be changed live.

## Compatibility

Existing title, width, height, and fullscreen values keep their startup
meaning. The optional icon is additive startup configuration.

## Verification

- Apply title to application name, display name, and window title before the
  window is shown.
- Use the packaged icon for `None` and an existing absolute path for a custom
  icon.
- Reject relative or invalid icon paths with a precise configuration path.
- Honor configured width, height, and fullscreen at startup.
- Verify no runtime identity mutation API is added.

## Dependencies

- Independent of scene, object-settings, and configuration-cleanup ADRs.

## Decision

Approved on 2026-11-08. `WindowConfig.title` is the single startup identity for
the Qt application and main window, while `WindowConfig.icon` selects either
the packaged icon or an existing absolute custom path. The rationale is to
make identity and startup window behavior deterministic without duplicate
names, post-construction mutation, or a separate runtime identity API.
