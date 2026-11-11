# Multi-Agent AI SOC (FYP)

## Run the week-1 demo (no installs needed)
    python run_demo.py

## Layout
- agents/    six agents (each has a TODO marking what to replace)
- schemas.py shared Incident message + safe-action whitelist
- orchestrator.py  pipeline runner (later: LangGraph)
- api.py     optional FastAPI endpoints (pip install -r requirements.txt)
- lab/ ml/ dashboard/  Track A / B / C work goes here
- docs/      message_schema.json, slide_outline.md
- reports/   generated incident JSON files

## Who owns what
Track A (lab): lab/, execution agent    Track B (ML): ml/, monitoring + detection agents
Track C (agents/dashboard): orchestrator, investigation + response + reporting, dashboard/
