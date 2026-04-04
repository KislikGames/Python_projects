from dataclasses import dataclass
from pathlib import Path
import json
import webbrowser


@dataclass
class ToolResult:
    ok: bool
    message: str


class DesktopTools:
    def __init__(self, sandbox_dir: str | None = None):
        self.sandbox_dir = Path(sandbox_dir).expanduser() if sandbox_dir else None

    def _resolve_target(self, target: str) -> Path:
        path = Path(target).expanduser()
        if self.sandbox_dir:
            self.sandbox_dir.mkdir(parents=True, exist_ok=True)
            return self.sandbox_dir / path.name
        return path

    def create_text_file(self, path: str, content: str) -> ToolResult:
        try:
            target = self._resolve_target(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return ToolResult(True, f"File created: {target}")
        except Exception as exc:  # noqa: BLE001
            return ToolResult(False, f"Failed to create file: {exc}")

    def open_url(self, url: str) -> ToolResult:
        webbrowser.open(url)
        return ToolResult(True, f"Opened URL: {url}")

    def run_action(self, action_json: str) -> ToolResult:
        """Supported actions:
        {"tool":"create_text_file","path":"~/Desktop/a.txt","content":"hello"}
        {"tool":"open_url","url":"https://example.com"}
        """
        try:
            action = json.loads(action_json)
        except json.JSONDecodeError as exc:
            return ToolResult(False, f"Bad action JSON: {exc}")

        tool = action.get("tool")
        if tool == "create_text_file":
            return self.create_text_file(action.get("path", "~/Desktop/agent_note.txt"), action.get("content", ""))
        if tool == "open_url":
            return self.open_url(action.get("url", "https://example.com"))

        return ToolResult(False, f"Unknown tool: {tool}")
