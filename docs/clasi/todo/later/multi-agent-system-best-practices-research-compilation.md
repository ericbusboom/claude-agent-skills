---
status: pending
---

# Multi-agent system best practices — research compilation

Reference document for future CLASI architecture decisions. Compiled
2026-04-30 from primary sources. Not a sprint plan — material that's
still useful 6 months out.

## Why we cared

CLASI is a 3-agent system: `team-lead` (orchestrator) → `sprint-planner`
(planning specialist) and `programmer` (implementation specialist). We
wanted to know what recognized authorities recommend for systems like
this, and whether the failure modes we've already hit (hallucinated
"done" reports, worktree collisions, etc.) are documented elsewhere
with mitigations.

## TL;DR for CLASI

The 3-agent hierarchical shape is squarely in the recommended pattern.
The known risk surface — hallucinated "done", worktree collisions,
summary fidelity, cost runaway — matches what's documented across the
literature. The strongest leverage points all consistently named:

1. **Rigorous structured briefs** to sub-agents (objective + output
   format + boundaries + tool guidance).
2. **End-state verification**, not trusting sub-agent self-reports.
3. **Dispatch logs with cost tracking** (multi-agent uses ~15x tokens
   of single-agent chat).
4. **Small-N real-task eval set** for regression detection.
5. **Don't parallelize agents touching the same files** (prefer serial
   or worktree isolation).

---

## 1. Anthropic's published guidance

**"Building Effective Agents"** (Schluntz & Zhang, Dec 2024) names
five workflow patterns — prompt chaining, routing, parallelization,
**orchestrator-workers**, and evaluator-optimizer — and warns:
> "find the simplest solution possible, and only increase complexity
> when needed."
Agents trade latency and cost for performance and risk compounding
errors.
Source: <https://www.anthropic.com/research/building-effective-agents>

**"How we built our multi-agent research system"** (Jun 2025) is the
strongest primary source for CLASI's pattern.
Source: <https://www.anthropic.com/engineering/multi-agent-research-system>

Headline lessons:

- **Cost reality:** agents use ~4x chat tokens; multi-agent uses ~15x.
  Token usage explains 80% of performance variance. Justified only
  when task value is high.
- **When it hurts:** "Most coding tasks involve fewer truly
  parallelizable tasks than research, and LLM agents are not yet
  great at coordinating and delegating to other agents in real time."
  Tasks needing shared context or heavy interdependencies should stay
  single-agent.
