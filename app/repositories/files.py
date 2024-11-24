from uuid import UUID

from fastapi import UploadFile

from app.models import File
from .sqlalchemy import SQLAlchemyRepository
from .interfaces.files import IFilesRepository


class FilesRepository(SQLAlchemyRepository, IFilesRepository):
    async def save(
        self,
        uuid: UUID,
        path: str,
        file: UploadFile,
    ) -> File:
        new_file = File(
            uuid=uuid,
            path=path,
            original_name=self._get_original_name(file),
            size=str(file.size),
            content_type=file.content_type,
        )

        self._session.add(new_file)
        return new_file

    def _get_original_name(self, file: UploadFile) -> str:
        if file.filename is None:
            return ""
        return (
            f"...{file.filename[:252]}" if len(file.filename) > 252 else file.filename
        )
