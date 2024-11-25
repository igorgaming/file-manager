from datetime import datetime, timedelta
import logging
from app.api.dependencies.db import get_async_session_maker
from app.api.dependencies.uow import get_uow
from app.api.dependencies.files import get_files_service
from app.storage.filesystem import get_filesystem_storage
from app.conf import settings
from .scheduler import scheduler

logger = logging.getLogger(__name__)


@scheduler.scheduled_job("cron", hour="3", minute="00")
async def clean_old_files():
    # Better way is to use 3rd-party DI containers that allow you
    # to resolve dependencies not only from FastAPI routes.
    service = await get_files_service()
    uow = await get_uow(await get_async_session_maker())
    storage = get_filesystem_storage()

    before_date = datetime.now() - timedelta(days=settings.DELETE_FILES_IN_DAYS)

    try:
        await service.clean_old_files(uow, storage, before_date)
    except Exception:
        logger.exception("Error cleaning old files")
