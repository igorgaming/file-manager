import logging.config as log_conf

from pydantic_settings import SettingsConfigDict

from .app import ENV_PATH, AppSettings
from .database import DatabaseSettings
from .security import SecuritySettings
from .logging import logging_config


class Settings(
    AppSettings,
    DatabaseSettings,
    SecuritySettings,
):
    """App configuration with support for loading values from `.env`."""

    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8")


settings = Settings()

log_conf.dictConfig(logging_config)
