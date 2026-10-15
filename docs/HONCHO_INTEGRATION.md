# Honcho Memory Integration Guide

## 1. Context Retention Across Loops
Standard LLM workflows suffer from memory amnesia: each iteration starts with a blank context or attempts to shove raw historical transcripts into the prompt, resulting in token limits, high costs, and attention dilution.

By integrating [plastic-labs/honcho](https://github.com/plastic-labs/honcho), this template provides:
- **Dialectic Representation**: Represents user preferences, quality standards, and feedback in a persistent model.
- **Salient Extraction**: Stores reverse-engineered learnings and invariant discoveries in structured JSONL records rather than raw token dumps.
- **Cross-Session Resilience**: When the harness reboots, the entire loop state, past iterations, and learned invariants are instantly reloaded.

---

## 2. Directory Layout
```
03-orchestration/honcho/
├── honcho_client.py       # Python memory manager with local fallback
├── honcho-client.mjs      # Node.js ESM client
├── storage/               # Local JSON / JSONL state persistence directory
│   ├── <session>_session.json
│   └── <session>_learnings.jsonl
└── mcp/                   # Official Honcho MCP server
```

## 3. Configuration
Set environment variables in `.env`:
```ini
HONCHO_API_KEY=your_honcho_api_key_or_leave_empty_for_local_fallback
HONCHO_API_URL=https://api.honcho.dev/v1
```
*Note: If no API key is provided, the client seamlessly defaults to local filesystem persistence in `storage/`.*
