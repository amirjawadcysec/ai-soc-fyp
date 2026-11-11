from agents.base import BaseAgent


class DetectionAgent(BaseAgent):
    """Classifies threat type and severity.
    TODO (Track B): call trained Random Forest model; return real confidence."""
    name = "detection"

    def process(self, inc):
        e = inc.raw_event
        if e.get("failed_logins", 0) >= 5:
            inc.threat_type, inc.severity, inc.confidence = "brute_force", "high", 0.90
        elif e.get("ports_scanned", 0) >= 20:
            inc.threat_type, inc.severity, inc.confidence = "port_scan", "medium", 0.85
        else:
            inc.threat_type, inc.severity, inc.confidence = "web_attack", "high", 0.80
        inc.stage = "detected"
        inc.log(self.name, f"{inc.threat_type} severity={inc.severity} conf={inc.confidence}")
        return inc
