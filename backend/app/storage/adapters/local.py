import os
import shutil
import aiofiles
from typing import AsyncIterator
from pathlib import Path

from app.storage.base import StorageAdapter, StorageObject
from app.core.config import settings

CHUNK_SIZE = 1024 * 1024  # 1MB chunks


class LocalStorageAdapter(StorageAdapter):
    """
    Stores files on the local filesystem.
    Default adapter for development and self-hosted deployments.
    """

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or settings.LOCAL_STORAGE_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _resolve(self, key: str) -> Path:
        # Prevent path traversal
        safe_key = key.lstrip("/").replace("..", "")
        path = self.base_path / safe_key
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    async def upload(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> StorageObject:
        path = self._resolve(key)
        async with aiofiles.open(path, "wb") as f:
            await f.write(data)
        return StorageObject(key=key, size_bytes=len(data), content_type=content_type)

    async def download(self, key: str) -> bytes:
        path = self._resolve(key)
        if not path.exists():
            raise FileNotFoundError(f"Key not found: {key}")
        async with aiofiles.open(path, "rb") as f:
            return await f.read()

    async def stream(self, key: str) -> AsyncIterator[bytes]:
        path = self._resolve(key)
        if not path.exists():
            raise FileNotFoundError(f"Key not found: {key}")
        async with aiofiles.open(path, "rb") as f:
            while chunk := await f.read(CHUNK_SIZE):
                yield chunk

    async def delete(self, key: str) -> bool:
        path = self._resolve(key)
        if path.exists():
            path.unlink()
            return True
        return False

    async def exists(self, key: str) -> bool:
        return self._resolve(key).exists()

    async def list(self, prefix: str = "") -> list[StorageObject]:
        base = self.base_path / prefix.lstrip("/") if prefix else self.base_path
        results = []
        if not base.exists():
            return results
        for p in base.rglob("*"):
            if p.is_file():
                rel = str(p.relative_to(self.base_path))
                results.append(StorageObject(key=rel, size_bytes=p.stat().st_size))
        return results

    async def move(self, source_key: str, dest_key: str) -> StorageObject:
        src = self._resolve(source_key)
        dst = self._resolve(dest_key)
        shutil.move(str(src), str(dst))
        return StorageObject(key=dest_key, size_bytes=dst.stat().st_size)

    async def copy(self, source_key: str, dest_key: str) -> StorageObject:
        src = self._resolve(source_key)
        dst = self._resolve(dest_key)
        shutil.copy2(str(src), str(dst))
        return StorageObject(key=dest_key, size_bytes=dst.stat().st_size)

    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        # Local adapter returns an API download URL
        return f"/api/v1/files/download/{key}"
