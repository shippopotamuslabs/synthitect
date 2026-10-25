# Synthitect

Synthitect is one engineer's habits for coding with agents, written
down as a skill. It claims no authority. It is the way Sean Brown
happens to work, formalized so an agent can run the same loop he runs
by hand. Take what survives contact with your own projects and leave
the rest.

It has two layers. The bottom layer is agent engineering: one
frontier model plans and reviews, smaller workhorse models run the
legwork. The top layer is the workflow those agents run: vision,
research, plan, implement, review, ship. State lives on disk under
both layers, because sessions are mortal and projects are not.

Version 2.0: modernized for current frontier intelligence.
Version 2.1 adds the two-tier execution model, layer one below.

## Usage

```
/synthitect [your high-level vision]
```

Install: copy `SKILL.md` and `references/` into your agent's skills
directory.

## Layer one: the agent engineering

Three roles. Each role's work is priced for the brain doing it.

**The Orchestrator** is a frontier model. It holds the vision, writes
the plan, talks to the human, and reviews the result. It never
implements. Its context window is the scarcest resource in the whole
system, so the design spends that context on decisions. File contents
are cheap to fetch and expensive to hold; the Orchestrator reads code
to check a claim or to review a diff, and delegates the rest.

**Scouts** are workhorse models (Muse Spark subagents, in Muse
Code) doing read-only legwork. A scout answers one factual question
about the codebase: every caller of this function, where this module
persists its state, which tests touch this table. It answers with
file:line citations and quoted lines, and it runs in parallel with its
siblings. A scout with an opinion is a bug. Facts come back, the
Orchestrator does the thinking.

**Implementers** are workhorse models too, one per plan chunk. An
implementer enacts its chunk, writes the chunk's tests, and reports
back in evidence: files changed, commands run, results. Anything it
finds that reaches past its chunk comes back as a flag for the
Orchestrator. Implementers never widen their own scope.

Why this shape works:

Judgment and throughput are different goods, and they cost different
amounts. Planning a migration and reviewing a diff burn capability.
Grepping for callers and typing a scoped chunk burn tokens. Frontier
prices for grep work are waste, and a workhorse model holding the
whole architecture in its head is a risk. The split prices each job
at what the job actually is.

Review independence stops depending on discipline. A model reviewing
code inside the session that produced it defends the code; the
research on this is blunt[^3]. In this setup the reviewer never wrote
the code under review, because a different model did. The structure
supplies what prompting tricks cannot.

Escalation has one path: worker, Orchestrator, human. Architecture
questions and genuine blockers reach the human. Everything else
resolves below that line, and the Orchestrator spot-checks any worker
claim a decision stands on before acting on it.

## Layer two: the workflow

Five phases run on top of layer one. Each one sits where it sits for
a reason.

**1. Vision discussion.** The human states the vision at the level he
thinks at: the architecture, the intent, the constraints already
known. The Orchestrator fans scouts out over the codebase, checks the
facts the vision depends on, and reports back in conversation: what
exists, the direction it proposes, the alternative it rejected, the
questions only the human can answer. The human approves, redirects,
or kills it. This is the only approval gate in the workflow, and its
placement is the point. A wrong direction caught in conversation
costs a conversation. The same direction caught after implementation
costs the implementation.

**2. Plan.** The Orchestrator writes the formal plan: the goal,
architecture decisions with the reasons behind them, the work broken
into ordered chunks, and acceptance scenarios for each chunk, stated
as behavior a test can check. The plan is the model's working
reference, and it is written for that reader. The human skims it, one
pass for direction and obvious problems, and on small tickets does
not read it at all. It works anyway. Writing the decomposition down
forces it into the open before code exists, and the file anchors the
work hours later, when the session has drifted and the original
conversation is gone. The research on spec-driven work points the
same way, with the human refining at exactly this level: the
vision[^5].

**3. Implement.** Implementers take one chunk at a time, in plan
order. Tests are written with the code, and their expectations come
from the plan's scenarios, never from calling the code under test. A
chunk ends when its scenarios hold and its commands pass, with the
results recorded. An architectural surprise stops the line: it goes
back to the Orchestrator and reaches the human as a question, and
nobody improvises a new architecture mid-chunk.

Tests ride along with the code here instead of leading it, and that
ordering is an evidence call, not a taste call. Agent-written tests,
imposed as a first phase, do not move resolution outcomes[^1], can
raise regressions when the procedure is all the agent is given[^2],
and make debugging worse when the model writes its own scaffolding
before repairing[^4]. Supplied, independent specifications are a
different animal: they raise correctness substantially[^6]. So the
scenarios live in the plan, written before the code and independent
of it, and the tests take their orders from there.

**4. Review.** The Orchestrator reviews the diff against the plan and
the project constitution, scouts tracing callers where the review
needs them, Thermos pass folded in where a project has one. Findings
follow an admissibility rule carried over from V1, the best rule V1
had: a finding names a concrete failure mode, cites file:line, and
brings command evidence, or it does not get reported. Style taste
stays home. Findings about the architecture itself come back as
questions, current shape against alternative, each stated on its own
merits. The human asks why it is done this way, the work changes what
needs changing, and the loop runs again, three rounds at most.
Anything still standing after round three arrives as a stated
disagreement. No fourth round, no quiet merge.

**5. Ship.** Pull request under the repo's own conventions, external
reviewer, merge. The state file gets marked complete, and the
ticket's paper trail (plan, research, review rounds) sits in
`plans/{ticket_id}/` for whoever picks the project up next, human or
model.

Underneath both layers, the state file does quiet work. Sessions
compact, crash, and get replaced by newer sessions with no memory of
the old ones. `status.md` holds the checklist, the gate state, the
loop counts, and the notes with the last commands and their results.
Any session, at either tier, reads the file and knows where the work
stands. The chat is a conversation. The file is the memory.

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

The rest got deleted, the test-first phase included. Scenario
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
