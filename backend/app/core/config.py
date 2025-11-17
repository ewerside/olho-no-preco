import os
from functools import lru_cache
from pathlib import Path


class Settings:
    """Project wide configuration loaded from environment variables."""

    project_name: str = "Olho no Preço API"
    api_version: str = "0.1.0"

    def __init__(self) -> None:
        data_dir = Path(os.getenv("DATA_DIR", "backend/data"))
        data_dir.mkdir(parents=True, exist_ok=True)
        default_db_path = data_dir / "olho_no_preco.db"
        self.database_url = os.getenv(
            "DATABASE_URL", f"sqlite:///{default_db_path.as_posix()}"
        )
        self.frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")


@lru_cache
def get_settings() -> Settings:
    return Settings()
