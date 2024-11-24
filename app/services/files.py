from typing import Optional
import logging
import uuid

from fastapi import HTTPException, UploadFile

from app.storage import IStorage
from app.utils import UploadTo
from app.uow import IUoW
from app.schemas.file import FileUpload
from .interfaces.files import IFilesService


logger = logging.getLogger(__name__)


class FilesService(IFilesService):
    def __init__(self) -> None:
        self._uuid_generator = uuid.uuid4
        self._filename_sanitizer = UploadTo("files")

    async def save(
        self, uow: IUoW, storage: IStorage, uploaded_file: UploadFile
    ) -> FileUpload:
        try:
            path = await self.save_to_storage(storage, uploaded_file)
        except OSError as e:
            logger.exception("Error writing to filesystem storage")

            raise HTTPException(
                status_code=500,
                detail="Something went wrong, please try again later or contact with administrator.",
            ) from e

        async with uow:
            saved_file = await uow.files.save(
                uuid=self._uuid_generator(),
                path=path,
                file=uploaded_file,
            )
            await uow.commit()

        return FileUpload.model_validate(saved_file, from_attributes=True)

    async def save_to_storage(
        self, storage: IStorage, uploaded_file: UploadFile
    ) -> str:
        return await storage.save_file(
            uploaded_file, self._sanitize_filename(uploaded_file.filename)
        )

    def _sanitize_filename(self, filename: Optional[str]) -> str:
        return self._filename_sanitizer(filename)
