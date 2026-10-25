---
name: synthitect
description: >-
  The Synthitect workflow, v2.0: vision intake, research, a formal plan
  artifact, implementation, a fresh-context architectural review loop, and
  ship via pull request with an external reviewer. Modernized for current
  frontier intelligence. Resume across sessions via plans/{ticket_id}/status.md.
---

# Synthitect v2.0

Use this skill when the user invokes `/synthitect` or asks for work to run
through the Synthitect workflow.

The division of labor: the human supplies the vision and the architectural
judgment. The model supplies research, the formal plan, implementation, and
evidence. Neither side does the other's job.

## Core Rules

1. **State lives on disk.** The orchestrator does not track progress only in
   conversation memory. Every ticket keeps `plans/{{ ticket_id }}/status.md`;
   phases update it as they finish. Sessions compact, crash, and get replaced;
   the work resumes from artifacts.
2. **One human gate, at the vision.** After Research, the findings and the
   proposed direction are reported to the human in chat, conversationally.
   The human approves, redirects, or kills the direction there. That is the
   only approval gate in the workflow.
3. **The plan is written for the model.** The formal plan is the model's
   working reference during implementation — a memory anchor, not a document
   the human is expected to read or sign. The human already approved what is
   in it during the vision conversation.
4. **No test-first phase.** Tests are written with the code, for regression
   protection, with expectations taken from the plan's acceptance scenarios.
   Scenario thinking lives in the plan. (The research for this is in the
   README; the short version is that agent-written tests-first measurably do
   not move outcomes, and the ceremony costs real time.)
5. **Review happens in a fresh context.** The reviewer did not write the code
   and does not inherit the production session's reasoning. It applies the
   admissible-findings discipline from the review briefing: material findings
   with file:line citations and command evidence, or silence.
6. **Loops are capped.** The review loop runs at most 3 rounds. Anything
   unresolved after that escalates to the human with the disagreement stated
   plainly.
7. **Architectural questions go to the human.** A finding that questions the
   design itself is reported as a question with the alternative stated, never
   silently "fixed." Code-level findings get fixed; architecture is the
   human's call.

## Trigger

`/synthitect [high-level vision]` — start or continue a ticket.

If the user omits a ticket id, derive a short slug from the vision
(e.g. `add-user-auth`). Reuse an existing `plans/{ticket_id}/` directory when
the user says continue or resume, or names a known ticket.

## Phases

| # | Phase | Briefing | Output |
| --- | --- | --- | --- |
| 1 | Research | `references/research-briefing.md` | `research.md` + a conversational report to the human. **Gate: vision approval.** |
| 2 | Plan | `references/plan-briefing.md` | `plan.md` with chunks and acceptance scenarios. Linear tickets mirrored when the project uses them. No gate. |
| 3 | Implementation | `references/implementation-briefing.md` | The code, tests written alongside, command evidence in `status.md`. |
| 4 | Review | `references/review-briefing.md` | Fresh-context review loop (max 3 rounds), including the project's Thermos pass where one exists. Architectural findings escalate as questions. |
| 5 | Ship | — | Pull request per repo conventions; external reviewer runs; merge per repo convention; `status.md` marked complete. |

Do not return a briefing as the chat answer. Load the matching briefing from
`references/`, fill in the request-specific context, and run the phase —
delegated to a subagent where the runtime supports it and the task is large
enough to warrant it, inline for small work. The Research report and the
fresh-context Review are never skipped; they are the workflow.

## Resume Protocol

Before choosing a phase, read `plans/{{ ticket_id }}/status.md` when it
exists and verify artifacts on disk.

| Condition | Next action |
| --- | --- |
| No `plans/{{ ticket_id }}/` | Create dir; write `ticket.md` from the user's vision, verbatim; start **Research** |
| Research done, vision not approved in `status.md` | Report the gate; wait for the human |
| Vision approved, no `plan.md` | **Plan** |
| `plan.md` exists, implementation incomplete | **Implementation** (next unfinished chunk) |
| Implementation complete, review not clean | **Review** loop |
| Review clean, PR not merged | **Ship** |
| PR merged | Report complete |

When resuming, summarize the checklist from `status.md` and the inferred next
phase before starting work.

## Status File

```markdown
# Status: {{ ticket_id }}

## Phase Checklist
- [ ] Research — vision approval: pending
- [ ] Plan
- [ ] Implementation
- [ ] Review — rounds: 0/3, result: pending
- [ ] Ship — PR: none

## Current Gate
none | awaiting vision approval | awaiting architecture decision

## Next Phase
[phase name]

## Notes
[blockers, open questions, changed files, last commands and their results]
```

## Scaling

The ceremony scales to the work. A one-file fix does not need five artifacts;
run the phases inline and keep `status.md` honest. A multi-day feature gets
the full path with delegated phases. When in doubt, keep the two load-bearing
pieces — research reported to the human before code, and review in a fresh
context after it — and compress the rest.

## If the runtime has no subagents

Run the phases inline, but keep the Review as a separate pass over the final
diff with the production reasoning out of scope, and say in the report that it
ran inline. V1 refused to run at all in that case. V2 considers that precious.
