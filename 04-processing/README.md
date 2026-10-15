# 04 - Processing & Evaluation Layer

This module provides the worker pipelines, priority task queues, and evaluation agents that execute the engineered loop.

## Core Components
- `task_queue.py`: Priority heap queue supporting concurrent worker execution, rate limiting, and task status tracking for strategic and high-volume workloads.
- `eval_agent.py`: The Evaluation Agent that:
  1. Scores iteration outputs against `RUBRIC.md`.
  2. Dispatches REA reverse engineering to discover why the iteration succeeded.
  3. Updates the evaluation rubric with new criteria.
  4. Dynamically updates the evaluation agent's own prompts.
  5. Records learnings in Honcho persistent memory and queues subsequent evaluation tasks.
- `reverse_engineering_analyzer.py`: Trace and artifact comparison engine.
- `batch_processor.py`: High-throughput pipeline for batch web scraping and compute tasks.
- `metrics.py`: Telemetry calculations for token cost, convergence velocity, and invariant stability.
