from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from .mixins import TimestampsMixin


class File(TimestampsMixin, Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(unique=True)
    path: Mapped[str] = mapped_column(String(255), comment="File path in local disk")
    original_name: Mapped[str] = mapped_column(
        String(255), comment="File original name"
    )
    size: Mapped[str] = mapped_column(comment="File size in bytes")
    content_type: Mapped[str] = mapped_column(String(255), comment="File content type")

    def __repr__(self) -> str:
        return f"File(id={self.id!r}, uuid={self.uuid!r}, path={self.path!r})"
