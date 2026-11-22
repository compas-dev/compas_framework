# ADR 001: Common Policy and Repository Profiles

**Status:** Accepted

## Context

COMPAS repositories share Python tooling and release policy but differ in
runtime provisioning and artifact production. `compas` is pure Python,
`compas_occ` needs Conda-provided PythonOCC, and `compas_cgal` builds native
wheels with CMake and cibuildwheel.

## Options

1. **One identical template.** Minimal visible variation, but cannot express
   native and Conda requirements honestly.
2. **Independent repository configurations.** Flexible, but perpetuates drift.
3. **One policy with explicit profiles.** Shares outcomes and conventions while
   keeping provisioning/build behavior repository-owned.

## Recommendation

Use one common policy with pure-Python, external-runtime hybrid, and
native-wheel profiles. Optional runtime integration jobs and coordinated
framework integration are explicit additions to the closest profile, not new
universal configuration layers. Assign `compas_viewer` to the Python profile
with an explicit Qt/OpenGL/headless-test extension. Add
a profile only for a demonstrated requirement, not anticipation.

## Consequences

Shared checks, documentation, and release stages remain consistent. Workflow
files are not byte-identical. Tests must cover each profile. Documentation must
state which profile a repository follows and any justified deviations.

## Affected repositories

The ten initial core repositories named in the initiative proposal. Host
integrations are a later wave.

## Dependencies

None.
