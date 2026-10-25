# Synthitect

**This skill is the formalization of the way I usually code with
agents.** Nothing in it is theoretical. Every phase is a habit that
survived contact with real projects, written down so the agent runs
the same loop I would run by hand.

A workflow for shipping software with AI coding models, in five phases:
vision, research, plan, implementation, review. The human supplies the
vision and the architectural judgment. The model does everything else
and brings receipts.

**Version 2.0 — modernized for current frontier intelligence.**
(V2.1 adds the two-tier execution model below.)

## How it's constructed, and why

The construction mirrors the practice at every level:

- **The phases are the loop I actually run.** I state a high-level
  vision. The model goes and learns things and reports back; if the
  direction sounds right, it writes the formal plan. I rarely read the
  plan — I approved its contents in the research conversation, and the
  document exists as the model's reference, not my homework[^5]. It
  implements. I review for architecture, run the Thermos pass, and ask
  "why is it done this way?" until the answers stop being interesting.
  Then a pull request, an external reviewer, and a merge.
- **The two tiers are my Muse setup.** One big-brain agent plans
  and reviews; fast subagents (Muse Spark) grep the codebase and
  implement the chunks. Judgment work goes to the expensive model,
  throughput work goes to the fast ones, and the reviewer never wrote
  the code it reviews[^3].
- **State lives on disk** because sessions compact, crash, and get
  replaced mid-project, at every model tier. `status.md` is the
  project's memory, not the chat's.
- **There is exactly one approval gate** because there is exactly one
  moment I actually make a decision: when the research comes back and
  the direction is set. V1 gated three more times because the models
  of its era could not be trusted between gates. These can.
- **Tests are regression tooling, not a ritual.** Written with the
  code, aimed at the plan's scenarios. The test-first phase was cut on
  evidence[^1][^2][^4], detailed in the obituary below. Tests drawn
  from an independent specification are a different matter — those
  demonstrably help[^6] — which is why the scenarios live in the plan
  and the implementation takes its expectations from them.

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
effect on outcomes[^1], and the TDAD evaluation found that TDD procedural
instructions alone *increased* regressions[^2]. Scenario thinking did not
die; it moved into the plan, where it always belonged.

V1 is preserved under `legacy/` and at the `v1.0` tag. It is a museum
now. It earned it.

## License

0BSD license. Do whatever you want with the code. Just don't expect it
to work or sue me.

[^1]: Chen, Z., Sun, Z., Shi, Y., Peng, C., Gu, X., Lo, D., & Jiang, L. (2026). *Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents.* arXiv:2602.07900. Across six frontier models on SWE-bench Verified, test-writing frequency had no statistically significant effect on issue resolution; controlled re-prompting to write more or fewer tests did not significantly change outcomes.
[^2]: *TDAD: Test-Driven Agentic Development — Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis.* arXiv:2603.17973. Adding TDD procedural instructions (write tests first) without identifying which existing tests matter raised the test-level regression rate from 6.08% to 9.94% versus a vanilla agent.
[^3]: Song, T.-E. (2026). *Cross-Context Review: Improving LLM Output Quality by Separating Production and Review Sessions.* arXiv:2603.12123. A model reviewing inside its production session anchors on its own reasoning and rationalizes it; a fresh session given only the artifact scrutinizes it. Consistent with the self-correction literature (Huang et al., 2024; Kamoi et al., 2024).
[^4]: *VIBEPASS: Can Vibe Coders Really Pass the Vibe Check?* arXiv:2603.15921. Models that generated their own tests before debugging repaired worse than models given no tests at all (mean P@1 51.8 vs. 58.6) — self-generated test scaffolding added more noise than signal.
[^5]: *Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants.* arXiv:2602.00180. Controlled studies report error reductions up to ~50% when agents work from human-refined specifications; the authors flag the evidence base as still nascent. Cited here for the mechanism — the human refines at the vision level, the artifact anchors the model — not as settled law.
[^6]: Ying, R., Ni, S., Cui, Z., et al. (2026). *Scaling Test-Driven Code Generation from Functions to Classes: An Empirical Study.* arXiv:2602.03557. When tests are supplied as an executable specification, class-level correctness rises 12–26 points across eight models. The value is in independent, correct tests — not in the order they were written.
