# 01 - REA (Reverse Engineer Anything with Agents)

This module packages [morluto/rea](https://github.com/morluto/rea) integrated directly into the loop harness.

## Purpose in the Harness
1. **Understand Why It Succeeded**: When an iteration passes, REA analyzes the execution artifacts, tool outputs, and prompt variations to isolate the decisive causal factor that produced success.
2. **Synthesize Invariants**: Discovered mechanics are converted into explicit invariants.
3. **Evolve the Evaluation Rubric**: Feeds new dimensions and stricter quality gates into `02-loop-engineering/RUBRIC.md`.
4. **Hydrate Honcho Memory**: Logs findings into Honcho so subsequent worker iterations operate with compounded intelligence.

## Scripts
- `rea_harness.py`: General bridge to dispatch REA against target binaries, apps, or execution traces.
- `rea_reverse_engineer.py`: Specialized post-iteration analyzer that updates the evaluation rubric and evaluation agent.
- `rea.config.json`: Configuration settings.
- `src/`, `bridge/`, `native/`: Vendored core REA engine components.
