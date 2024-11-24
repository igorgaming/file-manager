from typing import Protocol
from uuid import UUID

from fastapi import UploadFile

from app.storage import IStorage
from app.uow import IUoW
from app.schemas.file import FileData, FileUpload


class IFilesService(Protocol):
    async def save(
        self, uow: IUoW, storage: IStorage, uploaded_file: UploadFile
    ) -> FileUpload: ...

    async def get_link(self, uow: IUoW, storage: IStorage, uuid: UUID) -> FileData: ...
