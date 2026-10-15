# Loop Engineering Specification: LOOP.md

## 1. Loop Objective & Scope
- **Task Title**: High-Value Strategic Agentic Loop Execution
- **Goal Statement**: Execute an engineered, self-correcting agent loop for complex strategic, high-volume, or compute-intensive workloads while maintaining persistent context and evolving quality rubrics.

## 2. Mandatory Loop Invariant (Human Approved)
> [!IMPORTANT]
> **INVARIANT**: All intermediate and final claims must be strictly grounded in empirical execution artifacts, verified traces, and cited data sources. Zero ungrounded hallucinations permitted. All schema outputs must strictly conform to contract definitions.
- **Human Approval Status**: APPROVED
- **Approved At**: 2026-10-15T04:30:00Z
- **Approval Signature**: user@reverse-engineering-loop

## 3. Stop Conditions
| Condition | Parameter | Threshold / Rule |
| :--- | :--- | :--- |
| **Success Convergence** | `rubric_score` | Score >= 0.95 across all evaluation dimensions in `RUBRIC.md` |
| **Max Iterations** | `max_iterations` | 10 iterations |
| **Cost Budget Ceiling**| `max_budget_usd` | $5.00 total LLM / compute cost |
| **Stagnation Trap** | `min_delta` | Score delta < 0.02 for 3 consecutive iterations |
| **Invariant Violation** | `invariant_check`| Any unverified invariant breach immediately aborts loop |

## 4. Iteration Phase Mapping
1. **Context Hydration**: Load latest learnings and state from Honcho.
2. **Worker Dispatch**: Execute processing or task units.
3. **Trace Collection**: Capture execution artifacts and raw logs.
4. **Evaluation Dispatch**: Run Evaluation Agent against current `RUBRIC.md`.
5. **Reverse Engineering**: Analyze causal factors of success/failure via REA.
6. **Rubric Evolution**: Amend `RUBRIC.md` with newly isolated invariants.
7. **Telemetry & Stream**: Broadcast iteration events to OpenUI web dashboard.