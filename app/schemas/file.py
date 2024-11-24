from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class FileUpload(BaseModel):
    uuid: UUID


class FileData(BaseModel):
    filename: Optional[str]
    link: str
