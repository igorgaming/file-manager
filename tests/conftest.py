from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import NullPool, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI

from app.conf import settings
from app.db.base import Base
from app.dependencies.db import get_async_session_maker
from .fixtures import *  # noqa: F403


engine = create_async_engine(settings.TEST_DATABASE_URI, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session")
async def init_db():
    """Init database."""

    async with engine.begin() as connection:
        # Create all tables.
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()

        yield


@pytest_asyncio.fixture(scope="session", autouse=True)
async def app(init_db):
    """Initialize FastAPI application."""

    from app.main import app  # inited FastAPI app

    yield app


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Get `AsyncSession` instance to query database."""

    async with engine.begin() as connection:
        session = async_session_maker(bind=connection)

        # We are making a nested Savepoint here so that after the end of the one test
        # we can roll back all the changes that were made in it to make
        # the new test work with a clean database.
        session.begin_nested()

        @event.listens_for(session.sync_session, "after_transaction_end")
        def restart_savepoint(session, transaction):
            """
            Each time that Savepoint ends, reopen it
            """

            if transaction.nested and not transaction._parent.nested:
                session.begin_nested()

        yield session

        await session.close()
        await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI, db) -> AsyncGenerator[AsyncClient, None]:
    """Get HTTP client."""

    app.dependency_overrides[get_async_session_maker] = lambda: lambda: db

    host, port = "127.0.0.1", 8000
    async with AsyncClient(
        transport=ASGITransport(app=app, client=(host, port)), base_url="http://test"
    ) as client:
        yield client

    del app.dependency_overrides[get_async_session_maker]
