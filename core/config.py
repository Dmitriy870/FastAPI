from os import getenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url = "sqlite+aiosqlite:///db.sqlite3"


settings = Settings()
