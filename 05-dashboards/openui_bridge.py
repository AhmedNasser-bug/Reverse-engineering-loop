"""
OpenUI Bridge: Integrates wandb/openui generative UI components
into the Reverse Engineering Loop dashboard.
"""

from typing import Dict, Any

class OpenUIBridge:
    @staticmethod
    def render_iteration_card(iteration: int, score: float, causal_factor: str) -> str:
        """Generates dynamic HTML/Tailwind widget using OpenUI schema."""
        return f"""
<div class="p-4 bg-slate-900 border border-slate-800 rounded-xl shadow-lg">
  <div class="flex items-center justify-between mb-2">
    <span class="text-xs font-bold text-emerald-400">Iteration {iteration} Output</span>
    <span class="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">Score: {score:.3f}</span>
  </div>
  <p class="text-xs text-slate-300"><strong>Reverse Engineered Factor:</strong> {causal_factor}</p>
</div>
"""
