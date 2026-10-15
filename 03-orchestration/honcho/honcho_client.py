"""
Honcho Memory Persistence Client for Reverse Engineering Loop Harness.
Provides stateful context, dialectic session management, and cross-iteration
knowledge retention using Plastic Labs' Honcho patterns.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path

class HonchoMemoryManager:
    """
    Manages persistent memory across engineered loop iterations.
    Supports local JSONL storage fallback and remote Honcho API backend.
    """

    def __init__(self, session_id: str = "default-loop-session", base_path: Optional[str] = None):
        self.session_id = session_id
        self.api_key = os.getenv("HONCHO_API_KEY")
        self.api_url = os.getenv("HONCHO_API_URL", "https://api.honcho.dev/v1")
        
        # Local persistence directory
        if base_path:
            self.storage_dir = Path(base_path)
        else:
            self.storage_dir = Path(__file__).resolve().parent / "storage"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.session_file = self.storage_dir / f"{self.session_id}_session.json"
        self.learnings_file = self.storage_dir / f"{self.session_id}_learnings.jsonl"
        self.state = self._load_session()

    def _load_session(self) -> Dict[str, Any]:
        """Loads existing session state or initializes a new one."""
        if self.session_file.exists():
            try:
                with open(self.session_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "session_id": self.session_id,
            "created_at": time.time(),
            "updated_at": time.time(),
            "user_profile": {
                "preferred_invariants": [],
                "stop_condition_sensitivity": "strict",
                "budget_ceiling_usd": 10.0
            },
            "loop_goal": None,
            "active_invariant": None,
            "messages": [],
            "learnings": []
        }

    def _save_session(self) -> None:
        """Persists the session state to disk."""
        self.state["updated_at"] = time.time()
        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def set_loop_agreement(self, goal: str, invariant: str, stop_conditions: Dict[str, Any]) -> None:
        """Sets the agreed upon loop goals and invariant from Step 1 & 2."""
        self.state["loop_goal"] = goal
        self.state["active_invariant"] = invariant
        self.state["stop_conditions"] = stop_conditions
        self.add_message("system", f"Loop Goal Agreed: {goal}")
        self.add_message("system", f"Loop Invariant Established: {invariant}")
        self._save_session()

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Adds a conversation message into the persistent dialectic memory."""
        msg = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        self.state["messages"].append(msg)
        self._save_session()

    def record_learning(self, iteration: int, finding: str, causal_factor: str, rubric_delta: Optional[str] = None) -> None:
        """
        Records a reverse-engineered insight explaining why an iteration succeeded or failed.
        """
        entry = {
            "iteration": iteration,
            "finding": finding,
            "causal_factor": causal_factor,
            "rubric_delta": rubric_delta,
            "timestamp": time.time()
        }
        self.state["learnings"].append(entry)
        self._save_session()
        
        # Append to learnings JSONL file
        with open(self.learnings_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def get_learnings(self) -> List[Dict[str, Any]]:
        """Returns all recorded reverse-engineered learnings."""
        return self.state.get("learnings", [])

    def get_context_for_prompt(self, max_messages: int = 10) -> str:
        """
        Constructs a concise, high-signal memory context string for prompt injection.
        """
        lines = []
        if self.state.get("loop_goal"):
            lines.append(f"### CURRENT LOOP GOAL:\n{self.state['loop_goal']}\n")
        if self.state.get("active_invariant"):
            lines.append(f"### MANDATORY LOOP INVARIANT:\n{self.state['active_invariant']}\n")
        
        learnings = self.get_learnings()
        if learnings:
            lines.append("### REVERSE-ENGINEERED SUCCESS FACTORS (PREVIOUS ITERATIONS):")
            for item in learnings[-5:]:
                lines.append(f"- [Iter {item['iteration']}] {item['finding']} (Cause: {item['causal_factor']})")
            lines.append("")

        recent_msgs = self.state.get("messages", [])[-max_messages:]
        if recent_msgs:
            lines.append("### RECENT DIALECTIC HISTORY:")
            for m in recent_msgs:
                lines.append(f"{m['role'].upper()}: {m['content']}")
                
        return "\n".join(lines)


if __name__ == "__main__":
    memory = HonchoMemoryManager("test-session")
    memory.set_loop_agreement(
        goal="Extract, reverse-engineer, and synthesize strategic technical competitor docs",
        invariant="Never hallucinate undocumented API endpoints; all claims must cite execution trace",
        stop_conditions={"max_iterations": 5, "min_score": 0.95}
    )
    memory.record_learning(
        iteration=1,
        finding="Direct DOM parsing missed shadow DOM elements; switching to DevTools accessibility tree caught all nodes",
        causal_factor="Accessibility tree traversal captures dynamic client-side hydration"
    )
    print("Memory Context:")
    print(memory.get_context_for_prompt())
