from agents.base import BaseAgent
from schemas import SAFE_ACTIONS


class ExecutionAgent(BaseAgent):
    """Performs approved actions in the LAB ONLY. Whitelist enforced.
    TODO (Track A): replace print with real iptables / ssh command on lab VM."""
    name = "execution"

    def process(self, inc):
        a = inc.recommended_action
        if a.get("type") not in SAFE_ACTIONS:
            inc.execution_result = {"status": "refused", "reason": "action not whitelisted"}
        elif inc.approval_status == "pending":
            inc.execution_result = {"status": "waiting_for_human_approval"}
        elif inc.approval_status == "rejected":
            inc.execution_result = {"status": "skipped_rejected"}
        else:
            # Simulated command. Real version: e.g. `iptables -A INPUT -s <ip> -j DROP` on lab VM.
            inc.execution_result = {"status": "success", "command": f"SIMULATED {a['type']} {a['target']}"}
        inc.stage = "executed"
        inc.log(self.name, str(inc.execution_result))
        return inc
