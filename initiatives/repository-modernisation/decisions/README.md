# Repository Modernisation Decisions

ADRs 001–021 are **Accepted**. ShapeOp follow-up ADRs 022–023 are
**Proposed** and block only the corresponding public-contract changes. All
implementation remains subject to the repository-setting, publishing,
deployment, and merge approval boundaries.

| ADR | Decision | Status | Depends on |
|---|---|---|---|
| [001](001-repository-profiles.md) | Common policy and repository profiles | Accepted | — |
| [002](002-pyproject-source-of-truth.md) | `pyproject.toml` source of truth | Accepted | 001 |
| [003](003-uv-and-lockfiles.md) | uv and committed development locks | Accepted | 001, 002 |
| [004](004-command-interface.md) | Direct local and CI commands | Accepted | 002, 003, 007 |
| [005](005-ruff-standard.md) | Ruff-only style tooling | Accepted | 002, 004 |
| [006](006-mkdocs-standard.md) | Strict MkDocs documentation | Accepted | 002, 003 |
| [007](007-shared-action-boundary.md) | Shared-action boundary | Accepted | 001 |
| [008](008-release-and-artifacts.md) | Release PRs and artifact promotion | Accepted | 007, 009, 010, 011 |
| [009](009-python-platform-support.md) | Python/platform support policy | Accepted | 001, 002 |
| [010](010-workflow-security.md) | Workflow security and action pins | Accepted | 007 |
| [011](011-quality-gate-adoption.md) | Blocking quality-gate adoption | Accepted | 005, 006, 009 |
| [012](012-external-build-sources.md) | Immutable native build sources | Accepted | 001, 010 |
| [013](013-framework-integration-and-release-order.md) | Framework integration and release order | Accepted | 008, 009, 011, 012 |
| [014](014-gmsh-runtime-and-support.md) | Gmsh runtime provisioning and support contract | Accepted | 001, 002, 003, 009 |
| [015](015-gmsh-license-boundary.md) | `compas_gmsh` and Gmsh license boundary | Accepted | 002, 014 |
| [016](016-gmsh-verification-and-release.md) | Gmsh verification, typing, and artifact release | Accepted | 004–011, 014, 015 |
| [017](017-shapeop-python-stable-abi-matrix.md) | ShapeOp Python and stable-ABI matrix | Accepted | 001, 002, 008, 009, 011, 013 |
| [018](018-shapeop-native-dependencies-and-portability.md) | ShapeOp native dependencies and build portability | Accepted | 001, 002, 008, 010, 011, 012, 017 |
| [019](019-shapeop-distribution-and-quality-contract.md) | ShapeOp distribution and quality contract | Accepted | 002–006, 008, 010, 011, 013, 017, 018 |
| [020](020-framework-host-extras.md) | `compas_framework` host extras during the COMPAS 3 transition | Accepted | 001, 002, 003, 009, 011, 013 |
| [021](021-cross-repository-candidate-artifacts.md) | Cross-repository candidate artifact provenance | Accepted | 008, 010, 012, 013 |
| [022](022-shapeop-similarity-correspondence-flags.md) | ShapeOp similarity correspondence flags | Proposed | 019 |
| [023](023-shapeop-point-buffer-lifecycle.md) | ShapeOp point-buffer reassignment lifecycle | Proposed | 019 |

## Recommended review order

1. ADR 001: establish the policy/profile model.
2. ADR 002 and ADR 007: choose configuration and automation boundaries.
3. ADR 003, ADR 004, ADR 009, and ADR 010: settle environments, commands,
   support, and security.
4. ADR 005 and ADR 006: settle style and documentation targets.
5. ADR 011: settle adoption after target gates are known.
6. ADR 008: approve release behavior once its dependencies are clear.
7. ADR 012: settle native-source reproducibility after security policy (this
   can be reviewed in parallel with ADR 008).
8. ADR 013: approve coordinated integration/release order after release and
   native-source decisions.
9. ADRs 014–016: implement the accepted Gmsh provisioning/support, licensing,
   and verification/release contracts in dependency order.
10. ADRs 017–019: implement the accepted ShapeOp Python/ABI matrix, native
    dependency portability, and distribution/quality contract in dependency
    order.
11. Implement accepted ADR 020 to resolve the framework host-extra metadata
    conflict before the ordinary framework modernization patch is committed.
12. ADR 021: implement the accepted candidate-artifact provenance and
    credential boundary before enabling the native integration and
    release-order gate.
13. ADRs 022–023: decide the two newly exposed ShapeOp public contracts before
    renaming the misleading correspondence flag or changing post-init point
    reassignment.
