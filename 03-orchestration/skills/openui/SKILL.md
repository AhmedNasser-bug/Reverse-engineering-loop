---
name: openui
description: Generate, render, and stream interactive UI components using OpenUI. Enables real-time visual inspection of loop iterations, metric cards, human approval dialogs, and dynamic dashboards.
---

# OpenUI: Real-Time Generative UI Integration

## Overview
The `openui` skill enables AI agents inside the harness to produce dynamic, reactive UI components on the fly using W&B OpenUI. These components are streamed directly into the web dashboard (`05-dashboards`) to provide live, human-in-the-loop oversight.

## Use Cases
1. **Interactive Invariant Approval**: Render interactive approval cards where the user can toggle constraints, set budgets, and click "Approve Invariant".
2. **Real-Time Iteration Monitoring**: Display live telemetry, timeline steps, tool call logs, and convergence graphs.
3. **Hypothesis & Rubric Visualizer**: Render before/after diffs of the evaluation rubric as it evolves through reverse engineering.
4. **Custom Task Dashboards**: Generate tailored data visualizations, tables, and inspection forms for processing-intensive results.

## Syntax & Component Generation
OpenUI converts prompt descriptions or structured specifications into HTML/React/Tailwind components:

```html
<div class="p-6 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-bold text-emerald-400">Loop Invariant Approved</h3>
    <span class="px-2.5 py-1 text-xs font-semibold bg-emerald-500/20 text-emerald-300 rounded-full border border-emerald-500/30">Active</span>
  </div>
  <p class="text-sm text-slate-300 mb-4">Verification constraints validated across all worker agents.</p>
  <div class="grid grid-cols-3 gap-3 text-center">
    <div class="bg-slate-800/60 p-3 rounded-lg border border-slate-700/50">
      <div class="text-xs text-slate-400">Iteration</div>
      <div class="text-xl font-bold text-white">4 / 10</div>
    </div>
    <div class="bg-slate-800/60 p-3 rounded-lg border border-slate-700/50">
      <div class="text-xs text-slate-400">Score</div>
      <div class="text-xl font-bold text-cyan-400">0.942</div>
    </div>
    <div class="bg-slate-800/60 p-3 rounded-lg border border-slate-700/50">
      <div class="text-xs text-slate-400">Budget Spent</div>
      <div class="text-xl font-bold text-amber-400">$0.84</div>
    </div>
  </div>
</div>
```

## Dashboard Stream
Components generated with OpenUI are broadcast to clients connected to `/api/loop/events` on the dashboard server.
