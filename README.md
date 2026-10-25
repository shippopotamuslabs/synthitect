# Synthitect

This skill is the formalization of the way I usually code with agents.
Every phase in it is a habit that survived real projects. I wrote the
habits down so the agent runs the same loop I run by hand.

Five phases: vision, research, plan, implementation, review. The human
supplies the vision and the architectural judgment. The model does the
rest and brings receipts.

Version 2.0: modernized for current frontier intelligence.
Version 2.1 adds the two-tier execution model.

## How it is constructed, and why

The phases are the loop I run. I state a high-level vision. The model
goes and learns things and reports back. If the direction sounds
right, it writes the formal plan. I skim the plan. One pass, looking
for direction and obvious problems. I skip the twenty-minute read with
every code reference checked, and on small tickets I skip the read
entirely. The research conversation is where I approved the contents.
The document itself is the model's reference[^5]. Then it implements.
I review for architecture, run the Thermos pass, and ask "why is it
done this way?" until the answers stop being interesting. Then a pull
request, an external reviewer, and a merge.

The two tiers are my Muse setup. One big-brain agent plans and
reviews. Fast subagents, Muse Spark, grep the codebase and implement
the chunks. Judgment work goes to the expensive model. Throughput work
goes to the fast ones. The reviewer never wrote the code it
reviews[^3].

State lives on disk. Sessions compact, crash, and get replaced
mid-project, at every model tier. `status.md` holds the project's
memory. Chats lose theirs.

There is one approval gate. One moment in the loop has me making a
real decision: the research comes back and the direction gets set.
V1 gated three more times. Its models needed supervision between
gates. Current models hold up.

Tests guard regressions. That is their job, and they do it written
with the code, aimed at the plan's scenarios. The test-first phase was
cut on evidence[^1][^2][^4], detailed in the obituary below. Tests
drawn from an independent specification help a great deal[^6]. The
scenarios therefore live in the plan, and the implementation takes its
expectations from the plan.

## Usage

```
/synthitect [your high-level vision]
```

1. Research. The model investigates the codebase and the facts, then
   reports the findings and a proposed direction back to you, in
   conversation. You approve, redirect, or kill it. This is the only
   gate in the workflow.
2. Plan. The model writes the formal plan: architecture decisions,
   chunks, acceptance scenarios. The model reads this document for the
   rest of the job. You skim it at most, and on small work you skip it.
   You approved its contents during step 1.
3. Implementation. Chunk by chunk. Tests written with the code.
   Commands run and recorded.
4. Review. A fresh context that never wrote the code reviews it
   against the plan and the project constitution, Thermos pass
   included where one exists. Findings about the architecture itself
   come back to you as questions. Rounds cap at three.
5. Ship. Pull request, external reviewer, merge.

Progress lives on disk in `plans/{ticket_id}/status.md`. Any session
can pick the work up where the last one left off.

Execution runs on two tiers. A frontier model orchestrates: it holds
the vision, writes the plan, talks to the human, and reviews. Fast
worker models run the legwork. Scouts grep and trace the codebase and
report cited facts. Implementers enact one plan chunk each. The
orchestrator reviews code other models wrote, so its fresh context
comes from the structure of the thing.

Install: copy `SKILL.md` and `references/` into your agent's skills
directory.

## Version 1.0, an obituary

V1 shipped in the era of stupid models. Its reference test subject was
MiniMax M2.7, a model that could hold a plan for about twenty turns,
wrote tests that encoded its own misunderstandings down to the letter,
and declared victory with nothing run. V1 corrected those failure
modes the only way available: eight phases, three human approval
gates, a separate subagent for every concern, and a test-first
inquisition with a review loop of its own. It worked. It was also
exhausting, the way managing a talented, unreliable intern through a
checklist is exhausting.

The failure modes were real. The models were stupid. Both statements
expired, at different rates.

Frontier models hold the plan now. They do the research unprompted.
They run the tests because the tests are there. They still drift
across long sessions. They still talk themselves into their own code
at review time. They still shave architectural corners that only show
up later. So V2 keeps the parts of V1 aimed at those problems:

- State on disk. Sessions end. The work continues from the file.
- Independent review in a fresh context. The producer of code grades
  its own homework generously, at every intelligence level.
- Evidence over adjectives. Loop caps over endless polish rounds.

The rest got deleted, the test-first phase included. Tests keep a
codebase from regressing, and that work matters. Writing them first,
for a model, carries no measurable effect: a 2026 study of frontier
agents on real issue resolution (Chen et al., "Rethinking the Value of
Agent-Generated Tests") found test-writing frequency had no
significant effect on outcomes[^1], and the TDAD evaluation found TDD
procedural instructions alone raised regressions[^2]. Scenario
thinking moved into the plan. It does its work there.

V1 sits under `legacy/` and at the `v1.0` tag. It is a museum now. It
earned it.

## License

0BSD license. Do whatever you want with the code. Just don't expect it
to work or sue me.

[^1]: Chen, Z., Sun, Z., Shi, Y., Peng, C., Gu, X., Lo, D., & Jiang, L. (2026). *Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents.* arXiv:2602.07900. Across six frontier models on SWE-bench Verified, test-writing frequency had no statistically significant effect on issue resolution. Controlled re-prompting to write more or fewer tests left outcomes statistically unchanged.
[^2]: *TDAD: Test-Driven Agentic Development — Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis.* arXiv:2603.17973. Adding TDD procedural instructions (write tests first) without identifying which existing tests matter raised the test-level regression rate from 6.08% to 9.94% versus a vanilla agent.
[^3]: Song, T.-E. (2026). *Cross-Context Review: Improving LLM Output Quality by Separating Production and Review Sessions.* arXiv:2603.12123. A model reviewing inside its production session anchors on its own reasoning and rationalizes it. A fresh session given only the artifact scrutinizes it. Consistent with the self-correction literature (Huang et al., 2024; Kamoi et al., 2024).
[^4]: *VIBEPASS: Can Vibe Coders Really Pass the Vibe Check?* arXiv:2603.15921. Models that generated their own tests before debugging repaired worse than models given no tests at all (mean P@1 51.8 vs. 58.6). Self-generated test scaffolding added more noise than signal.
[^5]: *Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants.* arXiv:2602.00180. Controlled studies report error reductions up to ~50% when agents work from human-refined specifications. The authors flag the evidence base as still early. Cited for the mechanism: the human refines at the vision level, the artifact anchors the model.
[^6]: Ying, R., Ni, S., Cui, Z., et al. (2026). *Scaling Test-Driven Code Generation from Functions to Classes: An Empirical Study.* arXiv:2602.03557. Tests supplied as an executable specification raise class-level correctness 12 to 26 points across eight models. Independent, correct tests carry the value. The order they were written in carries none.
