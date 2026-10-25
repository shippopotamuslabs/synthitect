---
name: synthitect
description: >-
  Orchestrate the Synthitect workflow: research, design, structure, plan,
  human approvals, TDD Red, Red Review loop, implementation, and final review
  loop subagents. Resume across sessions via plans/{ticket_id}/status.md.
---

# Synthitect

Use this skill when the user wants the Synthitect workflow or asks for work to
be delegated to specialized phase subagents.

## Core Rule

The orchestrator stays stateless in chat — do not track phase progress only in
conversation memory. Persist progress on disk under `plans/{{ ticket_id }}/` and
use that to resume work across sessions or tool switches.

Do not return a briefing as the chat answer. Load the matching prompt from
`references/`, fill in request-specific context, and fire off the corresponding
subagent. Report the subagent's result and stop only at the gate the workflow
requires.

If the current runtime has no subagent/delegation tool, say that Synthitect
cannot run the phase in this environment. Do not paste the phase briefing as a
substitute for delegation.

## Trigger

`/synthitect [idea]` — start or continue a ticket.

If the user omits a ticket id, derive a short slug from the idea (e.g.
`add-user-auth`). Reuse an existing `plans/{ticket_id}/` directory when the
user says continue, resume, or names a known ticket.

## Resume Protocol

Before choosing a phase, read `plans/{{ ticket_id }}/status.md` when it exists
and verify artifacts on disk. Use this order:

| Condition | Next action |
| --- | --- |
| No `plans/{{ ticket_id }}/` | Create dir; write `ticket.md` from user request; start **Research** |
| No `research.md` | **Research** |
| `research.md` exists, no `design.md` | **Design** |
| `design.md` exists, design not approved in `status.md` | Report gate; wait for human approval |
| Design approved, no `structure.md` | **Structure** |
| `structure.md` exists, structure not approved in `status.md` | Report gate; wait for human approval |
| Structure approved, no `spec.md` or `test_spec.md` | **Plan** |
| Plan artifacts exist, plan not approved in `status.md` | Report gate; wait for human approval |
| Plan approved, red tests not written | **TDD Red** |
| Red tests exist, Red Review not clean | **Red Review** loop |
| Red Review clean, tests still failing | **Implementation** |
| Tests green, Final Review not clean | **Final Review** loop |
| Final Review clean | Report complete; ready for merge/handoff |

When resuming, summarize the checklist from `status.md` and the inferred next
phase before spawning a subagent.

## Status File

Every ticket keeps `plans/{{ ticket_id }}/status.md`. Subagents update it when
they finish. The orchestrator updates it when recording human approvals.

Template:

```markdown
# Status: {{ ticket_id }}

## Phase Checklist
- [ ] Research
- [ ] Design — approval: pending
- [ ] Structure — approval: pending
- [ ] Plan — approval: pending
- [ ] TDD Red
- [ ] Red Review — result: pending
- [ ] Implementation
- [ ] Final Review — result: pending

## Current Gate
none | awaiting human approval (design) | awaiting human approval (structure) | awaiting human approval (plan)

## Next Phase
[phase name after current gate clears]

## Loop Counts
- Red Review: 0/3
- Final Review: 0/3

## Notes
[blockers, open questions, changed files, last commands]
```

When the user approves design, structure, or plan, update the checklist entry to
`approval: yes` (with date), clear `Current Gate`, and set `Next Phase`.

## Workflow

1. Run the Resume Protocol to pick the correct phase.
2. Load the matching subagent prompt from `references/`.
3. Follow the human gates exactly:
   - Research: no human approval gate.
   - Design: run the design subagent, report its result, then wait for approval.
   - Structure: run after design approval; report result, then wait for approval.
   - Plan: run after structure approval; report result, then wait for approval.
   - TDD Red: no human approval gate after the plan is approved.
   - Red Review Loop: validate failing tests before implementation. If the
     reviewer finds admissible issues, rerun the TDD Red subagent with the
     findings as correction input, then rerun Red Review. Repeat until clean or
     until the loop limit is reached.
   - Implementation: no human approval gate after a clean Red Review.
   - Final Review Loop: run before merge or handoff. If the reviewer finds
     admissible issues, rerun the Implementation subagent with the findings as
     correction input, then rerun Final Review. Repeat until clean or until the
     loop limit is reached.
4. Never invent extra approvals or skip recorded gates.
5. Never paste the reference prompt into chat as the requested output.

## Review Loop Rule

Review loops are quality gates, not approval gates.

- Maximum loop attempts: 3 review passes per review phase.
- A loop continues only for admissible findings: correctness defects, approved
  behavior drift, contract or boundary incompatibility, behavioral regression,
  missing or weak required coverage, invalid Red phase tests, test weakening, or
  unverified runtime behavior.
- A loop must not continue for style preferences, naming taste, formatting
  churn, broad architecture suggestions, speculative hardening, optional
  refactors, or "nice to have" comments.
- If a reviewer reports only non-admissible findings, treat the review as clean
  and report those comments as ignored non-blocking notes only if they are useful.
- If the loop limit is reached with admissible findings still open, stop and
  report the unresolved findings, commands run, changed files, and blocker state
  to the user.
- Correction subagents must fix only the reported admissible findings and any
  directly required fallout. They must not restart the phase, broaden scope, or
  rewrite unrelated work.

## Delegation Contract

For each phase:

1. Read the relevant file from `references/`.
2. Substitute `{{ ticket_id }}`, `{{ raw_idea }}`, and any phase context from
   the current user request or completed artifacts.
3. Spawn a specialized subagent with that filled prompt.
4. Wait for the subagent when the next phase or human gate depends on its
   result.
5. Update `plans/{{ ticket_id }}/status.md` if the subagent did not.
6. Summarize completion status, changed files, command evidence, blockers, and
   gate state.

## Phase Order

1. Research subagent
2. Design subagent
3. Human approval (design)
4. Structure subagent
5. Human approval (structure)
6. Plan subagent
7. Human approval (plan)
8. TDD Red subagent
9. TDD Red Review loop
10. Implementation subagent
11. Final Review loop

## What To Use

- `references/research-briefing.md` for the research sub-agent
- `references/design-briefing.md` for the design sub-agent
- `references/structure-briefing.md` for the structure sub-agent
- `references/plan-briefing.md` for the plan sub-agent
- `references/tdd-red-briefing.md` for the red-test sub-agent
- `references/tdd-review-briefing.md` for the red-review sub-agent
- `references/implementation-briefing.md` for the implementation sub-agent
- `references/review-briefing.md` for the final review sub-agent

## TDD Red Review Standards

Before implementation, review the red tests against the approved plan and test
spec. Confirm every scenario has exactly one meaningful failing test, failures
come from unimplemented behavior rather than setup errors, and no test uses a
tautology, mocked system under test, production-derived expected value, or
generic exception assertion. If the Red Review finds invalid or missing tests,
rerun the TDD Red subagent with those findings as correction input, then rerun
Red Review. Proceed to implementation only after a clean Red Review, or stop
after the loop limit with unresolved admissible findings.

## Review Standards

For the final review, compare the implementation against the approved plan and
test spec, trace changed behavior through callers and callees, and report
evidence-backed findings. Prioritize fidelity to the plan, behavioral
regressions, boundary and contract compatibility, and missing tests. If the
Final Review finds admissible issues, rerun the Implementation subagent with
those findings as correction input, then rerun Final Review. Finish only after a
clean Final Review, or stop after the loop limit with unresolved admissible
findings.