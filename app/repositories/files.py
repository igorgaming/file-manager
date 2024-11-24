from typing import Optional
from uuid import UUID

from sqlalchemy import select

from app.models import File
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

    def _get_original_name(self, filename: Optional[str]) -> str:
        if filename is None:
            return ""
        return f"...{filename[:252]}" if len(filename) > 252 else filename
