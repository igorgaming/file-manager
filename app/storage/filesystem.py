import os

from aiofiles import open
from aiofiles.os import makedirs
from fastapi import UploadFile

from app.conf import settings
from .interfaces.storage import IStorage


class FileSystemStorage(IStorage):
    def __init__(self, base_dir: str) -> None:
        self._base_dir = base_dir

    @property
    def location(self) -> str:
        return os.path.abspath(self._base_dir)

    async def save_file(self, file: UploadFile, save_to: str) -> str:
        path = self._get_path(save_to)

        await self._create_dirs(path)
        await self._write_file(path, await file.read())

        return save_to

    async def _create_dirs(self, path: str) -> None:
        await makedirs(os.path.dirname(path), exist_ok=True)

    async def _write_file(self, path: str, data: bytes) -> None:
        async with open(path, mode="wb") as new_file:
            await new_file.write(data)

    def _get_path(self, path: str) -> str:
        return os.path.join(self.location, path)


def get_filesystem_storage() -> FileSystemStorage:
    return FileSystemStorage(settings.APP_UPLOAD_DIR)
