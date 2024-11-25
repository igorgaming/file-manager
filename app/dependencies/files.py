from app.cloud.cloud import Cloud
from app.services import IFilesService
from app.storage.interfaces.storage import IStorage
from app.conf import settings


async def get_files_service() -> IFilesService:
    from app.services.files import FilesService

    return FilesService()


async def get_filesystem_storage() -> IStorage:
    from app.storage.filesystem import FileSystemStorage

    return FileSystemStorage(settings.APP_UPLOAD_DIR)


async def get_cloud_storage(cloud: Cloud) -> IStorage:
    from app.storage.cloud import CloudStorage

    return CloudStorage(cloud)
