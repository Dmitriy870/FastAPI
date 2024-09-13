from pydantic_settings import BaseSettings
from pathlib import Path

WORK_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{WORK_DIR}/db.sqlite3"
    db_echo: bool = True


settings = Settings()
