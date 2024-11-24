import os
from pathlib import Path

from pydantic_settings import BaseSettings

current_dir = os.path.dirname(__file__)
ENV_PATH = os.path.join(current_dir, "..", ".env")


class AppSettings(BaseSettings):
    """Main application settings."""

    APP_BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
    APP_TITLE: str = "File manager app"
    APP_VERSION: str = "0.1.0"

    APP_UPLOAD_DIR: str = os.path.join(APP_BASE_DIR, "..", "uploads")
