# multi-agent-research

Planner → Researcher → Writer → Critic.

Four agents with distinct roles hand a research task down a pipeline, each one consuming the previous agent's output and producing a bounded artifact of its own — a pattern for decomposing one vague ask into a verifiable chain of specific work.

## How it works

1. **Planner** — breaks the topic into a short list of concrete sub-questions.
2. **Researcher** — answers each sub-question from its assigned sources.
3. **Writer** — synthesizes the research into a single coherent draft.
4. **Critic** — reviews the draft against the original topic and flags gaps, unsupported claims, or missed sub-questions before final output.

Each handoff is logged, so the full chain of reasoning — not just the final answer — is inspectable.

## Usage

```bash
python multi_agent_research.py --topic "your research topic"
```

## Why this exists

A single model asked to "research and write about X" tends to skip steps under its breath. Splitting the roles makes each step a small, checkable unit, and gives the Critic agent something concrete to grade against instead of vibes.

## Stack

Python · pluggable per-agent model backend
