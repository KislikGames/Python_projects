import tkinter as tk
from tkinter import ttk

from agent.core import DesktopAgent


class AgentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PC Agent App")
        self.geometry("820x520")

        self.agent = DesktopAgent()
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Задача:").pack(anchor="w")
        self.task_text = tk.Text(frame, height=5)
        self.task_text.pack(fill="x")

        self.confirm_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame,
            text="Подтверждаю рискованные/финансовые действия",
            variable=self.confirm_var,
        ).pack(anchor="w", pady=6)

        ttk.Label(frame, text="Реквизиты для вывода (опционально):").pack(anchor="w")
        self.payout_entry = ttk.Entry(frame)
        self.payout_entry.pack(fill="x", pady=4)

        ttk.Button(frame, text="Запустить агента", command=self._run_agent).pack(anchor="w", pady=8)

        ttk.Label(frame, text="Логи:").pack(anchor="w")
        self.output = tk.Text(frame, height=16)
        self.output.pack(fill="both", expand=True)

    def _run_agent(self):
        task = self.task_text.get("1.0", "end").strip()
        if not task:
            self._append("Введите задачу.\n")
            return

        response = self.agent.run(
            task=task,
            confirmed=self.confirm_var.get(),
            payout_details=self.payout_entry.get().strip() or None,
        )

        self._append(f"Skill: {response.plan_skill}\n")
        self._append(f"Policy: {response.policy_reason}\n")
        self._append(f"Result: {response.result}\n")
        self._append(f"Self-review: {response.review_summary}\n")
        self._append(f"Improve: {response.review_improvement}\n")
        self._append(f"Quality score: {response.quality_score}/5\n")
        self._append("-" * 60 + "\n")

    def _append(self, line: str):
        self.output.insert("end", line)
        self.output.see("end")


if __name__ == "__main__":
    app = AgentApp()
    app.mainloop()
