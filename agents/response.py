from agents.base import BaseAgent
from schemas import HIGH_IMPACT_ACTIONS


class ResponseAgent(BaseAgent):
    """Chooses the defensive action. High-impact actions need human approval.
    TODO (Track C): let the LLM propose, but validate against SAFE_ACTIONS."""
    name = "response"

    def process(self, inc):
        src = inc.raw_event.get("src_ip")
        action = {"brute_force": "block_ip", "port_scan": "rate_limit",
                  "web_attack": "isolate_host"}.get(inc.threat_type, "monitor_only")
        target = inc.raw_event.get("dst_host") if action == "isolate_host" else src
        needs = action in HIGH_IMPACT_ACTIONS
        inc.recommended_action = {"type": action, "target": target,
                                  "requires_approval": needs,
                                  "reason": f"{inc.threat_type} ({inc.severity})"}
        inc.approval_status = "pending" if needs else "not_required"
        inc.stage = "planned"
        inc.log(self.name, f"proposed {action} on {target}, approval={inc.approval_status}")
        return inc