- **Orchestrator pattern:** lead agent uses extended thinking to plan,
  then spawns subagents with explicit scaling rules ("simple
  fact-finding: 1 agent, 3-10 calls; comparisons: 2-4 subagents;
  complex: >10").
- **Context passing:** every dispatch must specify "objective, output
  format, tool/source guidance, clear task boundaries." Vague briefs
  cause duplication and gaps. For long horizons, store plans in
  external memory and spawn fresh-context subagents.
- **Tool design:** bad tool descriptions derail agents; an internal
  "tool-testing agent" rewrote descriptions and cut task time 40%.
- **Failure modes observed:** over-spawning (50 subagents for trivial
  queries), SEO-content-farm bias, task duplication from vague briefs,
  hallucinated answers on edge cases.
- **Fixes:** explicit prompt-level scaling rules, source-quality
  heuristics, end-state evals, human review for what automation
  misses.

## 2. OpenAI / Microsoft / Google

**OpenAI Agents SDK** (successor to Swarm) ships two patterns:
- **Manager (agents-as-tools)** — orchestrator stays in control
- **Handoffs** — peer-to-peer transfer

Docs explicitly recommend Manager when you need a single conversation
owner.
Sources:
- <https://openai.github.io/openai-agents-python/multi_agent/>
- <https://cookbook.openai.com/examples/orchestrating_agents/>

**Microsoft Magentic-One** (arXiv 2411.04468) puts an Orchestrator
on top of specialized workers (WebSurfer, FileSurfer, Coder,
ComputerTerminal). The Orchestrator runs:
- An **outer loop** maintaining a Task Ledger (facts + plan)
- An **inner loop** maintaining a Progress Ledger (who acts next; are
  we stuck; are we done)

Microsoft also ships **AutoGenBench** for repeatable agentic eval.
Sources:
- <https://arxiv.org/abs/2411.04468>
- <https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/magentic-one.html>

**Google Gemini** agent docs emphasize tool-using single agents over
coordinated swarms (no authoritative source for a hierarchical multi-
agent recommendation — common practice).

## 3. Open-source / community consensus

- **LangGraph** documents **supervisor** and **hierarchical-teams**
  patterns. Recommends "supervisor pattern via tools rather than
  libraries" for context-engineering control. Multi-level supervisors
  endorsed for complex domains.
  <https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/>

- **CrewAI** ships `Process.hierarchical` with a `manager_agent`.
  Practitioner reports flag a known pitfall: the default manager
  often executes all tasks sequentially rather than selectively
  delegating; fix with a custom manager that runs explicit triage.
  <https://docs.crewai.com/en/learn/hierarchical-process>
  <https://towardsdatascience.com/why-crewais-manager-worker-architecture-fails-and-how-to-fix-it/>

- **Aider** is two-agent: Architect (reasoner) + Editor (diff
  producer). Splitting reasoning from editing reached SOTA 85% on
  Aider's bench.
  <https://aider.chat/2024/09/26/architect.html>

- **SWE-bench Verified leaderboard** is dominated by systems mixing
  single-agent loops with multi-rollout/review (Verdent, Claude Code,
  Codex scaffolds added Feb 2026).
  <https://www.swebench.com/verified.html>
  <https://swe-bench-live.github.io/>

- **Claude Code subagents docs:**
  - "Give each subagent one clear goal, input, output, and handoff
    rule"
  - Restrict tools per subagent
  - "two subagents editing the same file in parallel is a recipe for
    conflict"
  <https://code.claude.com/docs/en/sub-agents>
  <https://claude.com/blog/subagents-in-claude-code>

**Dominant views:**
- Hierarchical orchestrator-worker beats peer-to-peer for production
  reliability.
- Specialized agents with restricted tools beat one generalist with
  role-prompts.
- Parallel dispatch only when truly independent.
- Structured output (named format in the brief) over free text.
- External memory beats stuffing context.
- Escalate to human on novel/edge queries (Anthropic) and on
  Progress-Ledger "stuck" detection (Magentic-One).

## 4. Failure modes and mitigations (cross-cutting)

The **MAST taxonomy** (Cemri et al., NeurIPS 2025, arXiv 2503.13657)
analyzed 1,600+ traces and reports 41-86.7% failure rates, mapped to
three roots: **specification ambiguity, coordination breakdowns,
verification gaps** (14 sub-modes).
<https://arxiv.org/pdf/2503.13657>

| Failure | Mitigation | Source |
|---|---|---|
| Hallucinated "done" reports | End-state evals (verify final artifact, not agent's claim); LLM-as-judge with pass/fail | Anthropic multi-agent post |
| Context bloat from returns | Subagent returns final-message-only; structured JSON; store plans externally | Claude Code subagents docs; Anthropic |
| Worktree collisions | Don't parallelize agents touching the same files | Claude Code docs |
| Cost runaway / over-spawn | Explicit prompt-level scaling rules; budget per dispatch | Anthropic |
| Summary fidelity loss | Citation-accuracy eval criterion; verbatim quoting in briefs | Anthropic |
| "Talking past each other" | Unified protocol, named output format | MAST + hallucination survey |
| Manager mis-delegates | Custom manager with explicit triage step | CrewAI community |

## 5. Evaluation and observability

- **Benchmarks:** SWE-bench Verified (500 human-validated instances),
  SWE-bench-Live (50 new issues/month, Windows variant Feb 2026),
  AutoGenBench, GAIA, Aider's leaderboard.
  <https://www.swebench.com/>
  <https://openai.com/index/introducing-swe-bench-verified/>

- **Eval design (Anthropic):**
  - Start with ~20 real-usage queries; small-N suffices early because
    effect sizes are large (30% → 80%).
  - Single-prompt LLM-as-judge with 0.0-1.0 score plus pass/fail
    outperforms multi-call rubrics.
  - **Evaluate end state, not every step**, with discrete checkpoints
    for long workflows.
  - Keep humans in the loop for unusual-query and source-bias
    detection.

- **Observability:**
  - Full per-agent tracing of decisions and dispatch structure (not
    necessarily message contents).
  - Rainbow deployments — agents may be mid-process at deploy time.
  - Cost / token tracking per dispatch is mandatory given the 15x
    multiplier.

## What this implies (suggestions, not prescriptions)

- **Brief discipline.** Sprint-planner's prompt-template should
  encode all four required brief elements (objective, output format,
  tool guidance, boundaries). Currently the dispatch templates are
  loose. Possible TODO.
- **End-state verification.** `move_ticket_to_done` already validates
  ACs and tests; that's good. But the team-lead currently trusts the
  programmer's *report* of what changed before validating. Consider
  capturing the actual diff and running the test command from the
  team-lead side at handoff, not just trusting the report.
- **Cost tracking.** We log dispatches but not token cost. Worth a
  small add to the dispatch_log.
- **Eval set.** No real-task eval exists for CLASI. ~20 representative
  TODOs run end-to-end through the SE process would catch regressions
  in the orchestration prompts. Currently we rely on unit + system
  tests of MCP tools, which don't cover orchestration quality.
- **Worktree collisions.** Sprint 011's serial execution sidestepped
  this, but the `parallel-execution` skill exists and uses worktrees.
  Document its constraints (no two tickets touching the same file)
  rather than discovering it the hard way.
- **Manager mis-delegation.** team-lead currently dispatches by
  subcommand routing in the role definition. Worth periodically
  reviewing whether the team-lead is *actually* delegating
  (programmer doing the work) vs. doing work itself (rare per the
  role-guard hooks). Spot-check via dispatch log.

## Out of scope for this TODO

This is a reference document. Concrete actions worth their own TODOs
if pursued:

- Add token-cost tracking to `dispatch_log` (small, OOP-able).
- Add a small CLASI eval set (~20 representative TODOs) and a runner.
- Audit dispatch templates for the four required brief elements.
- Document `parallel-execution` skill's "no shared file paths"
  constraint explicitly in its skill body.

## Origin

Stakeholder asked: "do some research on what are the recommendations
for best practices for multi-agent systems. There's got to be
somebody who's compiled details on how to engage with multiple agents
and what that looks like." Research dispatched and synthesized;
primary sources cited inline.
