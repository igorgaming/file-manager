from typing import Protocol

from fastapi import UploadFile


class IStorage(Protocol):
    @property
    def location(self) -> str: ...

    def get_absolute_path(self, path: str) -> str: ...

    async def exists(self, path: str) -> bool: ...

    async def save_file(self, file: UploadFile, save_to: str) -> str: ...
