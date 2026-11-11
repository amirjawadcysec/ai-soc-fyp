"""Optional FastAPI layer: uvicorn api:app --reload
POST /events  -> runs the pipeline.  GET /incidents -> list for the dashboard."""
from fastapi import FastAPI
from orchestrator import run_pipeline

app = FastAPI(title="AI SOC")
INCIDENTS = []


@app.post("/events")
def ingest(event: dict, approve: bool = False):
    inc = run_pipeline(event, approve_high_impact=approve)
    INCIDENTS.append(inc.to_dict())
    return inc.to_dict()


@app.get("/incidents")
def incidents():
    return INCIDENTS
