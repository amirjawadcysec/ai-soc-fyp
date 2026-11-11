"""Runs the six agents in order. Plain Python for now so it works anywhere.
Later: re-implement as a LangGraph StateGraph (same agents, nodes + edges)."""
from schemas import Incident
from agents.monitoring import MonitoringAgent
from agents.detection import DetectionAgent
from agents.investigation import InvestigationAgent
from agents.response import ResponseAgent
from agents.execution import ExecutionAgent
from agents.reporting import ReportingAgent

PIPELINE = [MonitoringAgent(), DetectionAgent(), InvestigationAgent(),
            ResponseAgent(), ExecutionAgent(), ReportingAgent()]


def run_pipeline(raw_event: dict, approve_high_impact: bool = False) -> Incident:
    inc = Incident(raw_event=raw_event)
    for agent in PIPELINE:
        inc = agent.process(inc)
        if agent.name == "monitoring" and not inc.is_anomaly:
            return inc                      # noise filtered out, stop here
        if agent.name == "response" and approve_high_impact and inc.approval_status == "pending":
            inc.approval_status = "approved"   # simulates the human clicking Approve
            inc.log("human", "approved high-impact action")
    return inc
