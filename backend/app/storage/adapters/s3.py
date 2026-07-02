import aioboto3
from typing import AsyncIterator
from botocore.exceptions import ClientError

from app.storage.base import StorageAdapter, StorageObject
from app.core.config import settings

CHUNK_SIZE = 1024 * 1024  # 1MB


class S3StorageAdapter(StorageAdapter):
    """
    S3-compatible adapter — works with:
    - AWS S3
    - Cloudflare R2 (set S3_ENDPOINT_URL to your R2 endpoint)
    - MinIO (set S3_ENDPOINT_URL to your MinIO host)
    - Any S3-compatible object store
    """

    def __init__(self):
        self.session = aioboto3.Session(
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION,
        )
        self.endpoint_url = settings.S3_ENDPOINT_URL or None
        self.bucket = settings.S3_BUCKET_NAME

    def _client(self):
        return self.session.client("s3", endpoint_url=self.endpoint_url)

    async def upload(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> StorageObject:
        async with self._client() as s3:
            await s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
        return StorageObject(key=key, size_bytes=len(data), content_type=content_type)

    async def download(self, key: str) -> bytes:
        async with self._client() as s3:
            response = await s3.get_object(Bucket=self.bucket, Key=key)
            return await response["Body"].read()

    async def stream(self, key: str) -> AsyncIterator[bytes]:
        async with self._client() as s3:
            response = await s3.get_object(Bucket=self.bucket, Key=key)
            async for chunk in response["Body"].iter_chunks(CHUNK_SIZE):
                yield chunk

    async def delete(self, key: str) -> bool:
        try:
            async with self._client() as s3:
                await s3.delete_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    async def exists(self, key: str) -> bool:
        try:
            async with self._client() as s3:
                await s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    async def list(self, prefix: str = "") -> list[StorageObject]:
        results = []
        async with self._client() as s3:
            paginator = s3.get_paginator("list_objects_v2")
            async for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
                for obj in page.get("Contents", []):
                    results.append(StorageObject(key=obj["Key"], size_bytes=obj["Size"]))
        return results

    async def move(self, source_key: str, dest_key: str) -> StorageObject:
        obj = await self.copy(source_key, dest_key)
        await self.delete(source_key)
        return obj

    async def copy(self, source_key: str, dest_key: str) -> StorageObject:
        async with self._client() as s3:
            copy_source = {"Bucket": self.bucket, "Key": source_key}
            await s3.copy_object(Bucket=self.bucket, CopySource=copy_source, Key=dest_key)
            response = await s3.head_object(Bucket=self.bucket, Key=dest_key)
        return StorageObject(key=dest_key, size_bytes=response["ContentLength"])

    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        async with self._client() as s3:
            url = await s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expires_in,
            )
        return url
