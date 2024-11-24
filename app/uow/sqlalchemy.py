from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from ..repositories import FilesRepository
from .interfaces.base import IUoW


class SQLAlchemyUnitOfWork(IUoW):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> None:
        self._session: AsyncSession = self._session_factory()

        self.files = FilesRepository(self._session)

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
