# Synthitect

A structured workflow for shipping features with AI coding tools. Synthitect
runs a feature request through a fixed pipeline of specialized subagents:
research, design, structure, plan, test-driven implementation, and review.
Human gates sit where judgment matters. Every phase writes its artifact to
disk, so work resumes across sessions and across tools.

## What it does

A feature request goes in. Reviewed, tested code comes out the other end,
with the reasoning kept in files you can read.

```text
Research → Design → Structure → Plan → TDD Red → Red Review → Implement → Final Review
              ↑          ↑         ↑
         human gate  human gate  human gate
```

**Alignment (before code).** Objective codebase research, a design discussion
artifact, and a vertical-slice structure outline. Wrong patterns get caught
in documents that take minutes to read, before they turn into a long plan
built on them.

**Planning.** `spec.md` holds the implementation contract. `test_spec.md`
holds Gherkin scenarios with literal expected values, mutation defense
included.

**Execution.** Failing tests first, a review of the red phase's integrity,
implementation to green, then a final evidence-backed review. Review loops
rerun only for findings that matter (correctness, drift from the plan, weak
coverage). Style nits do not loop.

## Quick start

### Install the skill

Point your agent skills directory at this repo:

```bash
ln -sfn /path/to/synthitect ~/.grok/skills/synthitect
```

The same link works for Claude Code, Codex, or any runtime that loads skills
from a path. The repo root is the skill: `SKILL.md` plus `references/`.

### Start a ticket

```text
Use synthitect to plan out adding rate limiting to the API
```

or

```text
/synthitect add-api-rate-limiting
```

The agent creates `plans/add-api-rate-limiting/`, runs Research, then Design,
and stops for your approval.

### Approve and continue

After reading `plans/{ticket_id}/design.md`:

```text
Design approved. Continue synthitect.
```

Same for Structure and Plan. After plan approval:

```text
Plan approved. Run the rest.
```

TDD Red through Final Review then runs with no further approvals, unless a
review loop needs a correction only you can make.

### Resume after switching tools

```text
Use synthitect to continue add-api-rate-limiting
```

The agent reads `plans/{ticket_id}/status.md` and the artifact files on disk
and works out the next phase. No chat history required.

## Artifacts per ticket

```text
plans/{ticket_id}/
  ticket.md       # captured request
  status.md       # phase checklist, gates, loop counts; the resume anchor
  research.md     # objective codebase map (questions + findings)
  design.md       # current and target state, patterns, decisions
  structure.md    # vertical slices, checkpoints, file map preview
  spec.md         # tactical implementation plan
  test_spec.md    # Gherkin behavioral contract
```

`status.md` is the checklist. Subagents update it as phases complete. You, or
the orchestrator, record approvals there.

## Human gates

| Gate | What you review | Typical time |
| --- | --- | --- |
| Design | Patterns, decisions, open questions | 5 to 10 min |
| Structure | Vertical slice order, checkpoints | 5 min |
| Plan | Tasks, scenarios, contracts | 10 to 20 min |

Research has no gate. It is facts only. Post-plan phases use automated review
loops (max 3 passes each) instead of human approval.

## Triggers cheat sheet

| Intent | Example |
| --- | --- |
| Start fresh | `Use synthitect to plan out X` |
| Named ticket | `/synthitect my-ticket-slug` |
| Resume | `Use synthitect to continue my-ticket-slug` |
| Approve | `Design approved. Continue synthitect.` |
| Redirect | `Reject design. Use the EventBus pattern from src/foo, not the legacy handler. Revise.` |
| Autopilot after plan | `Plan approved. Run the rest.` |

## After a long design discussion

Your conversation still works as input. Wrap up with:

```text
Use synthitect to plan this out now. Ticket: websocket-reconnect
```

Synthitect captures the request into `ticket.md`, then runs objective
research before design, so the fact-finding phase stays free of solutions
nobody has checked yet.

## Repository layout

| Path | Holds |
| --- | --- |
| `SKILL.md` | Orchestrator instructions |
| `references/` | Subagent briefings, one per phase |
| `plans/` | Per-ticket artifacts (in the project you work on) |

## Requirements

- An agent runtime with subagent/delegation support. Without it, Synthitect
  cannot run phases and will say so, rather than pasting briefings into chat.
- A project `CLAUDE.md` or `AGENTS.md` constitution file for subagents to
  read.

## License

See `LICENSE`. Copyright (C) 2026 browntown development.
