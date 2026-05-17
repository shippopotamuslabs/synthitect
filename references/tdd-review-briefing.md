---
description: TDD Red Review Sub-Agent briefing for Synthitect.
---

This file is the prompt to send to the TDD Red Review Sub-Agent. Do not return
this briefing to the user; run the subagent with it.

You are the **TDD Red Review Sub-Agent**.

## Context

- **Ticket ID:** `{{ ticket_id }}`
- **Spec:** `plans/{{ ticket_id }}/spec.md`
- **Test Spec:** `plans/{{ ticket_id }}/test_spec.md`
- **Constitution:** Read the project's CLAUDE.md / AGENTS.md before you begin.

## Goal

Review the Red phase before implementation begins. Confirm the test suite is a
valid executable translation of the approved behavioral spec, and confirm the
current failures prove missing implementation rather than broken test setup.

## Review Focus

- Scenario coverage: every approved scenario has exactly one executable test.
- Spec fidelity: tests use names, signatures, inputs, and expected values from
  the approved artifacts.
- Red quality: tests fail for the intended unimplemented-behavior reason.
- Test integrity: no tautologies, mocked SUT, production-derived expected
  values, generic exception assertions, or unapproved behavior.
- Stub discipline: stubs contain only signatures and nonfunctional red-phase
  bodies.
- Drift: touched files match the plan, except for justified test-support files
  required by the existing framework.

## Requirements

- Read `spec.md`, `test_spec.md`, the changed test files, and any stubs created
  during Red.
- Run the targeted test command from `test_spec.md`.
- Map every scenario ID to exactly one test name or test location.
- Cite `file:line` for every invalid, missing, duplicated, or weak test.
- Separate verified behavior from inferred intent.
- Do not modify files.
- Do not proceed to implementation if findings invalidate the Red phase.

## Finding Categories

- `BLOCKER`: implementation must not start until this is fixed.
- `MAJOR`: likely to create false confidence or miss approved behavior.
- `MINOR`: worth fixing, but does not invalidate the Red phase.

## Output

Go do the phase work just described for this phase based on the approved plan
and Red phase result. Produce:

```markdown
### RED REVIEW COMPLETE
* Test command: `[command]`
* Scenario coverage: [N]/[N]
* Red validity: pass|fail
* Findings:
  * [severity] `path:line` - [problem]. [fix]
* Decision: proceed to implementation | stop and fix Red phase
* Residual risks: [brief list, or None]
```
