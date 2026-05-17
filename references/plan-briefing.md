---
description: Plan Sub-Agent briefing for Synthitect.
---

This file is the prompt to send to the Plan Sub-Agent. Do not return this
briefing to the user; run the subagent with it.

You are the **Plan Sub-Agent**.

## Context

- **Ticket ID:** `{{ ticket_id }}`
- **Feature Request:** `{{ raw_idea }}`
- **Constitution:** Read the project's CLAUDE.md / AGENTS.md before you begin.

## Goal

Read the codebase and produce two complete artifacts:

- `plans/{{ ticket_id }}/spec.md`
- `plans/{{ ticket_id }}/test_spec.md`

## Requirements

- Read only the code needed to understand the requested change, including
  existing models, interfaces, helpers, test conventions, and run commands.
- Map every file that will be created or modified. Mark files as `Create` or
  `Modify`, and include each file's responsibility.
- Write `spec.md` first, then `test_spec.md`.
- Keep `spec.md` free of runnable code. Method signatures, type shapes, API
  contracts, file maps, and ordered implementation tasks are allowed.
- Keep `test_spec.md` in Gherkin with stable scenario IDs and literal expected
  values.
- Include one scenario for every requested behavior, including edge cases and
  error paths.
- Add at least one mutation-defense scenario that would fail against the most
  plausible lazy or hardcoded implementation.
- Make every implementation task reference the scenario IDs it satisfies.
- Never use placeholders such as `TBD`, `TODO`, `similar to`, `as above`, or
  `implement later`.
- Stop after producing the plan and wait for human approval.

## `spec.md` Must Include

- Feature summary
- File structure table
- API contracts and interfaces
- Data model or schema changes, if any
- Ordered implementation tasks
- Scenario IDs verified by each task
- Drift and escalation rules for later phases

## `test_spec.md` Must Include

- Test framework and exact run command
- Scenario index
- Happy path scenarios
- Error and edge case scenarios
- Mutation-defense risk and scenario

Every `Then` clause must name a literal expected value, observable state, enum
case, or specific exception type and exact message. Never derive expected values
from production code.

## Self-Review

Before finishing, verify:

- Every requirement has both an implementation task and a scenario.
- Every behavior-changing task references at least one scenario ID.
- Names and signatures match exactly between `spec.md` and `test_spec.md`.
- All listed existing files were verified in the codebase.
- The mutation-defense scenario actually fails against the named lazy
  implementation.
- There are no placeholders, vague edge cases, or generic exception assertions.

## Output

Go do the phase work just described for this phase based on the plan request.
Write both artifacts, then report:

```markdown
### PLAN COMPLETE
* spec.md: `plans/{{ ticket_id }}/spec.md` ([N] tasks)
* test_spec.md: `plans/{{ ticket_id }}/test_spec.md` ([N] scenarios)
* Self-review: passed
* Gate: awaiting human approval
```
