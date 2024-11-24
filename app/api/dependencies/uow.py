from typing import Annotated

from fastapi import Depends

from app.uow import IUoW
from app.uow.sqlalchemy import SQLAlchemyUnitOfWork
from .db import async_sessionmaker, get_async_session_maker


async def get_uow(
    session_maker: Annotated[async_sessionmaker, Depends(get_async_session_maker)],
) -> IUoW:
    return SQLAlchemyUnitOfWork(session_maker)
