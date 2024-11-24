from typing import BinaryIO

from app.conf import settings
from .cloud_client import CloudClient


class CloudService:
    def __init__(self, client: CloudClient, location: str) -> None:
        self._client = client
        self._location = location

    @property
    def location(self) -> str:
        return self._location

    async def has_folder(self, path: str) -> bool:
        response = await self._client.get("has_folder/", {"path": self.get_link(path)})
        return response.get("status") is True

    async def create_file(self, path: str, file: BinaryIO) -> None:
        await self._client.post(f"upload/{self.get_link(path)}", data=file)

    async def delete_file(self, path: str) -> None:
        await self._client.post(f"delete/{self.get_link(path)}")

    def get_link(self, path: str) -> str:
        return f"{self.location}{path}"


async def get_cloud_service(client: CloudClient) -> CloudService:
    return CloudService(client, settings.CLOUD_URL)
