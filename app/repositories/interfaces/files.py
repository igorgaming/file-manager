from typing import Iterable, Optional, Protocol
from datetime import datetime
from uuid import UUID

from app.models import File
from app.schemas.file import FileData


class IFilesRepository(Protocol):
    async def save(
        self,
        uuid: UUID,
        path: str,
        filename: Optional[str],
        content_type: Optional[str],
        size: Optional[str],
    ) -> File:
        """Save the given file metadata."""

    async def get_by_uuid(self, uuid: UUID) -> Optional[File]:
        """Get the file metadata by UUID."""

    async def delete_before_date(self, date: datetime) -> Iterable[FileData]:
        """Delete the files metadata before the given date.

        Returns:
            Iterable[FileData]: Returns the deleted files metadata.
        """
