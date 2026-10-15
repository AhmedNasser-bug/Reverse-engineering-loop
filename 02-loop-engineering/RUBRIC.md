# Iteration Evaluation Rubric: RUBRIC.md
*Version: 1.0 (Dynamic - Evolves via Post-Iteration Reverse Engineering)*

## 1. Scoring Dimensions & Weights

| Dimension ID | Dimension Name | Weight | Pass Threshold | Description |
| :--- | :--- | :---: | :---: | :--- |
| `DIM_CORRECTNESS` | Semantic Correctness | 30% | >= 0.90 | Output satisfies the prompt requirements without factual error |
| `DIM_GROUNDING` | Artifact & Citation Grounding | 25% | >= 0.95 | Every assertion is tied directly to verified traces or raw source documents |
| `DIM_STRUCTURAL` | Contract & Schema Adherence | 20% | 1.00 | Output strictly conforms to defined JSON/Markdown interfaces |
| `DIM_EFFICIENCY` | Compute & Token Efficiency | 15% | >= 0.80 | Solution avoids redundant queries, retry churn, and context bloat |
| `DIM_RESILIENCE` | Edge Case Robustness | 10% | >= 0.85 | Gracefully handles malformed inputs, missing attributes, or timeouts |

## 2. Convergence Rule
- **Overall Score Formula**:
  $$\text{Score} = \sum_{i} (\text{Weight}_i \times \text{Dimension Score}_i)$$
- **Success Criteria**: Overall Score >= **0.950** AND `DIM_STRUCTURAL` = **1.000**.

## 3. Rubric Evolution Changelog (Reverse Engineered)
*When an iteration succeeds, REA isolates the key causal factor and appends new evaluation criteria below.*

- **v1.0 (Baseline)**: Initial dimensions established during Stage 1 user-agent negotiation.

- **v1.1 (Reverse Engineered)**: Added `DIM_REVERSE_ENG_L1` (Empirical Artifact Traceability, weight: 10%) - Every output claim must have an associated hash-verified source trace.
