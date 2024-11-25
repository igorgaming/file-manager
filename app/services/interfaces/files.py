from datetime import datetime
from typing import Protocol
from uuid import UUID

from fastapi import UploadFile

from app.storage import IStorage
from app.uow import IUoW
from app.schemas.file import FileData, FileUpload


class IFilesService(Protocol):
    async def save(
        self, uow: IUoW, storage: IStorage, uploaded_file: UploadFile
    ) -> FileUpload:
        """Save the file.

        Args:
            uow (IUoW): UoW
            storage (IStorage): File storage.
            uploaded_file (UploadFile): Uploaded file.

        Returns:
            FileUpload: Uploaded file.
        """

    async def get_link(self, uow: IUoW, storage: IStorage, uuid: UUID) -> FileData:
        """Get link of the file by UUID."""

    async def get_backup_task(self, uploaded_file: UploadFile) -> None:
        """Get backup async task.

        Args:
            uploaded_file (UploadFile): Uploaded file.
        """

    async def clean_old_files(
        self, uow: IUoW, storage: IStorage, date: datetime
    ) -> None:
        """Clean old files from db and storage.

        Args:
            uow (IUoW): UoW
            storage (IStorage): File storage.
            date (datetime): Date to delete files before.
        """
