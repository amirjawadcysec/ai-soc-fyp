from agents.base import BaseAgent

MITRE = {
    "brute_force": ["T1110 Brute Force"],
    "port_scan": ["T1046 Network Service Discovery"],
    "web_attack": ["T1190 Exploit Public-Facing Application"],
}


class InvestigationAgent(BaseAgent):
    """Correlates logs, builds attack timeline, maps to MITRE ATT&CK.
    TODO (Track C): give an LLM tools (query_logs, lookup_ip) in a ReAct loop."""
    name = "investigation"

    def process(self, inc):
        e = inc.raw_event
        inc.mitre_techniques = MITRE.get(inc.threat_type, [])
        inc.evidence = [f"{k}={v}" for k, v in e.items()]
        inc.attack_timeline = [
            {"time": e.get("timestamp", "?"), "event": f"{inc.threat_type} from {e.get('src_ip')}"}
        ]
        inc.stage = "investigated"
        inc.log(self.name, f"mapped to {inc.mitre_techniques}")
        return inc
