import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.session import Base


class FileType(str, enum.Enum):
    FILE = "file"
    FOLDER = "folder"


class StorageProvider(str, enum.Enum):
    LOCAL = "local"
    S3 = "s3"
    R2 = "r2"
    MINIO = "minio"


class FileItem(Base):
    __tablename__ = "file_items"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    original_name: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)  # virtual path in Sōvēs
    storage_key: Mapped[str] = mapped_column(String, nullable=True)  # key in storage backend
    mime_type: Mapped[str] = mapped_column(String, nullable=True)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    file_type: Mapped[FileType] = mapped_column(
        Enum(FileType), default=FileType.FILE, nullable=False
    )
    storage_provider: Mapped[StorageProvider] = mapped_column(
        Enum(StorageProvider), default=StorageProvider.LOCAL
    )
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    share_token: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    share_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    parent_id: Mapped[str] = mapped_column(
        String, ForeignKey("file_items.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    owner: Mapped["User"] = relationship("User", back_populates="files")  # noqa: F821
    children: Mapped[list["FileItem"]] = relationship(
        "FileItem", back_populates="parent", lazy="selectin"
    )
    parent: Mapped["FileItem"] = relationship(
        "FileItem", back_populates="children", remote_side="FileItem.id"
    )
