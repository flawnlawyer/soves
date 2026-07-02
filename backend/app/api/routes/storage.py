from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/providers")
async def list_providers():
    return {
        "default": settings.DEFAULT_STORAGE_ADAPTER,
        "available": ["local", "s3", "r2", "minio"],
        "configured": [
            "local",
            *( ["s3"] if settings.S3_ACCESS_KEY_ID else []),
        ],
    }
