from typing import Any, Optional, Protocol

from uuid import UUID


class IFilesRepository(Protocol):
    async def save(
        self,
        uuid: UUID,
        path: str,
        filename: Optional[str],
        content_type: Optional[str],
        size: Optional[str],
    ) -> Any: ...
