---
name: sino-mena-researcher
description: >-
  Autonomous Sino-MENA researcher that discovers target URLs/papers, scrapes them using stealth bot-mitigated protocols, and compiles findings into strategy indexes and GSuite export payloads.
---

# Sino-MENA Strategy & Research Engine

## Overview
The `sino-mena-researcher` skill is an autonomous research tool. It discovers target competitor URLs and academic paper sources for a given business choice, fetches them using stealth request headers and delay structures to bypass Cloudflare/bot mitigation, and compiles the results into a centralized research database. It also automatically triggers the `agent-annealer` to write self-improving operational rules to the local workspace.

## Dependencies
*   `agent-annealer`: For injecting self-improving prompt adjustments into local rules.
*   `firecrawl-deep-research`: For crawling multi-page domains.
*   `firecrawl-competitive-intel`: For targeting specific competitor pricing/services.
*   `firecrawl-market-research`: For extracting market size (TAM/SAM/SOM) and cost data.
*   `literature-search-arxiv`: For academic backing.

## Quick Start
To launch autonomous research and self-annealing:
```bash
uv run C:/Users/enjoy/.gemini/config/skills/sino-mena-researcher/scripts/sino_mena_researcher.py --query "landing page conversion rate optimization 2026" --workspace .
```

## Utility Scripts

### `scripts/sino_mena_researcher.py`

#### Subcommand: `research`
Discovers targets, scrapes them with stealth requests, compiles results, and triggers the annealer.
*   **Arguments:**
    *   `--query` (Required): Research topic or business choice.
    *   `--workspace` (Required): Target repository workspace to write findings and local rules.
    *   `--output` (Optional): Alternative path for the compiled research index file.

## Workflow

### 1. Autonomous Target Discovery
*   Takes a topic (e.g. "outbound lead enrichment conversion rates").
*   Uses available search engines or search tools to discover 3-5 high-value domains or academic PDF links.

### 2. Stealth Scraping
*   Requests discovered URLs using custom modern browser headers and random sleep delays (1.0 to 3.5 seconds).
*   If blocked, writes the raw response headers and status to a debug log to allow prompt adjustment (no hallucinations or mock data).

### 3. Synthesis & Self-Annealing
*   Saves research copies to `docs/strategy/` and updates the index file.
*   Triggers the `agent-annealer` CLI tool to write self-improving prompt guidelines directly into `.agents/AGENTS.md`.

## Rate Limiting & Stealth
*   Default limit of 1 request per 3 seconds per host.
*   Rotates through a modern User-Agent library.
*   Retries with exponential backoff on HTTP 502/503/504 errors.

## Common Mistakes
*   **Invoking mock data on block:** Always raise a structured error detailing the block rather than returning fake/cached metrics.
*   **Blind crawling:** Always let the script discover targeted URLs first rather than scraping full domains.
