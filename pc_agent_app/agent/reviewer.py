from dataclasses import dataclass


@dataclass
class Review:
    success: bool
    quality_score: int
    summary: str
    improvement: str


class Reviewer:
    def review(self, task: str, result: str) -> Review:
        success = "ERROR" not in result
        quality_score = 4 if success else 2
        improvement = (
            "Try reducing unnecessary browser steps and ask clarifying questions earlier."
            if success
            else "Add better error handling and fallback strategy."
        )
        summary = f"Task: {task[:80]} | Success: {success}"
        return Review(success=success, quality_score=quality_score, summary=summary, improvement=improvement)
