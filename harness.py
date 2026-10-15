#!/usr/bin/env python3
"""
Reverse Engineering Loop: Unified CLI Harness.
Controls the full 5-stage lifecycle of engineered agent loops:
  Stage 0: Setup
  Stage 1: Intent & Alignment Chat
  Stage 2: Loop Invariant Human Approval
  Stage 3: Loop Execution & Reverse Engineering
  Stage 4: Real-Time Web Oversight
"""

import sys
import os
import argparse
import json
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
LOOP_ENG_DIR = PROJECT_ROOT / "02-loop-engineering"
ORCH_DIR = PROJECT_ROOT / "03-orchestration"
DASHBOARD_DIR = PROJECT_ROOT / "05-dashboards"
PROCESSING_DIR = PROJECT_ROOT / "04-processing"

# Dynamic imports
from importlib.machinery import SourceFileLoader

def get_loop_manager():
    mod_path = str(LOOP_ENG_DIR / "loop_manager.py")
    return SourceFileLoader("loop_manager", mod_path).load_module().LoopManager()

def get_honcho_memory(session_id="default-loop-session"):
    mod_path = str(ORCH_DIR / "honcho" / "honcho_client.py")
    return SourceFileLoader("honcho_client", mod_path).load_module().HonchoMemoryManager(session_id)

def cmd_setup(args):
    """Stage 0: Set up template project structure and dependencies."""
    print("\n--- STAGE 0: TEMPLATE SETUP ---")
    storage_dir = ORCH_DIR / "honcho" / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir = PROJECT_ROOT / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    env_file = PROJECT_ROOT / ".env"
    env_example = PROJECT_ROOT / ".env.example"
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text(encoding="utf-8"), encoding="utf-8")
        print("[Setup] Created .env from .env.example")
        
    print("[Setup] Initialized directories: storage/, artifacts/")
    print("[Setup] Template setup complete! Next: Run `python harness.py chat` to agree on goals.")

def cmd_chat(args):
    """Stage 1: Chat with the agent to agree on loop goals, stop conditions, and initial rubric."""
    print("\n--- STAGE 1: INTENT & ALIGNMENT CHAT ---")
    print("Welcome to the Reverse Engineering Loop Setup Chat.")
    print("This conversation will establish your loop goals, stop conditions, and the mandatory loop invariant.\n")

    goal = input("Enter your high-value loop goal (or press Enter for default):\n> ").strip()
    if not goal:
        goal = "Autonomous Reverse Engineering & Synthesis of High-Value Technical Specifications"

    invariant = input("\nEnter the mandatory loop invariant (or press Enter for default):\n> ").strip()
    if not invariant:
        invariant = "All claims must cite empirical execution artifacts; zero ungrounded hallucinations."

    max_iter_str = input("\nEnter maximum iterations ceiling [default: 10]:\n> ").strip()
    max_iter = int(max_iter_str) if max_iter_str.isdigit() else 10

    budget_str = input("\nEnter max budget ceiling in USD [default: 5.00]:\n> ").strip()
    budget = float(budget_str) if budget_str else 5.00

    # Save to Honcho memory
    memory = get_honcho_memory()
    memory.set_loop_agreement(
        goal=goal,
        invariant=invariant,
        stop_conditions={"max_iterations": max_iter, "budget_usd": budget, "target_score": 0.95}
    )

    # Save to LOOP.md
    loop_file = LOOP_ENG_DIR / "LOOP.md"
    loop_md_content = f"""# Loop Engineering Specification: LOOP.md

## 1. Loop Objective & Scope
- **Goal Statement**: {goal}

## 2. Mandatory Loop Invariant (Human Approval Required)
> [!IMPORTANT]
> **INVARIANT**: {invariant}
- **Human Approval Status**: PENDING
- **Approval Signature**: Pending human sign-off in Stage 2

## 3. Stop Conditions
| Condition | Parameter | Threshold / Rule |
| :--- | :--- | :--- |
| **Success Convergence** | `rubric_score` | Score >= 0.95 across all evaluation dimensions in `RUBRIC.md` |
| **Max Iterations** | `max_iterations` | {max_iter} iterations |
| **Cost Budget Ceiling**| `max_budget_usd` | ${budget:.2f} total cost |
| **Stagnation Trap** | `min_delta` | Score delta < 0.02 for 3 consecutive iterations |

## 4. Iteration Phase Mapping
1. Context Hydration (Honcho)
2. Worker Execution
3. Trace Capture
4. Reverse Engineering Success Factors (REA)
5. Rubric Dynamic Evolution
6. Real-Time Telemetry Streaming
"""
    loop_file.write_text(loop_md_content, encoding="utf-8")

    lm = get_loop_manager()
    lm.state["human_approved"] = False
    lm.state["status"] = "AWAITING_INVARIANT_APPROVAL"
    lm.state["max_iterations"] = max_iter
    lm.state["budget_ceiling_usd"] = budget
    lm._save_state()

    print("\n✓ Stage 1 Complete! Goal and invariant saved.")
    print("Stage 2 Ready: To approve the invariant and unlock execution, run:")
    print("  python harness.py approve")
    print("or approve via the web dashboard (`python harness.py serve`).")

