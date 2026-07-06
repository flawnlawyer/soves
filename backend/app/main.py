from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routes import auth, files, storage, users
from app.db.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="Sōvēs API",
    description="Let Data Fly — Open-source unified storage platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(storage.router, prefix="/api/v1/storage", tags=["storage"])


@app.get("/")
async def root():
    return {"name": "Sōvēs", "version": "0.1.0", "status": "Let Data Fly"}


@app.get("/health")
async def health():
    return {"status": "ok"}
