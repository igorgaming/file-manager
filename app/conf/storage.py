from pydantic_settings import BaseSettings


class StorageSettings(BaseSettings):
    """Storage application settings."""

    CLOUD_URL: str
    CLOUD_API_URL: str = "http://localhost/cloud/api/"
    CLOUD_API_TOKEN: str
