from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Path, UploadFile, status
from fastapi.responses import FileResponse

from app.schemas.file import FileUpload
from app.dependencies import (
    IUoW,
    IStorage,
    IFilesService,
    get_uow,
    get_files_service,
    get_filesystem_storage,
)

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="File upload (also supports streaming requests)",
)
async def upload(
    bg_task: BackgroundTasks,
    uow: Annotated[IUoW, Depends(get_uow)],
    service: Annotated[IFilesService, Depends(get_files_service)],
    filestorage: Annotated[IStorage, Depends(get_filesystem_storage)],
    file: UploadFile,
) -> FileUpload:
    file_data = await service.save(uow, filestorage, file)

    bg_task.add_task(service.get_backup_task, uploaded_file=file)

    return file_data


@router.get("/download/{uuid}", summary="Download file by UUID")
async def download(
    uow: Annotated[IUoW, Depends(get_uow)],
    service: Annotated[IFilesService, Depends(get_files_service)],
    filestorage: Annotated[IStorage, Depends(get_filesystem_storage)],
    uuid: Annotated[UUID, Path()],
) -> FileResponse:
    file_data = await service.get_link(uow, filestorage, uuid)
    return FileResponse(
        file_data.link,
        filename=file_data.filename or None,
        media_type="application/octet-stream",
    )
