from dataclasses import dataclass


@dataclass
class PolicyDecision:
    allowed: bool
    needs_confirmation: bool
    reason: str


class PolicyEngine:
    BLOCKED = ("взлом", "steal", "malware", "ddos")
    HIGH_RISK = ("перевод", "карта", "банков", "деньги", "payment", "transfer")

    def evaluate(self, task: str) -> PolicyDecision:
        lowered = task.lower()
        if any(word in lowered for word in self.BLOCKED):
            return PolicyDecision(False, False, "Task is blocked by safety policy")
        if any(word in lowered for word in self.HIGH_RISK):
            return PolicyDecision(True, True, "Financial/high-risk action needs explicit confirmation")
        return PolicyDecision(True, False, "Task is allowed")
