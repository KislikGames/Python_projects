import sqlite3
from pathlib import Path


class MemoryStore:
    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    result TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    improvement TEXT NOT NULL,
                    quality_score INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def save_lesson(self, task: str, result: str, summary: str, improvement: str, quality_score: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO lessons(task, result, summary, improvement, quality_score)
                VALUES (?, ?, ?, ?, ?)
                """,
                (task, result, summary, improvement, quality_score),
            )

    def latest_lessons(self, limit: int = 5):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT task, summary, improvement, quality_score, created_at FROM lessons ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return rows
