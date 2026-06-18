# Synthitect

Structured agent workflow for shipping features with AI coding tools. Synthitect
orchestrates specialized subagents through alignment, planning, test-driven
implementation, and review — with human gates where judgment matters and on-disk
artifacts so work resumes across sessions and subscriptions.

## What it does

Synthitect turns a feature request into reviewed, tested code through a fixed
pipeline. Each phase has a dedicated subagent briefing in `references/`. The
orchestrator delegates phase work, stops at approval gates, and persists
progress under `plans/{ticket_id}/` so you never re-explain context after
switching tools.

```text
Research → Design → Structure → Plan → TDD Red → Red Review → Implement → Final Review
              ↑          ↑         ↑
         human gate  human gate  human gate
```

**Alignment (before code)** — objective codebase research, a design discussion
artifact, and a vertical-slice structure outline. Catch wrong patterns early in
documents you can read in minutes, not in a thousand-line plan.

**Planning** — `spec.md` (implementation contract) and `test_spec.md` (Gherkin
scenarios with literal expected values, mutation-defense included).

**Execution** — failing tests first, red-phase integrity review, implementation
to green, final evidence-backed review. Review loops rerun only for admissible
findings (correctness, drift, weak coverage) — not style nits.

## Quick start

### Install the skill

Point your agent skills directory at this repo:

```bash
ln -sfn /path/to/synthitect ~/.grok/skills/synthitect
```

Works the same for Claude Code, Codex, or any runtime that loads skills from a
path. The repo root *is* the skill (`SKILL.md` + `references/`).

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

TDD Red through Final Review runs without further approvals unless a review loop
needs correction.

### Resume after switching tools

```text
Use synthitect to continue add-api-rate-limiting
```

The agent reads `plans/{ticket_id}/status.md` and artifact files on disk to
infer the next phase. No chat history required.

## Artifacts per ticket

```text
plans/{ticket_id}/
  ticket.md       # captured request
  status.md       # phase checklist, gates, loop counts — resume anchor
  research.md     # objective codebase map (questions + findings)
  design.md       # alignment: current/target state, patterns, decisions
  structure.md    # vertical slices, checkpoints, file map preview
  spec.md         # tactical implementation plan
  test_spec.md    # Gherkin behavioral contract
```

`status.md` is the checklist. Subagents update it when phases complete; you (or
the orchestrator) record approvals there.

## Human gates

| Gate | What you review | Typical time |
| --- | --- | --- |
| Design | Patterns, decisions, open questions | 5–10 min |
| Structure | Vertical slice order, checkpoints | 5 min |
| Plan | Tasks, scenarios, contracts | 10–20 min |

Research has no gate — it is facts only. Post-plan phases use automated review
loops (max 3 passes each) instead of human approval.

## Triggers cheat sheet

| Intent | Example |
| --- | --- |
| Start fresh | `Use synthitect to plan out X` |
| Named ticket | `/synthitect my-ticket-slug` |
| Resume | `Use synthitect to continue my-ticket-slug` |
| Approve | `Design approved. Continue synthitect.` |
| Redirect | `Reject design — use EventBus pattern from src/foo, not legacy handler. Revise.` |
| Autopilot after plan | `Plan approved. Run the rest.` |

## After a long design discussion

Your conversation still works as input. Wrap up with:

```text
Use synthitect to plan this out now. Ticket: websocket-reconnect
```

Synthitect captures the request into `ticket.md`, then runs objective research
before design — so the agent maps the codebase without baking premature
solutions into the fact-finding phase.

## Repository layout

```text
SKILL.md              # orchestrator instructions
references/           # subagent briefings (one per phase)
plans/                # per-ticket artifacts (gitignored or committed per project)
```

## Requirements

- An agent runtime with **subagent/delegation** support. Without it, Synthitect
  cannot run phases and will say so rather than paste briefings into chat.
- A project `CLAUDE.md` or `AGENTS.md` constitution file for subagents to read.

## License

See [LICENSE](LICENSE).