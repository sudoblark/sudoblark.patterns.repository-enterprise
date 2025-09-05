import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    backend: str = os.getenv("PERSIST_BACKEND", "sqlite").strip().lower()
    sqlite_path: Path = Path(os.getenv("SQLITE_PATH", "app.db"))
    json_dir: Path = Path(os.getenv("JSON_DIR", "data"))


def get_settings() -> Settings:
    return Settings()
