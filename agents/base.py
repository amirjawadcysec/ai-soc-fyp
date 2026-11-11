from schemas import Incident


class BaseAgent:
    name = "base"

    def process(self, incident: Incident) -> Incident:
        raise NotImplementedError
