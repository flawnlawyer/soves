import uuid
import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models.file_item import FileItem, FileType, StorageProvider
from app.models.user import User
from app.schemas.file_item import (
    FileItemOut, FolderCreate, FileShare, ShareLinkOut, StorageStats
)
from app.core.security import get_current_user_id
from app.core.config import settings
from app.storage.registry import get_adapter

router = APIRouter()

MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024


async def _get_user(user_id: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.post("/upload", response_model=FileItemOut, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    parent_id: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, f"File too large. Max {settings.MAX_FILE_SIZE_MB}MB")

    user = await _get_user(user_id, db)

    if user.storage_used_bytes + len(data) > user.storage_limit_bytes:
        raise HTTPException(507, "Storage limit exceeded")

    storage_key = f"{user_id}/{uuid.uuid4()}/{file.filename}"
    adapter = get_adapter()
    await adapter.upload(storage_key, data, file.content_type or "application/octet-stream")

    # Build virtual path
    path = f"/{file.filename}"
    if parent_id:
        parent_result = await db.execute(
            select(FileItem).where(FileItem.id == parent_id, FileItem.owner_id == user_id)
        )
        parent = parent_result.scalar_one_or_none()
        if parent:
            path = f"{parent.path}/{file.filename}"

    item = FileItem(
        name=file.filename,
        original_name=file.filename,
        path=path,
        storage_key=storage_key,
        mime_type=file.content_type,
        size_bytes=len(data),
        file_type=FileType.FILE,
        storage_provider=StorageProvider(settings.DEFAULT_STORAGE_ADAPTER),
        owner_id=user_id,
        parent_id=parent_id,
    )
    db.add(item)

    user.storage_used_bytes += len(data)
    await db.flush()
    await db.refresh(item)
    return item


@router.get("/", response_model=list[FileItemOut])
async def list_files(
    parent_id: Optional[str] = Query(None),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    query = select(FileItem).where(
        FileItem.owner_id == user_id,
        FileItem.is_deleted == False,  # noqa: E712
        FileItem.parent_id == parent_id,
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/stats", response_model=StorageStats)
async def storage_stats(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    user = await _get_user(user_id, db)

    file_count = await db.scalar(
        select(func.count()).where(
            FileItem.owner_id == user_id,
            FileItem.file_type == FileType.FILE,
            FileItem.is_deleted == False,  # noqa: E712
        )
    )
    folder_count = await db.scalar(
        select(func.count()).where(
            FileItem.owner_id == user_id,
            FileItem.file_type == FileType.FOLDER,
            FileItem.is_deleted == False,  # noqa: E712
        )
    )

    used_pct = (user.storage_used_bytes / user.storage_limit_bytes * 100) if user.storage_limit_bytes else 0

    return StorageStats(
        used_bytes=user.storage_used_bytes,
        limit_bytes=user.storage_limit_bytes,
        used_percent=round(used_pct, 2),
        file_count=file_count or 0,
        folder_count=folder_count or 0,
    )


@router.get("/{file_id}", response_model=FileItemOut)
async def get_file(
    file_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FileItem).where(FileItem.id == file_id, FileItem.owner_id == user_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "File not found")
    return item


@router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FileItem).where(FileItem.id == file_id, FileItem.owner_id == user_id)
    )
    item = result.scalar_one_or_none()
    if not item or item.file_type == FileType.FOLDER:
        raise HTTPException(404, "File not found")

    adapter = get_adapter(item.storage_provider.value)

    async def generator():
        async for chunk in adapter.stream(item.storage_key):
            yield chunk

    return StreamingResponse(
        generator(),
        media_type=item.mime_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{item.original_name}"'},
    )


@router.post("/folder", response_model=FileItemOut, status_code=201)
async def create_folder(
    payload: FolderCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    path = f"/{payload.name}"
    if payload.parent_id:
        parent_result = await db.execute(
            select(FileItem).where(FileItem.id == payload.parent_id, FileItem.owner_id == user_id)
        )
        parent = parent_result.scalar_one_or_none()
        if parent:
            path = f"{parent.path}/{payload.name}"

    folder = FileItem(
        name=payload.name,
        original_name=payload.name,
        path=path,
        file_type=FileType.FOLDER,
        storage_provider=StorageProvider.LOCAL,
        owner_id=user_id,
        parent_id=payload.parent_id,
    )
    db.add(folder)
    await db.flush()
    await db.refresh(folder)
    return folder


@router.post("/{file_id}/share", response_model=ShareLinkOut)
async def share_file(
    file_id: str,
    payload: FileShare,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FileItem).where(FileItem.id == file_id, FileItem.owner_id == user_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "File not found")

    token = secrets.token_urlsafe(24)
    expires_at = None
    if payload.expires_in_hours:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=payload.expires_in_hours)

    item.is_public = payload.is_public
    item.share_token = token
    item.share_expires_at = expires_at

    return ShareLinkOut(
        share_token=token,
        share_url=f"/api/v1/files/shared/{token}",
        expires_at=expires_at,
    )


@router.get("/shared/{token}")
async def access_shared_file(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FileItem).where(FileItem.share_token == token, FileItem.is_public == True)  # noqa: E712
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Shared file not found or link expired")

    if item.share_expires_at and datetime.now(timezone.utc) > item.share_expires_at:
        raise HTTPException(410, "Share link has expired")

    adapter = get_adapter(item.storage_provider.value)

    async def generator():
        async for chunk in adapter.stream(item.storage_key):
            yield chunk

    return StreamingResponse(
        generator(),
        media_type=item.mime_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{item.original_name}"'},
    )


@router.delete("/{file_id}", status_code=204)
async def delete_file(
    file_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FileItem).where(FileItem.id == file_id, FileItem.owner_id == user_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "File not found")

    item.is_deleted = True

    if item.file_type == FileType.FILE and item.storage_key:
        user = await _get_user(user_id, db)
        adapter = get_adapter(item.storage_provider.value)
        await adapter.delete(item.storage_key)
        user.storage_used_bytes = max(0, user.storage_used_bytes - item.size_bytes)
