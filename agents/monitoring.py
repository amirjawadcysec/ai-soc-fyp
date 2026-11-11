from agents.base import BaseAgent


class MonitoringAgent(BaseAgent):
    """Reads normalized logs, filters noise, raises anomaly alerts.
    TODO (Track B): replace the rule with Isolation Forest / autoencoder score."""
    name = "monitoring"

    def process(self, inc):
        e = inc.raw_event
        suspicious = (
            e.get("failed_logins", 0) >= 5
            or e.get("ports_scanned", 0) >= 20
            or any(k in e.get("request", "").lower() for k in ("' or 1=1", "<script", "../"))
        )
        inc.is_anomaly = suspicious
        inc.stage = "monitored"
        inc.log(self.name, "anomaly raised" if suspicious else "benign, dropped as noise")
        return inc
