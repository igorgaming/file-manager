from functools import cached_property

from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database-related settings."""

    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    TEST_DB: str = "tests"

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def DATABASE_URI(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ).unicode_string()

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def TEST_DATABASE_URI(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.TEST_DB,
        ).unicode_string()
