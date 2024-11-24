from typing import Any, Protocol

from uuid import UUID

from fastapi import UploadFile


class IFilesRepository(Protocol):
    async def save(self, uuid: UUID, path: str, file: UploadFile) -> Any: ...
