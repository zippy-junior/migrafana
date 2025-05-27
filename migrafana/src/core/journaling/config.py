import os
from pathlib import Path


from pydantic_settings import BaseSettings
from pydantic.types import DirectoryPath


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_BACKUP_COUNT: int = 7
    LOG_FILE_PATH: DirectoryPath = Path(os.environ.get("LOG_FILE_PATH", Path(__file__).resolve().parent))

    class Config:
        case_sensitive = False
