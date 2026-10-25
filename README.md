# Synthitect

A workflow for shipping software with AI coding models, in five phases:
vision, research, plan, implementation, review. The human supplies the
vision and the architectural judgment. The model does everything else
and brings receipts.

**Version 2.0 — modernized for current frontier intelligence.**
(V2.1 adds the two-tier execution model below.)

## Usage

```
/synthitect [your high-level vision]
```

1. **Research.** The model investigates the codebase and the facts,
   then reports the findings and a proposed direction back to you, in
   conversation. You approve, redirect, or kill it. This is the only
   gate in the workflow.
2. **Plan.** The model writes the formal plan: architecture decisions,
   chunks, acceptance scenarios. It is written for the model, as its
   working reference. You will probably never read it. That is the
   design, not a defect — you already approved everything in it during
   step 1.
3. **Implementation.** Chunk by chunk, tests written with the code,
   commands run and recorded.
4. **Review.** A fresh context that did not write the code reviews it
   against the plan and the project constitution, Thermos pass included
   where one exists. Findings that question the architecture come back
   to you as questions. Rounds are capped at three.
5. **Ship.** Pull request, external reviewer, merge.

Progress lives on disk in `plans/{ticket_id}/status.md`, so any session
can pick the work up where the last one left off.

Execution runs on two tiers. A frontier model **orchestrates**: it
holds the vision, writes the plan, talks to the human, and reviews.
Fast worker models (Muse Spark subagents, in Muse) do the
legwork — **Scouts** grep and trace the codebase and report cited
facts, **Implementers** enact one plan chunk each. Judgment work goes
to the expensive brain; throughput work goes to the fast ones; and the
reviewer's fresh context stops being a discipline problem, because the
reviewer genuinely never wrote the code.

Install: copy `SKILL.md` and `references/` into your agent's skills
directory.

## Version 1.0, an obituary

V1 shipped in the era of stupid models. Its reference test subject was
MiniMax M2.7, a model that could not hold a plan across twenty turns,
wrote tests that faithfully encoded its own misunderstandings, and
declared victory without running anything. V1 corrected those failure
modes the only way available: eight phases, three human approval gates,
a separate subagent for every concern, and a test-first inquisition
with its own review loop. It worked. It was also exhausting, in the
way that managing a talented but unreliable intern through a checklist
is exhausting.

The failure modes were real. The models were stupid. Both statements
expired, at different rates.

Frontier models now hold the plan, do the research unprompted, and run
the tests because the tests are there. What they still do is drift
across long sessions, rationalize their own code in review, and cut
corners on architecture in ways that only show up later. So V2 keeps
exactly the parts of V1 that were never about model IQ:

- State on disk, because sessions are mortal even when models are not.
- Independent review in a fresh context, because the producer of code
  is the worst reviewer of it, at any intelligence level.
- Evidence over adjectives, loop caps over infinite polish.

And it deletes the rest, including the test-first phase. Tests matter —
they are how a codebase stays un-regressed. Writing them *first*, for a
model, measurably does not matter: a 2026 study of frontier agents on
real issue resolution (Chen et al., "Rethinking the Value of
Agent-Generated Tests") found test-writing frequency had no significant
effect on outcomes, and the TDAD evaluation found that TDD procedural
instructions alone *increased* regressions. Scenario thinking did not
die; it moved into the plan, where it always belonged.

V1 is preserved under `legacy/` and at the `v1.0` tag. It is a museum
now. It earned it.

## License

0BSD license. Do whatever you want with the code. Just don't expect it
to work or sue me.
