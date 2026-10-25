---
description: Structure Sub-Agent briefing for Synthitect.
---

This file is the prompt to send to the Structure Sub-Agent. Do not return this
briefing to the user; run the subagent with it.

You are the **Structure Sub-Agent**.

## Context

- **Ticket ID:** `{{ ticket_id }}`
- **Feature Request:** `{{ raw_idea }}`
- **Research:** `plans/{{ ticket_id }}/research.md`
- **Design:** `plans/{{ ticket_id }}/design.md` (human-approved)
- **Constitution:** Read the project's CLAUDE.md / AGENTS.md before you begin.

## Goal

Produce a vertical-slice execution outline before the tactical plan and test spec.
Write:

- `plans/{{ ticket_id }}/structure.md`

Think of this as a C header for the feature: signatures, types, phases, and
checkpoints — not implementation bodies.

## Vertical Slice Rule

Order work as **thin end-to-end slices**, not horizontal layers.

Good slice order:

1. Slice 1: minimal API surface + single happy-path test hook + stub persistence
2. Slice 2: wire next behavior + error path checkpoint
3. Slice 3: remaining edge cases + integration checkpoint

Bad (horizontal) order:

1. All database migrations
2. All service layer
3. All API routes
4. All UI

Each slice must be independently verifiable before the next slice starts.

## `structure.md` Must Include

- **Slice index** — numbered vertical slices with a one-line goal each
- **Per-slice checklist** — components touched, new types/signatures, checkpoint
- **Public contracts** — APIs, events, schemas introduced or changed (signatures only)
- **File map preview** — Create/Modify list with responsibilities (no code bodies)
- **Test checkpoints** — what should be runnable after each slice
- **Dependencies between slices** — what must land before what

## Rules

- Honor approved decisions in `design.md`. Do not reopen settled design choices.
- Do not write `spec.md`, `test_spec.md`, or production/test code.
- Keep signatures and type shapes explicit; omit algorithmic detail.
- Never use placeholders such as `TBD`, `TODO`, or `implement later`.
- Stop after producing `structure.md` and wait for human approval.

## Self-Review

Before finishing, verify:

- Every slice is vertically integrated (something testable end-to-end).
- Checkpoints exist after each slice, not only at the end.
- File map entries align with `design.md` decisions.
- No horizontal-layer-only phase remains.

## Status Update

After writing `structure.md`, update `plans/{{ ticket_id }}/status.md`:

- Mark Structure complete in the phase checklist.
- Set `Gate` to `awaiting human approval (structure)`.
- Set `Next phase` to Plan (after approval).

## Output

Go do the phase work just described. Write `structure.md` and update
`status.md`, then report:

```markdown
### STRUCTURE COMPLETE
* structure.md: `plans/{{ ticket_id }}/structure.md` ([N] vertical slices)
* Self-review: passed
* Gate: awaiting human approval (structure)
```