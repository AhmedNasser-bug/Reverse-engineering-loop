# Rule 00: Loop Invariant & Human Approval Protocol

## 1. Absolute Invariant Definition
- Before ANY loop iteration begins, an explicit, unambiguous **Loop Invariant** must be established.
- The invariant defines the boundaries of truth, safety, and acceptable behavior that must NEVER be violated.
- Examples:
  - *Data Integrity*: "All extracted fields must cite source URLs with timestamps; zero unverified hallucinations."
  - *Safety Boundary*: "No write operations to external production endpoints without explicit human token."
  - *Quality Floor*: "All generated code must compile cleanly and pass static analysis with 0 lint errors."

## 2. Mandatory Human Approval Gate (Phase 2)
- The agent or harness MUST NEVER begin running an automated execution loop without the human's explicit approval of the invariant.
- The harness presents:
  1. Primary Goal
  2. The Proposed Invariant
  3. Stop Conditions (Max Iterations, Budget, Target Score)
  4. Initial Evaluation Rubric
- Execution is strictly BLOCKED until the human signs off via CLI or the Web Dashboard.

## 3. Invariant Breach Handling
- If any worker agent output or evaluation step detects an invariant breach:
  1. The harness IMMEDIATELY transitions to state `INVARIANT_BREACH`.
  2. Iteration execution is halted.
  3. A diagnostic alert is sent to Honcho memory and streamed to the Web Dashboard.
  4. The human is prompted to either modify the invariant or terminate the loop.
