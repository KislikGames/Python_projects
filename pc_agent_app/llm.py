import json
from dataclasses import dataclass


@dataclass
class PlanOutput:
    thinking: str
    actions: list[str]


class PlannerLLM:
    def __init__(self, api_key: str | None, model: str):
        self.api_key = api_key
        self.model = model

    def plan(self, task: str) -> PlanOutput:
        if not self.api_key:
            return self._fallback(task)

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            prompt = (
                "You are a desktop automation planner. "
                "Return strict JSON with fields: thinking (string), actions (array of JSON strings). "
                "Each action JSON must use one of tools: create_text_file, open_url. "
                "Task: " + task
            )
            response = client.responses.create(model=self.model, input=prompt)
            text = response.output_text
            data = json.loads(text)
            actions = data.get("actions", [])
            actions = [a for a in actions if isinstance(a, str)]
            return PlanOutput(thinking=data.get("thinking", ""), actions=actions)
        except Exception:
            return self._fallback(task)

    def review(self, task: str, result: str) -> str:
        if not self.api_key:
            return self._fallback_review(result)

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            prompt = (
                "Evaluate the run briefly in 3 bullets: success, what to improve, next experiment. "
                f"Task: {task}\nResult: {result}"
            )
            response = client.responses.create(model=self.model, input=prompt)
            return response.output_text.strip()
        except Exception:
            return self._fallback_review(result)

    def _fallback(self, task: str) -> PlanOutput:
        lowered = task.lower()
        if "файл" in lowered or "text file" in lowered:
            return PlanOutput(
                thinking="Detected file creation intent.",
                actions=[
                    json.dumps(
                        {
                            "tool": "create_text_file",
                            "path": "~/Desktop/agent_created.txt",
                            "content": "Файл создан универсальным агентом.",
                        },
                        ensure_ascii=False,
                    )
                ],
            )
        if "wordle" in lowered:
            return PlanOutput(
                thinking="Detected browser game task.",
                actions=[json.dumps({"tool": "open_url", "url": "https://www.nytimes.com/games/wordle/index.html"})],
            )
        return PlanOutput(
            thinking="Fallback planning.",
            actions=[json.dumps({"tool": "open_url", "url": "https://www.google.com"})],
        )

    def _fallback_review(self, result: str) -> str:
        ok = "Failed" not in result and "ERROR" not in result
        if ok:
            return "- Success: yes\n- Improve: reduce unnecessary steps\n- Next experiment: add one more validation"
        return "- Success: partial/no\n- Improve: add better fallback\n- Next experiment: retry with clarification"
