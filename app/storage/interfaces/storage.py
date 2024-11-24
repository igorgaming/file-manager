from typing import Protocol

from fastapi import UploadFile


class IStorage(Protocol):
    @property
    def location(self) -> str: ...

    async def save_file(self, file: UploadFile, save_to: str) -> str: ...
