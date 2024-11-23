from pydantic_settings import BaseSettings


class SecuritySettings(BaseSettings):
    """Security-related settings."""

    CORS_ORIGINS: list[str] = [
        "*",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = [
        "*",
    ]
    CORS_ALLOW_HEADERS: list[str] = [
        "*",
    ]
    CORS_EXPOSE_HEADERS: list[str] = ["Content-Disposition"]
