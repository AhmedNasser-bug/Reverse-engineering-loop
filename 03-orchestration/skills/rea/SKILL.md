---
name: rea
description: Reverse engineer anything with agents. Analyzes execution traces, binary outputs, API behaviors, and black-box systems to identify causal success factors and synthesize invariants.
---

# REA: Reverse Engineering Anything with Agents

## Overview
The `rea` skill provides automated reverse engineering capabilities inside an agentic loop. It allows the agent to deconstruct why a complex execution succeeded or failed, break down opaque behaviors, generate falsifiable hypotheses, and extract invariant principles that guide subsequent loop iterations.

## When to Use
- **Post-Iteration Success Analysis**: Reverse engineering an iteration output to understand *why* it succeeded rather than just that it passed.
- **Root Cause Deconstruction**: Investigating unexpected failures, hallucinated outputs, or convergence stalls.
- **Black-Box Exploration**: Inspecting external APIs, binary formats, network payloads, or undocumented services.
- **Invariant Synthesis**: Extracting structural rules and success patterns to update the evaluation rubric (`RUBRIC.md`).

## Methodology

```
┌─────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│ Execution Trace │ ──> │ Hypothesis Generator │ ──> │ Falsification Test │
└─────────────────┘     └──────────────────────┘     └────────────────────┘
                                                                │
                                                                ▼
┌─────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│ Rubric Update   │ <── │ Invariant Extraction │ <── │ Causal Factor Map  │
└─────────────────┘     └──────────────────────┘     └────────────────────┘
```

### 1. Trace Ingestion & Deconstruction
- Ingest execution logs, prompt snapshots, tool invocation sequences, and memory diffs.
- Identify transition points where output quality significantly jumped.

### 2. Hypothesis Generation
- Formulate precise, testable hypotheses:
  - *Example*: "Iteration 3 succeeded because web scraping prioritized raw markdown over noisy HTML, reducing context distraction."
  - *Example*: "Tool call ordering with memory lookup before code generation prevented variable re-declaration."

### 3. Falsification Testing
- Evaluate whether the identified factor was strictly necessary or incidental.
- Verify against baseline conditions.

### 4. Invariant Extraction & Rubric Amending
- Convert verified causal factors into explicit rubric criteria.
- Append new evaluation dimensions to `02-loop-engineering/RUBRIC.md`.
- Persist findings into Honcho memory so all future loop iterations inherit the learning.

## CLI Usage in Harness
```bash
# Run REA post-iteration analysis
python 01-rea/rea_reverse_engineer.py --iteration 3 --output artifacts/iteration_3.json

# Extract invariants for rubric update
python 04-processing/eval_agent.py --reverse-engineer
```
