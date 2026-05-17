---
name: synthitect
description: >-
  Orchestrate the Synthitect workflow: plan, human approval, TDD Red,
  Red Review, implementation, and final review subagents.
---

# Synthitect

Use this skill when the user wants the Synthitect workflow or asks for work to
be delegated to specialized phase subagents.

## Core Rule

Stay stateless. Do not track phase state, completed phases, or workflow memory
in files or chat. Do not return a briefing as the chat answer. Instead, load the
matching prompt from `references/`, fill in the request-specific context, and
fire off the corresponding subagent to do the phase work. Report the subagent's
result and stop only at the gate that the workflow requires.

If the current runtime has no subagent/delegation tool, say that Synthitect
cannot run the phase in this environment. Do not paste the phase briefing as a
substitute for delegation.

## Trigger

`/synthitect [idea]`

## Workflow

1. Decide whether the request is atomic or needs the Synthitect workflow.
2. For a workflow request, load the matching subagent prompt from `references/`.
3. Follow the human gates exactly:
   - Plan: run the plan subagent, report its result, then wait for approval.
   - TDD Red: no human approval gate after the plan is approved.
   - Red Review: validate the failing tests before implementation.
   - Implementation: no human approval gate after a clean Red Review.
   - Final Review: run before merge or handoff.
4. Never invent extra approvals, phase state, or persistence.
5. Never paste the reference prompt into chat as the requested output.

## Delegation Contract

For each phase:

1. Read the relevant file from `references/`.
2. Substitute `{{ ticket_id }}`, `{{ raw_idea }}`, and any phase context from
   the current user request or completed artifacts.
3. Spawn a specialized subagent with that filled prompt.
4. Wait for the subagent when the next phase or human gate depends on its
   result.
5. Summarize the subagent's completion status, changed files, command evidence,
   blockers, and gate state.

## Phase Order

1. Plan subagent
2. Human approval
3. TDD Red subagent
4. TDD Red Review subagent
5. Implementation subagent
6. Final review subagent

## What To Use

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
stop and report the gap instead of proceeding to implementation.

## Review Standards

For the final review, compare the implementation against the approved plan and
test spec, trace changed behavior through callers and callees, and report
evidence-backed findings. Prioritize fidelity to the plan, behavioral
regressions, boundary and contract compatibility, and missing tests.
