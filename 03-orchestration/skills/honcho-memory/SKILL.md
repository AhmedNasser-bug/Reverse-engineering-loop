---
name: honcho-memory
description: Stateful memory persistence for building multi-turn and cross-iteration AI agents using Honcho. Maintains dialectic context, user profiles, session state, and persistent reverse-engineering insights across loop runs.
---

# Honcho: Stateful Agent Memory Persistence

## Overview
`honcho-memory` leverages [plastic-labs/honcho](https://github.com/plastic-labs/honcho) to provide persistent, cross-iteration memory for the reverse engineering loop harness. Rather than relying on fragile prompt concatenation or losing context when LLM context windows roll over, Honcho constructs a rich dialectic representation of the user, task goals, iteration hypotheses, and discovered invariants.

## Why Honcho in the Loop?
1. **Dialectic Representation**: Models the evolving relationship between the human supervisor, the worker agents, and the evaluation agent.
2. **Context Window Preservation**: Extracts compact, salient semantic facts rather than raw multi-megabyte execution dumps.
3. **Cross-Iteration Recall**: When Iteration 5 starts, it immediately accesses the reverse-engineered insights and failure post-mortems of Iterations 1-4.
4. **Metacognitive Profiling**: Builds persistent awareness of user preferences, stop condition sensitivities, and domain-specific quality constraints.

## Architecture & Integration

```
┌─────────────────────────────────────────────────────────────┐
│                       HONCHO CORE                           │
│  ┌─────────────────┐   ┌─────────────────┐   ┌────────────┐ │
│  │ User Dialectic  │   │ Session Context │   │ Invariant  │ │
│  │ Representation  │   │   & Messages    │   │ Knowledge  │ │
│  └─────────────────┘   └─────────────────┘   └────────────┘ │
└──────────────────────────────▲──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               │                               │
    ┌──────────────────────┐       ┌──────────────────────┐
    │  03-orchestration    │       │   04-processing      │
    │  Honcho Client       │       │   Evaluation Agent   │
    │  (Session & Prompts) │       │   (Learnings & Diffs)│
    └──────────────────────┘       └──────────────────────┘
```

## Python Client Usage
```python
from orchestration.honcho.honcho_client import HonchoMemoryManager

# Initialize memory manager
memory = HonchoMemoryManager(session_id="loop-session-alpha")

# Log user interaction or loop goal agreement
memory.add_message(role="user", content="Ensure data integrity invariant is enforced")
memory.add_message(role="agent", content="Invariant configured in LOOP.md")

# Record reverse-engineered success factor
memory.record_learning(
    iteration=2,
    finding="Prioritizing schema-first parsing resolved 98% of extraction discrepancies.",
    causal_factor="Strict JSON schema validation before transformation"
)

# Retrieve distilled context for next iteration prompt
context = memory.get_context_for_prompt()
```
