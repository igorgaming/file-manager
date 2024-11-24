from uuid import UUID
from pydantic import BaseModel


class FileUpload(BaseModel):
    uuid: UUID
