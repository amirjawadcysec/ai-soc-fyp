import json, os
from agents.base import BaseAgent


class ReportingAgent(BaseAgent):
    """Writes the incident summary for the dashboard (saved to reports/).
    TODO: use an LLM to write the human-readable explanation."""
    name = "reporting"

    def process(self, inc):
        inc.summary = (f"{inc.threat_type} from {inc.raw_event.get('src_ip')} "
                       f"(severity {inc.severity}, MITRE {', '.join(inc.mitre_techniques)}). "
                       f"Action: {inc.recommended_action.get('type')} -> "
                       f"{inc.execution_result.get('status')}.")
        inc.stage = "reported"
        inc.log(self.name, "report written")
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{inc.incident_id}.json", "w") as f:
            json.dump(inc.to_dict(), f, indent=2)
        return inc
