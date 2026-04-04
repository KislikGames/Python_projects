import tkinter as tk
from tkinter import ttk

from desktop_agent import GeneralDesktopAgent


class AgentWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("General Desktop Agent")
        self.geometry("900x600")
        self.agent = GeneralDesktopAgent()
        self._build_ui()

    def _build_ui(self):
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Цель (свободным текстом):").pack(anchor="w")
        self.task = tk.Text(root, height=6)
        self.task.pack(fill="x")

        self.confirm = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            root,
            text="Подтверждаю финансовые/высокорисковые действия",
            variable=self.confirm,
        ).pack(anchor="w", pady=6)

        ttk.Button(root, text="Выполнить", command=self._run).pack(anchor="w", pady=8)

        self.out = tk.Text(root, height=24)
        self.out.pack(fill="both", expand=True)

    def _run(self):
        task = self.task.get("1.0", "end").strip()
        if not task:
            self._log("Введите цель.\n")
            return

        run = self.agent.execute(task, confirmed=self.confirm.get())
        self._log(f"Policy: {run.policy_reason}\n")
        self._log(f"Plan: {run.plan}\n")
        self._log(f"Result:\n{run.result}\n")
        self._log(f"Review:\n{run.review}\n")
        self._log("=" * 70 + "\n")

    def _log(self, text: str):
        self.out.insert("end", text)
        self.out.see("end")


if __name__ == "__main__":
    AgentWindow().mainloop()
