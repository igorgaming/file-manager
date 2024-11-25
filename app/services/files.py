from typing import Optional
import logging
import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException, UploadFile, status

from app.schemas.file import FileData, FileUpload
from app.cloud.exceptions import BaseCloudException
from app.dependencies import (
    IUoW,
    IStorage,
    get_cloud_storage,
    get_cloud_client,
    get_cloud,
)
from app.utils import UploadTo
from app.conf import settings
from .interfaces.files import IFilesService


logger = logging.getLogger(__name__)


class FilesService(IFilesService):
    def __init__(self) -> None:
        self._uuid_generator = uuid.uuid4
        self._path_generator = UploadTo("files")

    async def save(
        self, uow: IUoW, storage: IStorage, uploaded_file: UploadFile
    ) -> FileUpload:
        path = await self._save_to_storage(storage, uploaded_file)

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    async def get_backup_task(self, uploaded_file: UploadFile) -> None:
        try:
            # This is a background task, so we cant rely on FastAPI DI injector,
            # we must resolve them manually.
            # See https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#background-tasks-and-dependencies-with-yield-technical-details
            async with await get_cloud_client() as client:
                service = await get_cloud(client)
                storage = await get_cloud_storage(service)
                await storage.save(
                    uploaded_file, self._generate_file_path(uploaded_file.filename)
                )
        except BaseCloudException:
            logger.exception("Error writing to cloud storage")
            raise

    async def clean_old_files(self, uow: IUoW, storage: IStorage) -> None:
        before_date = datetime.now() - timedelta(days=settings.DELETE_FILES_IN_DAYS)

        async with uow:
            items = await uow.files.delete_before_date(before_date)

            for item in items:
                await storage.delete(item.link)

            await uow.commit()

    async def _save_to_storage(
        self, storage: IStorage, uploaded_file: UploadFile
    ) -> str:
        try:
            path = await storage.save(
                uploaded_file, self._generate_file_path(uploaded_file.filename)
            )
            return path
        except OSError as e:
            logger.exception("Error writing to filesystem storage")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

    def _generate_file_path(self, filename: Optional[str]) -> str:
        """Get final path to the file.

        Args:
            filename (Optional[str]): Filename with extension.

        Returns:
            str: Final path to the file.
        """
        return self._path_generator(filename)
