# How to Use and Adapt This Template

This project is a modular harness template for building self-correcting agent loops. It is optimized for:
- **Strategic High-Value Tasks**: In-depth competitive analysis, software architecture reverse engineering, algorithmic discovery, autonomous technical due diligence.
- **High-Volume Automation**: Bulk web scraping, structured data extraction across thousands of endpoints, multi-source knowledge synthesis.
- **Processing-Intensive Workflows**: Complex data pipelines, batch LLM evaluations, multimodal deconstruction.

---

## 1. Adapting the Template for Your Use Case

### Step 1: Customize the Initial Rubric (`02-loop-engineering/RUBRIC.md`)
Edit the scoring dimensions and weights to reflect your domain-specific criteria:
```markdown
| Dimension ID | Dimension Name | Weight | Pass Threshold | Description |
| :--- | :--- | :---: | :---: | :--- |
| `DIM_ACCURACY` | Domain Accuracy | 35% | >= 0.95 | No hallucinations, mathematically verified |
| `DIM_SCHEMA` | Schema Conformity | 25% | 1.00 | Strict JSON contract adherence |
```

### Step 2: Define Custom Worker Tasks (`04-processing/`)
Create your task handler in `04-processing/batch_processor.py` or enqueue items into `04-processing/task_queue.py`:
```python
from processing.task_queue import ProcessingTaskQueue, TaskPriority

queue = ProcessingTaskQueue()
queue.enqueue(
    task_type="ANALYZE_TARGET_SPEC",
    payload={"target_url": "https://api.example.com/v2/docs"},
    priority=TaskPriority.HIGH
)
```

### Step 3: Configure Persistent Memory Sessions (`03-orchestration/honcho/`)
Set your session identifier in `03-orchestration/honcho/honcho_client.py`:
```python
memory = HonchoMemoryManager(session_id="enterprise-audit-loop")
```

### Step 4: Add Domain-Specific Skills (`03-orchestration/skills/`)
Add custom skills with a `SKILL.md` to `03-orchestration/skills/<skill-name>/SKILL.md`. The orchestrator will automatically load them and expose them to worker agents.

---

## 2. Running the Harness

```bash
# 1. Start the real-time web dashboard
python harness.py serve --port 8080

# 2. Approve the loop invariant (via Web UI or CLI)
python harness.py approve

# 3. Execute the loop to convergence
python harness.py run
```
