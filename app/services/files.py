from typing import Optional
import logging
import uuid

from fastapi import HTTPException, UploadFile

from app.storage import IStorage
from app.utils import UploadTo
from app.uow import IUoW
from app.schemas.file import FileData, FileUpload
from .interfaces.files import IFilesService


logger = logging.getLogger(__name__)


class FilesService(IFilesService):
    def __init__(self) -> None:
        self._uuid_generator = uuid.uuid4
        self._files_dir = UploadTo("files")

    async def save(
        self, uow: IUoW, storage: IStorage, uploaded_file: UploadFile
    ) -> FileUpload:
        path = await self.save_to_storage(storage, uploaded_file)

        size = str(uploaded_file.size)
        content_type = uploaded_file.content_type
        filename = uploaded_file.filename

        return await self._save_to_db(uow, path, filename, content_type, size)

    async def get_link(self, uow: IUoW, storage: IStorage, uuid: uuid.UUID) -> FileData:
        async with uow:
            item = await uow.files.get_by_uuid(uuid)
            if item is not None and (await storage.exists(item.path)):
                return FileData(
                    filename=item.original_name,
                    link=storage.get_absolute_path(item.path),
                )

        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    async def save_to_storage(
        self, storage: IStorage, uploaded_file: UploadFile
    ) -> str:
        try:
            path = await storage.save(
                uploaded_file, self._get_files_dir(uploaded_file.filename)
            )
            return path
        except OSError as e:
            logger.exception("Error writing to filesystem storage")

            raise HTTPException(
                status_code=500,
                detail="Something went wrong, please try again later or contact with administrator.",
            ) from e

    async def _save_to_db(
        self,
        uow: IUoW,
        path,
        filename: Optional[str],
        content_type: Optional[str],
        size: Optional[str],
    ) -> FileUpload:
        async with uow:
            saved_file = await uow.files.save(
                uuid=self._uuid_generator(),
                path=path,
                filename=filename,
                content_type=content_type,
                size=size,
            )
            await uow.commit()

        return FileUpload.model_validate(saved_file, from_attributes=True)

    def _get_files_dir(self, filename: Optional[str]) -> str:
        return self._files_dir(filename)
