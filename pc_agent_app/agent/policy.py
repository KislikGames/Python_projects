from dataclasses import dataclass


@dataclass
class PolicyDecision:
    allowed: bool
    requires_confirmation: bool
    reason: str


class PolicyEngine:
    RISKY_KEYWORDS = (
        "перевод",
        "карта",
        "карту",
        "переведи",
        "bank",
        "card",
        "money transfer",
        "payment",
    )

    def evaluate(self, task: str) -> PolicyDecision:
        lowered = task.lower()
        if any(word in lowered for word in self.RISKY_KEYWORDS):
            return PolicyDecision(
                allowed=True,
                requires_confirmation=True,
                reason="Financial/risky action requires explicit user confirmation",
            )
        return PolicyDecision(allowed=True, requires_confirmation=False, reason="Task is allowed")
