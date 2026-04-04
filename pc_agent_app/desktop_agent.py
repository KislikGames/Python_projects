from dataclasses import dataclass

from config import load_settings
from llm import PlannerLLM
from memory import MemoryStore
from policy import PolicyEngine
from tools import DesktopTools


@dataclass
class AgentRun:
    allowed: bool
    policy_reason: str
    plan: str
    result: str
    review: str


class GeneralDesktopAgent:
    def __init__(self, db_path: str = "agent_memory.db"):
        settings = load_settings()
        self.policy = PolicyEngine()
        self.tools = DesktopTools(sandbox_dir=settings.sandbox_dir)
        self.llm = PlannerLLM(api_key=settings.openai_api_key, model=settings.openai_model)
        self.memory = MemoryStore(db_path=db_path)

    def execute(self, task: str, confirmed: bool = False) -> AgentRun:
        decision = self.policy.evaluate(task)
        if not decision.allowed:
            return AgentRun(False, decision.reason, "", f"ERROR: {decision.reason}", "Blocked")
        if decision.needs_confirmation and not confirmed:
            return AgentRun(False, decision.reason, "", "ERROR: Confirmation required", "Awaiting confirmation")

        plan = self.llm.plan(task)
        action_logs = []
        for action in plan.actions[:5]:
            tool_result = self.tools.run_action(action)
            action_logs.append(f"{action} => {tool_result.message}")

        result = "\n".join(action_logs) if action_logs else "No actions generated"
        review = self.llm.review(task, result)
        self.memory.save_run(task=task, plan=plan.thinking, result=result, review=review)
        return AgentRun(True, decision.reason, plan.thinking, result, review)
