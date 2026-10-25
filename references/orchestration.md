---
description: Orchestration reference for Synthitect v2.1 — the two-tier execution model.
---

# Orchestration: Orchestrator and Workers

Synthitect runs on two tiers. The **Orchestrator** (a frontier model)
plans, talks to the human, and reviews. **Workers** (fast, cheaper
models — Muse Spark subagents in Muse) gather information and
implement. This file defines the roles and the assignment shapes. It is
a reference for the Orchestrator, not a phase briefing.

## Why the split exists

- Planning and architectural review are judgment work; they are what
  the expensive model's capability is actually for.
- Grepping a codebase and enacting a scoped chunk are throughput work;
  a fast model does them at the same quality for a fraction of the cost
  and context.
- The split buys the Review phase its fresh context for free: the
  Orchestrator reviews code it genuinely did not write.

## The Scout (read-only)

Spawn scouts in parallel whenever the Orchestrator needs facts it does
not have: during Research, and during Review for caller/callee tracing.

Assignment shape:

```markdown
You are a Scout. Answer only the question below, from the code.
Question: [one factual question — e.g. "every caller of X", "how module
Y persists Z", "which tests cover W"]
Rules: read-only; cite file:line for every fact; quote the decisive
lines; if the answer is not in the code, say so instead of inferring;
no recommendations, no opinions, no code changes.
Return: the facts, each with its citation, then a one-line summary.
```

Scout output is raw material. The Orchestrator synthesizes it; a scout
never writes the research report and never addresses the human.

## The Implementer

One implementer per plan chunk, briefed with
`references/implementation-briefing.md` plus chunk-specific context: the
chunk's plan section, its acceptance scenarios, and the files it may
touch. The implementer's world is the chunk. Anything it discovers that
reaches beyond the chunk — a plan contradiction, an architectural
surprise — comes back in its report as a flag, not a decision.

## Conduct rules

- **Context hygiene.** Workers return summaries and citations, not file
  dumps. The Orchestrator reads source directly only to spot-check a
  load-bearing claim or to review the final diff.
- **Spot-check before building.** Any scout or implementer claim a
  decision depends on gets verified against the cited lines before the
  Orchestrator acts on it. Verify the decisive ones; trust the rest.
- **Serialization.** Scouts parallelize freely. Implementers serialize
  when chunks share files, a build, or a test suite that cannot run
  concurrently in the environment. Parallel implementers on truly
  independent chunks are fine.
- **Escalation path.** Worker → Orchestrator → human. Workers never
  escalate sideways or directly to the human; the Orchestrator decides
  what is worth the human's attention — mostly architecture questions
  and genuine blockers.
- **Same model everywhere?** Acceptable. The tier split then lives in
  the role discipline (plan first, review as a stranger) rather than in
  model choice, and the briefing structure still enforces it.
