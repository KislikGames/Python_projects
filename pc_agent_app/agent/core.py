from dataclasses import dataclass

from agent.memory import MemoryStore
from agent.planner import Planner
from agent.policy import PolicyEngine
from agent.reviewer import Reviewer
from skills.microtask_skill import run_earn_task
from skills.wordle_skill import run_wordle_task


@dataclass
class AgentResponse:
    plan_skill: str
    policy_reason: str
    result: str
    review_summary: str
    review_improvement: str
    quality_score: int


class DesktopAgent:
    def __init__(self, memory_path: str = "agent_memory.db"):
        self.planner = Planner()
        self.policy = PolicyEngine()
        self.reviewer = Reviewer()
        self.memory = MemoryStore(memory_path)

    def run(self, task: str, confirmed: bool = False, payout_details: str | None = None) -> AgentResponse:
        plan = self.planner.build_plan(task)
        decision = self.policy.evaluate(task)

        if not decision.allowed:
            result = f"ERROR: Blocked by policy: {decision.reason}"
        elif decision.requires_confirmation and not confirmed:
            result = "ERROR: Confirmation required before risky/financial actions."
        else:
            result = self._execute(plan.skill, payout_details)

        review = self.reviewer.review(task, result)
        self.memory.save_lesson(
            task=task,
            result=result,
            summary=review.summary,
            improvement=review.improvement,
            quality_score=review.quality_score,
        )

        return AgentResponse(
            plan_skill=plan.skill,
            policy_reason=decision.reason,
            result=result,
            review_summary=review.summary,
            review_improvement=review.improvement,
            quality_score=review.quality_score,
        )

    def _execute(self, skill: str, payout_details: str | None) -> str:
        if skill == "solve_wordle":
            return run_wordle_task()
        if skill == "earn_100_rub":
            return run_earn_task(target_amount_rub=100, payout_details=payout_details)
        return "Generic assistant mode: task parsed, but no specific skill registered yet."
