from typing import Protocol

from fastapi import UploadFile

from app.storage import IStorage
from app.uow import IUoW
from app.schemas.file import FileUpload


class IFilesService(Protocol):
    async def save(
        self, uow: IUoW, storage: IStorage, uploaded_file: UploadFile
    ) -> FileUpload: ...
