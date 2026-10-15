# Reverse Engineering Loop

A modular agentic harness template for engineering self-correcting loops for AI agents, suitable for strategic high-value tasks, high-volume automation, and compute-intensive workloads.

---

## Use Cases
- **Strategic High-Value Tasks**: In-depth competitive analysis, architectural due diligence, and autonomous system research.
- **High-Volume Automation**: Multi-source web scraping, large-scale data extraction, and structured knowledge synthesis.
- **Processing-Intensive Tasks**: Iterative code generation, multi-stage data pipelines, and reverse-engineering execution traces.

---

## Project Structure
```
Reverse-engineering-loop/
├── 01-rea/               # Reverse engineer anything (morluto/rea integration & causal analysis)
├── 02-loop-engineering/  # Loop governance (LOOP.md, STATE.md, RUBRIC.md, loop_manager.py)
├── 03-orchestration/     # Honcho memory persistence, packaged skills, MCP configs & rules
├── 04-processing/        # Priority task queue, batch workers, and Evaluation Agent
├── 05-dashboards/        # Real-time web harness server & OpenUI generative components
├── docs/                 # Detailed guides (User Flow, Template Guide, Architecture)
└── harness.py            # Unified CLI entrypoint
```

---

## How It Works

The harness orchestrates self-improving agent loops by coupling invariant governance, stateful memory, and causal reverse engineering:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        03 - ORCHESTRATION                              │
│   Honcho Stateful Memory  •  Packaged Skills  •  MCP Tools  •  Rules   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Hydrates Context & Invariant
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        02 - LOOP ENGINEERING                           │
│   Human Approval Gate ──> Invariant Verification ──> Iteration Control │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Dispatches Tasks
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        04 - PROCESSING                                 │
│   Priority Task Queue ──> Worker Agents (Web Scraping / Code / RTK)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Outputs Artifacts & Traces
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        01 - REA REVERSE ENGINEERING                    │
│   Deconstructs Traces ──> Discovers "Why Did It Succeed?"             │
│   Updates RUBRIC.md   ──> Evolves Eval Agent ──> Records in Honcho     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Streams Telemetry & Events
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        05 - DASHBOARDS                                 │
│   OpenUI Real-Time Widgets • Live Convergence Graph • Web Oversight    │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Stateful Context Hydration**: At the start of each iteration, worker agents hydrate their prompt context from **Honcho**, retrieving prior iteration learnings, user dialectic profile, and the active loop invariant without token window bloat.
2. **Loop Invariant Enforcement**: The loop manager enforces a formal invariant (agreed upon and signed off by the human in Stage 2). Stop conditions continuously check for target convergence, iteration limits, cost ceilings, and stagnation traps.
3. **Multi-Tool Worker Execution**: Workers draw from the priority task queue, utilizing targeted tools (RTK for surgical token retrieval, Graphify for architecture diagrams, Firecrawl for scraping, and Chrome DevTools for browser automation).
4. **Post-Iteration Reverse Engineering**: Instead of simply marking an iteration as "passed", the **REA engine** analyzes execution traces to identify the exact causal factor behind success (e.g., specific schema constraints, prompt reframing, or tool ordering).
5. **Dynamic Rubric Annealing**: The **Evaluation Agent** translates discovered success factors into new weighted criteria in `RUBRIC.md`, updates its own system prompt, records findings into Honcho memory, and queues the next iteration's evaluation task.
6. **Real-Time Generative Dashboard**: The loop streams telemetry, rubric revisions, and dynamic UI cards generated with **OpenUI** to the web dashboard (`http://localhost:8080`) via Server-Sent Events.

---

### Included Tools & Technologies

| Tool / Repository | Role in Harness | Integration Path |
| :--- | :--- | :--- |
| **[REA](https://github.com/morluto/rea)** | Reverse engineers execution traces, binaries, and APIs to isolate causal success factors | `01-rea/` |
| **[Loop Engineering](https://github.com/cobusgreyling/loop-engineering)** | Loop governance patterns, invariant verification, budget ceilings, and `loop-audit`/`loop-cost` tools | `02-loop-engineering/` |
| **[Honcho](https://github.com/plastic-labs/honcho)** | Stateful dialectic memory library maintaining cross-iteration context and persistent learnings | `03-orchestration/honcho/` |
| **[OpenUI](https://github.com/wandb/openui)** | Generative UI engine producing live interactive dashboard widgets and approval dialogs | `05-dashboards/openui/` |
| **RTK (Rust Token Killer)** | Token-conservation skill replacing expensive full-file reads with surgical queries | `03-orchestration/skills/rtk/` |
| **Graphify** | Architecture visualization engine generating Mermaid topology diagrams | `03-orchestration/skills/graphify/` |
| **Firecrawl & Web Scraping** | High-throughput web scraping, deep research, and crawling skills | `03-orchestration/skills/firecrawl-scrape/` |
| **Chrome DevTools MCP** | Browser automation, DOM inspection, network interception, and trace capture | `03-orchestration/mcp/chrome-devtools/` |
| **Sequential Thinking MCP** | Structured hypothesis generation and falsification reasoning for REA | `03-orchestration/mcp/sequential-thinking/` |
| **GitHub MCP Server** | Repository tracking, commit management, and remote inspection | `03-orchestration/mcp/github-mcp-server/` |
| **Context7 MCP** | Knowledge base indexing and technical documentation lookup | `03-orchestration/mcp/context7/` |


---

## User Flow
1. **0. Setup**: User sets up the template project and hydrates environment variables.
2. **1. Agreement Chat**: User chats with the agent to agree on loop goals, stop conditions, and initial evaluation rubric.
3. **2. Invariant Approval**: Harness compiles orchestration rules and the mandatory **Loop Invariant**. The human user explicitly reviews and approves the invariant before execution unlocks.
4. **3. Execution & Reverse Engineering**:
   - Loop runs using worker agents, REA, web scraping, and research tools.
   - REA reverse engineers **why exactly the iteration succeeded**.
   - Evaluation Agent updates the evaluation rubric and its own prompt.
   - The updated output and next evaluation task are queued.
5. **4. Real-Time Web Oversight**: Human interacts with the harness via the web dashboard (`http://localhost:8080`), inspecting real-time progress, dynamic OpenUI widgets, and rubric evolution.

---

## How to Setup

### 1. Clone & Install
```bash
git clone https://github.com/AhmedNasser-bug/Reverse-engineering-loop.git
cd Reverse-engineering-loop
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure Loop (Stage 1)
```bash
python harness.py chat
```

### 3. Approve Invariant (Stage 2)
```bash
python harness.py approve
```

### 4. Run Loop or Launch Dashboard (Stage 3 & 4)
```bash
# Run loop to convergence
python harness.py run

# Or launch real-time web dashboard
python harness.py serve --port 8080
```
Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser.
