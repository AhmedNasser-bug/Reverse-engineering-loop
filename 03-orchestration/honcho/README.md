# Honcho Memory Persistence Layer

This directory packages [plastic-labs/honcho](https://github.com/plastic-labs/honcho) along with local client bindings for Python and Node.js.

## What Honcho Provides in the Loop
- **Cross-Iteration Memory**: Persists learnings and reverse-engineered success factors across loop iterations without context window overflow.
- **Dialectic Representation**: Maintains a structured model of the user, task requirements, and agent roles.
- **Invariant Knowledge**: Holds the agreed-upon loop invariant and stop conditions.

## File Structure
- `honcho_client.py`: Python client with automatic local JSON/JSONL fallback and optional remote Honcho API connectivity.
- `honcho-client.mjs`: Node.js ESM client.
- `storage/`: Directory where session states and reverse-engineering learnings are persisted locally.
- `mcp/`: Honcho's official MCP server implementation for tool-based memory access.
