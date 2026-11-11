"""Common message format passed between all six agents.

One Incident object travels through the pipeline; each agent fills in its own
section and appends to `timeline` and `audit`. See docs/message_schema.json.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import uuid

# The execution agent may ONLY perform actions from this whitelist.
SAFE_ACTIONS = {"monitor_only", "block_ip", "rate_limit", "isolate_host"}
# These need explicit human approval before execution.
HIGH_IMPACT_ACTIONS = {"isolate_host"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Incident:
    raw_event: dict                      # normalized log event from ingestion
    incident_id: str = field(default_factory=lambda: "INC-" + uuid.uuid4().hex[:8])
    created_at: str = field(default_factory=now)
    stage: str = "ingested"              # ingested|monitored|detected|investigated|planned|executed|reported
    is_anomaly: bool = False             # Monitoring Agent
    threat_type: str = "unknown"         # Detection Agent: brute_force|port_scan|web_attack|benign
    severity: str = "low"                # low|medium|high|critical
    confidence: float = 0.0              # 0.0 - 1.0
    evidence: list = field(default_factory=list)       # Investigation Agent
    mitre_techniques: list = field(default_factory=list)
    attack_timeline: list = field(default_factory=list)
    recommended_action: dict = field(default_factory=dict)  # {type,target,requires_approval,reason}
    approval_status: str = "not_required"  # not_required|pending|approved|rejected
    execution_result: dict = field(default_factory=dict)    # Execution Agent
    summary: str = ""                    # Reporting Agent
    audit: list = field(default_factory=list)               # every agent logs here

    def log(self, agent: str, message: str):
        self.audit.append({"time": now(), "agent": agent, "message": message})

    def to_dict(self) -> dict:
        return asdict(self)
