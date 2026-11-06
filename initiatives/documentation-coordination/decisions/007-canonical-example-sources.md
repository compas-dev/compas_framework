# ADR 007: Canonical Source Ownership for Examples

## Status

Accepted.

## Context

Runnable examples can appear in root example trees, documentation assets,
Markdown snippets, and copied variants. Verification of one copy does not keep
the others correct.

## Options

1. Maintain one canonical executable source per example.
2. Keep independent copies where each page needs one.
3. Introduce notebooks or generated Markdown as the universal source.

## Recommendation

Choose option 1. Documentation pages include or link the canonical `.py` file.
Small illustrative snippets may remain inline when they are not complete
programs. Substantial runnable snippets are extracted so the exact code shown
to users enters static and applicable runtime gates. Generated pages and copied
output are never authoritative sources.

## Consequences

- One edit updates every page that reuses the example.
- Duplicated root/docs variants must be consolidated deliberately.
- Notebook or Markdown generation remains a future decision, not a hidden new
  source system.

## Dependencies

ADRs 002 and 006.
