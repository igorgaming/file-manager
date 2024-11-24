from typing import Protocol

from app.repositories.interfaces.files import IFilesRepository


class IUoW(Protocol):
    files: IFilesRepository
    """Repository for managing Files."""

    async def __aenter__(self): ...

    async def __aexit__(self, *args): ...

    async def commit(self):
        """Commit changes in current transaction."""

    async def rollback(self):
        """Rollback changes in current transaction."""
