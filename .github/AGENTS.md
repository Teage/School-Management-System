---
description: "Workspace instructions for AI coding agents: preserve existing style and support format-on-save behavior."
---

# Workspace Agent Instructions

- This repository is a small Flask web application with Python backend files, Jinja2 templates, and static JS/CSS assets.
- When editing code, preserve the existing formatting style for Python, HTML, CSS, and JavaScript.
- Prefer minimal, focused changes. Avoid broad reformatting unless the specific change needs it.
- Treat format-on-save as an expected editor workflow: keep edits compatible with existing indentation, line breaks, and syntax so autosave formatting remains stable.
- Do not add or change formatter configuration files, editor settings, or workspace settings unless explicitly requested.
- When a formatting decision is needed, follow the current project style rather than imposing a new formatter across the repository.
- Keep code readable and consistent with the current project style.
