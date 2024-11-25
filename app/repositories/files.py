from typing import Iterable, Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select

from app.models import File
from app.schemas.file import FileData
from .sqlalchemy import SQLAlchemyRepository
from .interfaces.files import IFilesRepository


class FilesRepository(SQLAlchemyRepository, IFilesRepository):
    async def save(
        self,
        uuid: UUID,
        path: str,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        size: Optional[str] = None,
    ) -> File:
        new_file = File(
            uuid=uuid,
            path=path,
            original_name=self._get_original_name(filename),
            content_type=content_type or "",
            size=size or "",
        )

        self._session.add(new_file)
        return new_file

    async def get_by_uuid(self, uuid: UUID) -> Optional[File]:
        query = select(File).where(File.uuid == uuid)
        return (await self._session.scalars(query)).first()

    async def delete_before_date(self, date: datetime) -> Iterable[FileData]:
        query = (
            delete(File)
            .where(File.created_at < date)
            .returning(File.original_name, File.path)
        )
        result = (await self._session.execute(query)).fetchall()
        return map(lambda item: FileData(filename=item[0], link=item[1]), result)

    def _get_original_name(self, filename: Optional[str]) -> str:
        if filename is None:
            return ""
        return f"...{filename[:252]}" if len(filename) > 252 else filename
