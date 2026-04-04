import unittest
from pathlib import Path

from agent.core import DesktopAgent


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_memory.db"
        if Path(self.db_path).exists():
            Path(self.db_path).unlink()
        self.agent = DesktopAgent(memory_path=self.db_path)

    def tearDown(self):
        if Path(self.db_path).exists():
            Path(self.db_path).unlink()

    def test_wordle_plan(self):
        response = self.agent.run("Реши wordle")
        self.assertEqual(response.plan_skill, "solve_wordle")
        self.assertIn("Opened Wordle", response.result)

    def test_finance_requires_confirmation(self):
        response = self.agent.run("Заработай 100 рублей и переведи на карту")
        self.assertIn("Confirmation required", response.result)

    def test_finance_with_confirmation(self):
        response = self.agent.run(
            "Заработай 100 рублей и переведи на карту",
            confirmed=True,
            payout_details="+79990000000",
        )
        self.assertEqual(response.plan_skill, "earn_100_rub")
        self.assertIn("safe microtask plan", response.result)


if __name__ == "__main__":
    unittest.main()
