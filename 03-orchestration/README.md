# 03 - Orchestration Layer

The Orchestration Layer is the brain and nerve center of the Reverse Engineering Loop Harness. It packages:
1. **Honcho Memory Persistence** (`honcho/`): Stateful cross-iteration memory based on [plastic-labs/honcho](https://github.com/plastic-labs/honcho).
2. **Packaged Skills** (`skills/`): Modular capabilities including REA, Loop Engineering, OpenUI, Graphify, RTK, Web Scraping, Deep Research, and Engineering Best Practices.
3. **MCP Configurations** (`mcp/`): Preconfigured Model Context Protocol servers for Sequential Thinking, Chrome DevTools, GitHub, and Context7.
4. **Orchestration Rules** (`rules/`): Enforced operational directives for loop invariant sign-off, reverse engineering post-runs, and memory hygiene.
5. **Orchestrator Engine** (`orchestrator.py`): Dynamic assembler that binds memory, skills, and rules into targeted agent prompts.

## Key Subdirectories
- `honcho/`: Python and Node client bindings + storage directory for persistent sessions.
- `skills/`: Complete collection of packaged skills.
- `mcp/`: Consolidated MCP configuration (`mcp-config.json`) and schema files.
- `rules/`: Governance rules for loop invariants and self-improvement.
