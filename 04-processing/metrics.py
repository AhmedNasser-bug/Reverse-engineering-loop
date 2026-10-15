"""
Telemetry & Metrics Engine for Reverse Engineering Loop.
Tracks cost accumulation, token efficiency, convergence rate, and invariant stability.
"""

from typing import Dict, Any

class LoopMetrics:
    @staticmethod
    def calculate_token_cost(prompt_tokens: int, completion_tokens: int, model: str = "gpt-4o") -> float:
        """Calculates USD cost based on token counts."""
        # Standard benchmark rates per 1M tokens
        pricing = {
            "gpt-4o": {"prompt": 5.0, "completion": 15.0},
            "claude-3-5-sonnet": {"prompt": 3.0, "completion": 15.0},
            "gemini-1-5-pro": {"prompt": 3.5, "completion": 10.5}
        }
        rates = pricing.get(model, {"prompt": 3.0, "completion": 15.0})
        cost = (prompt_tokens / 1_000_000 * rates["prompt"]) + (completion_tokens / 1_000_000 * rates["completion"])
        return round(cost, 4)

    @staticmethod
    def calculate_convergence_velocity(scores: list) -> float:
        """Calculates velocity of score improvement per iteration."""
        if len(scores) < 2:
            return 0.0
        deltas = [scores[i] - scores[i - 1] for i in range(1, len(scores))]
        return round(sum(deltas) / len(deltas), 4)
