from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, AsyncIterator


@dataclass
class StorageObject:
    key: str
    size_bytes: int
    content_type: Optional[str] = None
    etag: Optional[str] = None


class StorageAdapter(ABC):
    """
    Base interface for all Sōvēs storage backends.
    Every provider implements these methods identically —
    the rest of the app never knows which backend it's talking to.
    """

    @abstractmethod
    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> StorageObject:
        """Upload bytes to the storage backend. Returns metadata."""
        ...

    @abstractmethod
    async def download(self, key: str) -> bytes:
        """Download and return file bytes."""
        ...

    @abstractmethod
    async def stream(self, key: str) -> AsyncIterator[bytes]:
        """Stream file in chunks — for large files."""
        ...

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a file. Returns True if deleted, False if not found."""
        ...

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists."""
        ...

    @abstractmethod
    async def list(self, prefix: str = "") -> list[StorageObject]:
        """List objects under a prefix."""
        ...

    @abstractmethod
    async def move(self, source_key: str, dest_key: str) -> StorageObject:
        """Move/rename a file."""
        ...

    @abstractmethod
    async def copy(self, source_key: str, dest_key: str) -> StorageObject:
        """Copy a file to a new key."""
        ...

    @abstractmethod
    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        """Get a presigned/direct URL for a file."""
        ...
