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
