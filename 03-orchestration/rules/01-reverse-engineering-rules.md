# Rule 01: Reverse Engineering & Rubric Evolution Protocol

## 1. Post-Iteration Reverse Engineering Requirement
- Passing an iteration is NOT the end of the step.
- The harness MUST execute the **Reverse Engineering Analyzer** on the iteration output:
  - Deconstruct *why* the iteration succeeded.
  - Isolate the causal factors (prompt framing, retrieval strategy, tool sequencing, data filtering).
  - Distinguish between correlated noise and causal determinants.

## 2. Dynamic Rubric Evolution
- The evaluation rubric (`RUBRIC.md`) must dynamically anneal as new success factors are discovered.
- When a causal factor is confirmed:
  1. The **Evaluation Agent** formulates a new rubric criterion or adjusts dimension weights.
  2. The rubric version is incremented (e.g., `v1.0` -> `v1.1`).
  3. The updated rubric is committed to `02-loop-engineering/RUBRIC.md`.
  4. The next iteration's evaluation task is queued against this refined rubric.

## 3. Feedback Loop to Honcho Memory
- Every discovered causal factor and rubric amendment is immediately committed to Honcho persistent memory.
- Worker agents in the subsequent iteration receive these insights in their context prompt, ensuring continuous performance acceleration.