def cmd_approve(args):
    """Stage 2: Approve the loop invariant (Human-in-the-loop Gate)."""
    print("\n--- STAGE 2: LOOP INVARIANT HUMAN APPROVAL ---")
    lm = get_loop_manager()
    approver = args.approver or "Human Supervisor (CLI)"
    lm.approve_invariant(approved_by=approver)
    print(f"✓ Invariant verified and signed off. Automated execution unlocked!")
    print("Next step: Run `python harness.py run` to execute iterations.")

def cmd_step(args):
    """Execute a single loop iteration."""
    lm = get_loop_manager()
    res = lm.run_iteration()
    print(json.dumps(res, indent=2))

def cmd_run(args):
    """Stage 3: Run the loop until convergence or stop condition is met."""
    print("\n--- STAGE 3: LOOP EXECUTION & REVERSE ENGINEERING ---")
    lm = get_loop_manager()
    while lm.state["status"] not in ["CONVERGED_SUCCESS", "MAX_ITERATIONS_REACHED", "HALTED"]:
        lm.run_iteration()
        time.sleep(1)
    print(f"\nFinal Status: {lm.state['status']}")
    print(f"Final Rubric Score: {lm.state['latest_rubric_score']:.3f}")

def cmd_status(args):
    """Display active loop telemetry and invariant status."""
    lm = get_loop_manager()
    print(f"\n=== Reverse Engineering Loop Status ===")
    print(f"Status:            {lm.state['status']}")
    print(f"Invariant Health:  {lm.state['invariant_health']}")
    print(f"Human Approved:    {lm.state['human_approved']}")
    print(f"Active Iteration:  {lm.state['current_iteration']} / {lm.state['max_iterations']}")
    print(f"Latest Score:      {lm.state['latest_rubric_score']:.3f} / {lm.state['target_score']:.3f}")
    print(f"Budget Spent:      ${lm.state['cumulative_cost_usd']:.2f} / ${lm.state['budget_ceiling_usd']:.2f}")

def cmd_serve(args):
    """Stage 4: Launch real-time web dashboard."""
    print("\n--- STAGE 4: REAL-TIME WEB DASHBOARD ---")
    port = args.port or 8080
    mod_path = str(DASHBOARD_DIR / "server.py")
    server_mod = SourceFileLoader("server", mod_path).load_module()
    server_mod.run_dashboard_server(port)


def main():
    parser = argparse.ArgumentParser(description="Reverse Engineering Loop CLI Harness")
    subparsers = parser.add_subparsers(dest="subcommand")

    subparsers.add_parser("setup", help="Stage 0: Set up template project")
    subparsers.add_parser("chat", help="Stage 1: Chat to agree on loop goals and invariant")
    
    approve_parser = subparsers.add_parser("approve", help="Stage 2: Approve the loop invariant")
    approve_parser.add_argument("--approver", default="Human Supervisor", help="Signer identity")

    subparsers.add_parser("step", help="Execute single loop iteration")
    subparsers.add_parser("run", help="Stage 3: Run loop to convergence")
    subparsers.add_parser("status", help="Show loop status")

    serve_parser = subparsers.add_parser("serve", help="Stage 4: Launch web dashboard")
    serve_parser.add_argument("--port", type=int, default=8080, help="Web dashboard port")

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "setup": cmd_setup,
        "chat": cmd_chat,
        "approve": cmd_approve,
        "step": cmd_step,
        "run": cmd_run,
        "status": cmd_status,
        "serve": cmd_serve
    }
    cmds[args.subcommand](args)

if __name__ == "__main__":
    main()
