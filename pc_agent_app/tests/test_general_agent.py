import tempfile
import unittest
from pathlib import Path

from desktop_agent import GeneralDesktopAgent
from tools import DesktopTools


class AgentV2Tests(unittest.TestCase):
    def test_requires_confirmation_for_financial_task(self):
        agent = GeneralDesktopAgent(db_path="test_memory.db")
        run = agent.execute("Переведи деньги на карту")
        self.assertFalse(run.allowed)
        self.assertIn("Confirmation required", run.result)

    def test_file_tool_writes_to_sandbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            tools = DesktopTools(sandbox_dir=tmp)
            result = tools.create_text_file("~/Desktop/abc.txt", "hello")
            self.assertTrue(result.ok)
            self.assertTrue((Path(tmp) / "abc.txt").exists())


if __name__ == "__main__":
    unittest.main()
