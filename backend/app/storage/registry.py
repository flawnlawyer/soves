from app.storage.base import StorageAdapter
from app.storage.adapters.local import LocalStorageAdapter
from app.core.config import settings

_adapters: dict[str, StorageAdapter] = {}


def get_adapter(provider: str = None) -> StorageAdapter:
    """
    Returns the appropriate storage adapter.
    Adapters are singletons — instantiated once and reused.
    """
    provider = provider or settings.DEFAULT_STORAGE_ADAPTER

    if provider not in _adapters:
        if provider == "local":
            _adapters[provider] = LocalStorageAdapter()
        elif provider in ("s3", "r2", "minio"):
            from app.storage.adapters.s3 import S3StorageAdapter
            _adapters[provider] = S3StorageAdapter()
        else:
            raise ValueError(f"Unknown storage provider: {provider}")

    return _adapters[provider]
