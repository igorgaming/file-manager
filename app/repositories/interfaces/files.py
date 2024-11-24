from typing import Optional, Protocol
from uuid import UUID

from app.models import File


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
