from app.services import IFilesService
from app.services.files import FilesService


async def get_files_service() -> IFilesService:
    return FilesService()
