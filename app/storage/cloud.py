import os

from fastapi import UploadFile

from app.cloud.cloud import Cloud
from .interfaces.storage import IStorage


class CloudStorage(IStorage):
    """Cloud storage example implementation.

    This storage is used to manage files in cloud filesystem.

    Its just PoC and not connected to a real service.
    """

    def __init__(self, cloud: Cloud) -> None:
        self._cloud = cloud

    @property
    def location(self) -> str:
        return os.path.abspath(self._cloud.location)

    def get_absolute_path(self, path: str) -> str:
        return self._cloud.get_link(path)

    async def exists(self, path: str) -> bool:
        return await self._cloud.has_folder(path)

    async def save(self, file: UploadFile, save_to: str) -> str:
        await self._cloud.create_file(save_to, file.file)
        return f"{self._cloud.get_link(save_to)}"

    async def delete(self, path: str) -> None:
        await self._cloud.delete_file(path)
