\# Pipeline: Análisis LatAm 2025



\## Project

Repeatable financial wellness analysis pipeline for Futuro Digital LatAm.

Dataset: data/latam\_finanzas\_2025.csv (raw) → data/latam\_finanzas\_clean.csv (clean)

Report: analysis-report.md



\## Python Environment

venv activated. Libraries: pandas, matplotlib, seaborn, scipy.

Scripts go in scripts/. Charts go in charts/ as PNGs.



\## Naming Conventions

Scripts: 01\_explore.py, 02\_clean.py, 03\_analyse.py, 04\_visualise.py

Charts: 01\_income\_by\_country.png through 05\_housing\_burden\_by\_country.png

Country scripts: country\_Mexico.py, country\_Colombia.py, etc.



\## Notion Workspace

Integration: LatAm Pipeline

Databases: "Findings Tracker", "Country Profiles"

Report page: "Informe Ejecutivo"

Push each finding after Phase 3 analysis. Push report after Phase 6.



\## Pipeline Components

Hooks: chart counter, script logger, phase validator (configured in .claude/settings.json)

MCP: notion (configured in .mcp.json, not settings.json — Claude Code reads project-scoped MCP servers from .mcp.json)

Skills: /interpret (finding format), /publish-finding (Notion push)

Agent: country-profiler (parallel country analysis)

