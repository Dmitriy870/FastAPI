from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel


WORK_DIR = Path(__file__).parent.parent


class DBSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{WORK_DIR}/db.sqlite3"
    echo: bool = False


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DBSettings = DBSettings()


settings = Settings()
