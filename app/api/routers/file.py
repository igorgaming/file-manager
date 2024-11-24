from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status

from app.uow import IUoW
from app.services import IFilesService
from app.schemas.file import FileUpload
from app.storage.filesystem import FileSystemStorage, get_filesystem_storage
from ..dependencies import get_uow, get_files_service

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="File upload (w/o streaming)",
)
async def upload(
    uow: Annotated[IUoW, Depends(get_uow)],
    service: Annotated[IFilesService, Depends(get_files_service)],
    filestorage: Annotated[FileSystemStorage, Depends(get_filesystem_storage)],
    file: UploadFile,
) -> FileUpload:
    file_data = await service.save(uow, filestorage, file)
    return file_data
