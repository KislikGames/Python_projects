from dataclasses import dataclass
import os

try:
    from dotenv import load_dotenv
except ImportError:  # optional dependency for tests/minimal env
    def load_dotenv():
        return None


load_dotenv()


@dataclass
class Settings:
    openai_api_key: str | None
    openai_model: str
    sandbox_dir: str | None



def load_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        sandbox_dir=os.getenv("AGENT_SANDBOX_DIR") or None,
    )
