from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, UploadFile, status
from fastapi.responses import FileResponse

from app.uow import IUoW
from app.services import IFilesService
from app.schemas.file import FileUpload
from app.storage.filesystem import FileSystemStorage, get_filesystem_storage
from ..dependencies import get_uow, get_files_service

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="File upload (also supports streaming requests)",
)
async def upload(
    uow: Annotated[IUoW, Depends(get_uow)],
    service: Annotated[IFilesService, Depends(get_files_service)],
    filestorage: Annotated[FileSystemStorage, Depends(get_filesystem_storage)],
    file: UploadFile,
) -> FileUpload:
    file_data = await service.save(uow, filestorage, file)
    return file_data


@router.get("/download/{uuid}", summary="Download file by UUID")
async def download(
    uow: Annotated[IUoW, Depends(get_uow)],
    service: Annotated[IFilesService, Depends(get_files_service)],
    filestorage: Annotated[FileSystemStorage, Depends(get_filesystem_storage)],
    uuid: Annotated[UUID, Path()],
) -> FileResponse:
    file_data = await service.get_link(uow, filestorage, uuid)
    return FileResponse(
        file_data.link,
        filename=file_data.filename or None,
        media_type="application/octet-stream",
    )
