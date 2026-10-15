# Agent Definitions & Roles: AGENTS.md

## 1. Loop Orchestrator Agent (`agent-orchestrator`)
- **Role**: Coordinates the overall loop lifecycle.
- **Responsibilities**:
  - Validates human invariant approval before execution starts.
  - Hydrates worker context from Honcho memory.
  - Monitors stop conditions (iterations, costs, stagnation).
  - Broadcasts real-time events to the OpenUI web dashboard.

## 2. Worker Agent (`agent-worker`)
- **Role**: Performs strategic high-value tasks, high-volume scraping, or compute-intensive data processing.
- **Tools**: Chrome DevTools MCP, Firecrawl scrape, RTK, Graphify.
- **Constraint**: Must operate within the approved loop invariant.

## 3. Reverse Engineering Agent (`agent-rea`)
- **Role**: Dissects execution traces after each iteration.
- **Responsibilities**:
  - Employs REA methodology to identify *why* the iteration succeeded or failed.
  - Isolates decisive causal variables (e.g. prompt framing, schema pre-validation, retrieval ordering).
  - Formulates candidate rubric updates to permanently capture the insight.

## 4. Evaluation Agent (`agent-eval`)
- **Role**: Impartial judge scoring iteration outputs against `RUBRIC.md`.
- **Responsibilities**:
  - Calculates weighted scores across all active dimensions.
  - Commits rubric amendments proposed by the Reverse Engineering Agent.
  - Queues the next iteration task or signals convergence.