# ADR 020: `compas_framework` Host Extras During the COMPAS 3 Transition

**Status:** Accepted

## Context

`compas_framework` is a COMPAS 3 metapackage and requires `compas>=3.0.0`.
Its project metadata for that release line also defines three optional host
extras:

```toml
rhino = ["compas_ghpython", "compas_rhino"]
blender = ["compas_blender"]
hosts = ["compas_blender", "compas_ghpython", "compas_rhino"]
```

The exact host-package revisions inspected by the modernization work remain on
the COMPAS 2 contract:

- `compas_blender` at `2796eec4` requires `compas>=2.15,<3`;
- `compas_rhino` at `8f5e28d1` requires `compas>=2.15,<3`; and
- `compas_ghpython` at `8dabfefd` requires both `compas>=2.15,<3` and
  `compas_rhino>=2.15,<3`.

Consequently, no standards-compliant resolver can install the COMPAS 3
metapackage together with any of those extras. uv also resolves project extras
when producing the root development lock, so the contradiction prevents a
truthful `uv.lock` even when ordinary CI later synchronizes tooling groups
without installing the project.

The draft modernization patch temporarily uses
`override-dependencies = ["compas>=3.0.0"]` plus Git source pins. That makes the
lock resolvable by discarding the host packages' declared COMPAS constraint.
It does not establish runtime compatibility and permits an explicitly
unsupported `uv sync --extra ...` environment.

Host integration packages are outside the approved initial core modernization
wave. Their runtime migration requires separate evidence in Rhino,
Grasshopper, and Blender.

## Options

### 1. Remove and defer the incompatible host extras

Remove `rhino`, `blender`, and `hosts` from `compas_framework` metadata for the
COMPAS 3 line. Remove their Git sources and the COMPAS override from the root
uv configuration. Remove installation examples that claim the extras work and
state in the changelog and installation guide that host bundles will return
after their owning packages have compatible, verified releases.

This is a visible compatibility break, but it makes published metadata, the
development lock, and documentation tell the same truth.

### 2. Retain the extras with a documented tooling-only override

Keep the current extras, Git sources, and `override-dependencies`, while
documenting that only `--only-group ... --no-install-project` commands are
supported and that the extras must not be synchronized.

This preserves the extra names but publishes combinations that ordinary
installers cannot resolve. The override also suppresses dependency evidence
instead of demonstrating compatibility. A warning in contributor docs cannot
repair invalid distribution metadata.

### 3. Put modernization tools in a nested uv project

Move dependency groups and their lock into a separate tooling project whose
metadata never includes the metapackage extras. Keep the existing root project
metadata unchanged and leave its extras outside the tooling lock.

This can make contributor tooling reproducible without an override, but adds a
second project configuration, lock, environment location, and command context.
It still leaves the published COMPAS 3 host extras unsatisfiable, so it avoids
rather than resolves the public contract defect.

## Recommendation

Choose option 1. Remove and explicitly defer all three host extras for the
COMPAS 3 metapackage until their dependencies and host-runtime evidence are
compatible with COMPAS 3.

This is the smallest truthful contract:

- `pyproject.toml` remains the sole dependency authority;
- the root `uv.lock` resolves without overrides that contradict dependency
  metadata;
- every documented installation command denotes a resolvable environment; and
- host support is restored only by the repositories that own and can verify
  it.

Do not publish empty extras, aliases, placeholder packages, conditional
constraints, or a compatibility shim. Those would preserve names without
providing the advertised functionality.

## Decision

Approved on 2026-11-05. Remove and explicitly defer the incompatible COMPAS 2
host extras from the COMPAS 3 metapackage. The rationale is to keep published
metadata, the root lock, and installation documentation truthful rather than
override dependency evidence or advertise combinations that cannot resolve.
Host support returns only through separately verified package decisions.

## Compatibility implications

- `pip install "compas_framework[rhino]"`,
  `pip install "compas_framework[blender]"`, and
  `pip install "compas_framework[hosts]"` stop being supported COMPAS 3
  installation paths.
- Existing COMPAS 2 releases and their host extras are unchanged.
- Users needing a current host package continue to install the COMPAS 2 stack
  documented by that host package. Mixing it with the COMPAS 3 metapackage is
  explicitly unsupported.
- Removing the extras must be recorded in the changelog and release notes as a
  deliberate compatibility break, not hidden as lock-file maintenance.
- No host package source, runtime behavior, or release is changed by this ADR.

## Implementation consequences

After acceptance, the bounded `compas_framework` modernization patch must:

1. remove the three entries from `[project.optional-dependencies]`;
2. remove the `compas-blender`, `compas-rhino`, and `compas-ghpython` uv source
   entries and remove the COMPAS dependency override;
3. regenerate `uv.lock` from the unmodified remaining project metadata;
4. remove the three extra-install commands from the README and installation
   documentation, replacing them with the explicit deferral notice;
5. add changelog and release-guide coverage for the compatibility break; and
6. keep the pure tooling synchronization and native integration jobs otherwise
   unchanged.

The repository must not claim that removing the extras completes host-package
modernization. It only removes an invalid metapackage promise.

## Verification

- `uv lock --check` succeeds without `override-dependencies`.
- A clean root `uv lock` resolves all remaining project metadata and dependency
  groups without host-package Git sources.
- The pure development synchronization still installs no COMPAS framework or
  native runtime distributions.
- Wheel and sdist metadata contain no `Provides-Extra` or conditional
  `Requires-Dist` entries for `rhino`, `blender`, or `hosts`.
- Repository search finds no command that recommends installing one of the
  removed extras for COMPAS 3.
- Ruff, Pyright, tests, strict MkDocs, artifact inspection, and isolated
  no-dependency metapackage import remain green.

## Restoration criteria

A host extra may return only through a new explicit architecture decision
after every package in that extra:

1. declares a compatible COMPAS 3 dependency range without an override;
2. has a released or immutable candidate artifact that resolves together with
   the metapackage;
3. passes source and installed-artifact checks appropriate to its Python
   runtime;
4. passes real Rhino, Grasshopper, or Blender runtime evidence for the public
   integration contract, rather than ordinary CPython import tests alone; and
5. has installation, support-matrix, failure-mode, and ownership documentation
   consistent with the restored metadata.

The `hosts` aggregate returns only after all three individual package paths
meet these criteria. Individual extras may be restored independently when
their complete dependency set is ready.

## Dependencies

ADRs 001, 002, 003, 009, 011, and 013.
