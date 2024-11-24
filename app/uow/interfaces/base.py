from typing import Protocol

from app.repositories.interfaces.files import IFilesRepository


class IUoW(Protocol):
    files: IFilesRepository

    async def __aenter__(self): ...

    async def __aexit__(self, *args): ...

    async def commit(self): ...

    async def rollback(self): ...
