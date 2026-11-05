# ADR 015: `compas_gmsh` and Gmsh License Boundary

**Status:** Proposed

## Context

The wrapper source is intended to use the MIT license, and documentation
includes `LICENSE.MIT`. Project metadata instead points to a nonexistent
`LICENSE`. The repository also contains a GPL-3.0 license text, while its README
describes the separately installed Gmsh runtime as GPL-2.0-or-later. This can be
read as an accidental dual-license declaration or as an incorrect statement of
Gmsh's license.

`compas_gmsh` does not build or bundle Gmsh. Its dependency resolver installs
the separately distributed official Gmsh SDK.

## Options

1. **Declare the wrapper GPL.** This would remove ambiguity but changes the
   intended license of COMPAS-owned source without a technical requirement.
2. **Declare dual MIT/GPL licensing.** This preserves both files but does not
   explain which terms apply to which software.
3. **Declare the wrapper MIT and document Gmsh separately.** Package metadata
   and artifacts identify only the wrapper's license; installation guidance
   identifies the required Gmsh dependency and its GPL-2.0-or-later terms.

## Recommendation

Choose option 3. Use the SPDX expression `MIT` in project metadata and include
`LICENSE.MIT` as the wrapper's license file. Remove the ambiguous GPL-3.0 text
from the wrapper distribution. Add a concise third-party runtime notice in the
README, installation guide, and license page linking to Gmsh's authoritative
license information and stating that Gmsh is installed and distributed
separately.

Do not copy Gmsh binaries or its license into the `compas_gmsh` wheel. If a
future release bundles Gmsh, vendors patched Gmsh, or publishes a combined
installer, this decision no longer covers that artifact and legal/license
review is required before distribution.

## Consequences

PyPI metadata, source archives, wheels, badges, and documentation have one
unambiguous project license. Users are still informed that using the package
requires separately licensed GPL software. The repository stops shipping an
unrelated GPL-3.0 text that can be mistaken for the wrapper's license.

This is a packaging boundary, not legal advice. Maintainers remain responsible
for confirming license metadata before publication.

## Affected files

`pyproject.toml`, `LICENSE.MIT`, `LICENSE.GPL`, `README.md`, `docs/license.md`,
installation documentation, and artifact metadata tests.

## Dependencies

ADRs 002 and 014.
