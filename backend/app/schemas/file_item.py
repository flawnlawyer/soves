from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.file_item import FileType, StorageProvider


class FileItemOut(BaseModel):
    id: str
    name: str
    original_name: str
    path: str
    mime_type: Optional[str]
    size_bytes: int
    file_type: FileType
    storage_provider: StorageProvider
    is_public: bool
    share_token: Optional[str]
    share_expires_at: Optional[datetime]
    parent_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FileItemWithChildren(FileItemOut):
    children: List["FileItemOut"] = []


class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None


class FileShare(BaseModel):
    is_public: bool = True
    expires_in_hours: Optional[int] = None  # None = no expiry


class ShareLinkOut(BaseModel):
    share_token: str
    share_url: str
    expires_at: Optional[datetime]


class StorageStats(BaseModel):
    used_bytes: int
    limit_bytes: int
    used_percent: float
    file_count: int
    folder_count: int
