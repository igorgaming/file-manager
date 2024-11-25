import logging

from app.dependencies import (
    get_async_session_maker,
    get_uow,
    get_files_service,
    get_filesystem_storage,
)
from .scheduler import scheduler

logger = logging.getLogger(__name__)


@scheduler.scheduled_job("cron", hour="3", minute="00")
async def clean_old_files():
    # Better way is to use 3rd-party DI containers that allow you
    # to resolve dependencies not only from FastAPI routes.
    service = await get_files_service()
    uow = await get_uow(await get_async_session_maker())
    storage = await get_filesystem_storage()

    try:
        await service.clean_old_files(uow, storage)
    except Exception:
        logger.exception("Error cleaning old files")
