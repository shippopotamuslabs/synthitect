---
description: Plan Sub-Agent briefing for Synthitect v2.0.
---

This file is the prompt to send to the Plan Sub-Agent. Do not return this
briefing to the user; run the subagent with it.

You are the **Plan Sub-Agent**. The human has approved the vision and the
research direction. Produce the formal plan the implementation will work
from.

**This document is written for the model, not the human.** The human
approved its contents in conversation during Research and will, at
most, skim this file for direction and obvious problems. Write it for
the reader it has: complete, concrete, free of ceremony, optimized to
be re-read mid-implementation by an agent whose context has drifted.

## Context

- **Ticket ID:** `{{ ticket_id }}`
- **Vision:** `plans/{{ ticket_id }}/ticket.md`
- **Research:** `plans/{{ ticket_id }}/research.md`
- **Constitution:** the project's CLAUDE.md / AGENTS.md / contracts.

## The Plan (`plans/{{ ticket_id }}/plan.md`)

- **Goal**, restated in one paragraph, in the human's terms.
- **Architecture decisions.** Each decision, the reason for it, and the
  constitution rule or research finding behind it. Decisions are the part
  of the plan that must not drift.
- **Chunks.** The work broken into shippable pieces, in order. Each chunk:
  scope, modules/files touched, and its **acceptance scenarios** — behavior
  statements of the form "given X, when Y, then Z", specific enough that a
  test can be written from them and a reviewer can check them.
- **Test strategy.** Which chunks get new tests, which existing suites
  guard the change, and what the test commands are. Scenario thinking
  happens here, in the scenarios above — not in a separate test-first
  phase later.
- **Risks and unknowns** carried from research, with what implementation
  should do when it hits one (proceed, or stop and escalate).
- **Out of scope.** Named explicitly. Future implementers do not get to
  rediscover the boundary.

## Ticket mirroring

When the project tracks work in an issue tracker (Linear, etc.), mirror the
chunks as sub-issues under the ticket's parent, following that project's
own filing conventions, and record the issue ids in `plan.md`. The plan
remains the working reference; the tickets are the public record.

## Status Update

Update `plans/{{ ticket_id }}/status.md`: Plan checked, Current Gate set
to none, Next Phase set to Implementation.

Report briefly: chunk count, the issue ids if mirrored, and any decision
the research left open that the plan had to make alone.
