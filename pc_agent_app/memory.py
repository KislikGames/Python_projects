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
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    plan TEXT NOT NULL,
                    result TEXT NOT NULL,
                    review TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def save_run(self, task: str, plan: str, result: str, review: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO runs(task, plan, result, review) VALUES (?, ?, ?, ?)",
                (task, plan, result, review),
            )

    def recent_reviews(self, limit: int = 5) -> list[tuple[str, str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT task, review, created_at FROM runs ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return rows
