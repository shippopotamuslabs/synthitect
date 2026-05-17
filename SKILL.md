---
name: synthitect
description: >-
  Orchestrate the Synthitect workflow: plan, human approval, TDD Red,
  Red Review loop, implementation, and final review loop subagents.
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
   - Red Review Loop: validate the failing tests before implementation. If the
     reviewer finds admissible issues, rerun the TDD Red subagent with the
     findings as correction input, then rerun Red Review. Repeat until clean or
     until the loop limit is reached.
   - Implementation: no human approval gate after a clean Red Review.
   - Final Review Loop: run before merge or handoff. If the reviewer finds
     admissible issues, rerun the Implementation subagent with the findings as
     correction input, then rerun Final Review. Repeat until clean or until the
     loop limit is reached.
4. Never invent extra approvals, phase state, or persistence.
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
5. Summarize the subagent's completion status, changed files, command evidence,
   blockers, and gate state.

## Phase Order

1. Plan subagent
2. Human approval
3. TDD Red subagent
4. TDD Red Review loop
5. Implementation subagent
6. Final Review loop

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
