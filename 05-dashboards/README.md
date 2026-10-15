# 05 - Dashboards & OpenUI Integration Layer

This module provides the real-time web interface and OpenUI generative component rendering for human-in-the-loop interaction.

## Features
- **Real-Time Web Dashboard**: Built-in HTTP server (`server.py`) serving a modern Tailwind CSS dashboard with zero external dependencies.
- **Stage 2 Invariant Sign-Off**: Interactive approval gate allowing human supervisors to review, adjust, and approve loop invariants before automated execution begins.
- **Live Progress & REA Stream**: Displays iteration timelines, live evaluation rubric scores, and reverse engineering causal factor dissections.
- **OpenUI Integration** (`openui/`): Packaged [wandb/openui](https://github.com/wandb/openui) repository and `openui_bridge.py` for rendering reactive components dynamically.

## Quickstart
```bash
# Launch the dashboard server
python 05-dashboards/server.py 8080

# Open in browser
# http://127.0.0.1:8080
```
