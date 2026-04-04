from dataclasses import dataclass


@dataclass
class Plan:
    skill: str
    rationale: str


class Planner:
    def build_plan(self, task: str) -> Plan:
        lowered = task.lower()
        if "wordle" in lowered:
            return Plan(skill="solve_wordle", rationale="Detected Wordle-related task")
        if "100" in lowered and ("руб" in lowered or "rubl" in lowered or "money" in lowered):
            return Plan(skill="earn_100_rub", rationale="Detected small earning task")
        return Plan(skill="generic_assistant", rationale="Fallback generic workflow")
