from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db import async_session_maker


async def get_async_session_maker() -> async_sessionmaker:
    return async_session_maker
