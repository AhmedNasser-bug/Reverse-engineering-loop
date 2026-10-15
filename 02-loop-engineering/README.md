# 02 - Loop Engineering Layer

This module packages the core patterns, starters, and governance tools from [cobusgreyling/loop-engineering](https://github.com/cobusgreyling/loop-engineering) adapted for the Reverse Engineering Loop Harness.

## Core Files & Artifacts
- `LOOP.md`: Active loop contract detailing the goal, human-approved invariant, stop conditions, and iteration phase mapping.
- `STATE.md`: Real-time markdown telemetry file updated after every iteration.
- `RUBRIC.md`: Dynamic evaluation rubric that anneals and adds criteria through post-iteration reverse engineering.
- `AGENTS.md`: Role definitions and operational boundaries for Orchestrator, Worker, REA Reverse Engineer, and Evaluation Agent.
- `loop_manager.py`: Python CLI and programmatic controller for running, stepping, approving, and auditing loops.
- `patterns/`, `starters/`, `tools/`: Vendored loop engineering tools (`loop-audit`, `loop-init`, `loop-cost`).

## CLI Usage
```bash
# Check loop state
python 02-loop-engineering/loop_manager.py status

# Approve the loop invariant (Human-in-the-loop Phase 2)
python 02-loop-engineering/loop_manager.py approve

# Execute a single iteration
python 02-loop-engineering/loop_manager.py step

# Run until convergence or stop condition
python 02-loop-engineering/loop_manager.py run
```
