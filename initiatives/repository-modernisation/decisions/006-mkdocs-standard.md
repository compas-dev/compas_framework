# ADR 006: MkDocs Documentation Standard

**Status:** Accepted

## Context

The three references use MkDocs Material and mkdocstrings, but installation,
strictness, URLs, versioning, and deployment differ. Some obsolete RST remains.

## Options

1. Permit Sphinx or MkDocs per repository indefinitely.
2. Use one generated central documentation configuration.
3. Standardize outcomes and a small MkDocs baseline while keeping explicit
   repository navigation/content.

## Recommendation

Use MkDocs Material, mkdocstrings, Markdown, explicit navigation, correct
site/repository URLs, and cross-package inventories. Every PR runs
`mkdocs build --strict`. Use Mike only for repositories with versioned deployed
docs. Keep `mkdocs.yml` repository-owned and remove superseded RST after link
verification.

## Consequences

Documentation failures become visible before merge. Existing warnings must be
resolved before strict mode blocks changes. Documentation dependencies live in
the pyproject docs group. Migration requires link, API, and example validation.

## Affected repositories

All core repositories with published documentation.

## Dependencies

ADR 002, ADR 003.
