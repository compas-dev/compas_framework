# Initiative Handoff

Last updated: YYYY-MM-DD

## Resume here

Current phase: `<reconnaissance | architecture | implementation | integration | audit | complete>`

Status: One or two sentences describing the verified checkpoint and why work
is stopping here.

Read next:

1. `objective.md`
2. `implementation-plan.md`
3. Add only the ADR, inventory section, proposal section, or package document
   required for the next task.

Do not reread the entire initiative unless the next task requires it.

## Decisions and approvals

- Accepted: link only the ADRs governing the next tasks.
- Proposed or unresolved: link each blocking decision and state the approval
  required.
- Scope boundary: state what is explicitly not authorized.

## Working state

| Repository | Branch | Exact head | Pull request | Status |
|---|---|---|---|---|
| `owner/repository` | `initiative/branch` | `<40-character SHA>` | `<URL or none>` | `<clean/dirty, pushed/local>` |

Preserve any unrelated dirty paths explicitly. Never infer a branch head from
an earlier conversation.

## Completed at this checkpoint

- Record only work completed since the previous handoff or the evidence needed
  to understand the current boundary.
- Link hosted workflow evidence instead of copying logs.

## Next tasks

1. First concrete, verifiable task.
2. Second task, including its dependency on the first if applicable.
3. Third task or final review.

## Blockers and approval gates

- `None`, or one bullet per concrete blocker.
- State actions that still require explicit approval, especially merges,
  publication, new initiative scope, or unresolved ADRs.

## Verification

Last verified:

- `<command>` — `<result or not yet run>`
- `<workflow URL>` — `<exact head and result>`

Run next:

```text
<smallest focused command>
<broader completion command, only when warranted>
```
