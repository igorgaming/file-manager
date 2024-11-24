import os

from aiofiles import open
from aiofiles.os import makedirs, remove, stat
from fastapi import UploadFile

from app.conf import settings
from .interfaces.storage import IStorage


class FileSystemStorage(IStorage):
    """File system storage implementation.

    This storage is used to manage files in local filesystem.
    """

    CHUNK_SIZE = 1024 * 1024 * 100  # 100 MB

    def __init__(self, base_dir: str) -> None:
        self._base_dir = base_dir

    @property
    def location(self) -> str:
        return os.path.abspath(self._base_dir)

    def get_absolute_path(self, path: str) -> str:
        return os.path.join(self.location, path)

    async def exists(self, path: str) -> bool:
        try:
            await stat(self.get_absolute_path(path))
        except (OSError, ValueError):
            return False
        return True

    async def save(self, file: UploadFile, save_to: str) -> str:
        path = self._get_path(save_to)

        await self._create_dirs(path)

        async with open(path, mode="wb") as new_file:
            while chunk := await file.read(size=self.CHUNK_SIZE):
                await new_file.write(chunk)

        return save_to

    async def delete(self, path: str) -> None:
        await remove(self._get_path(path))

    async def _create_dirs(self, path: str) -> None:
        await makedirs(os.path.dirname(path), exist_ok=True)

    def _get_path(self, path: str) -> str:
        return os.path.join(self.location, path)


def get_filesystem_storage() -> FileSystemStorage:
    return FileSystemStorage(settings.APP_UPLOAD_DIR)
