# Sōvēs — Let Data Fly

> Open-source unified cloud storage platform. Store, sync, and share across providers through one interface.

![License](https://img.shields.io/badge/license-MIT-gold)
![Status](https://img.shields.io/badge/status-MVP-amber)

## Stack

| Layer | Tech |
|-------|------|
| Frontend | React 18, Vite, TypeScript, Tailwind CSS, TanStack Query |
| Backend | Python, FastAPI, SQLAlchemy (async), Pydantic v2 |
| Database | SQLite (dev) / PostgreSQL via Supabase (prod) |
| Storage | Local FS (dev) / S3-compatible: R2, MinIO, AWS (prod) |
| Auth | JWT + Refresh Tokens |

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # edit as needed
uvicorn app.main:app --reload
```
rel
API runs at `http://localhost:8000`
Swagger UI at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

UI runs at `http://localhost:5173`

### Docker (both together)

```bash
cd docker
docker compose up --build
```

## Storage Adapters

Sōvēs abstracts storage behind a common interface. Set `DEFAULT_STORAGE_ADAPTER` in `.env`:

| Value | Provider |
|-------|----------|
| `local` | Local filesystem (default) |
| `s3` | AWS S3 |
| `r2` | Cloudflare R2 |
| `minio` | MinIO self-hosted |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Register |
| POST | `/api/v1/auth/login` | Login → tokens |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Current user |
| POST | `/api/v1/files/upload` | Upload file |
| GET | `/api/v1/files/` | List files |
| GET | `/api/v1/files/stats` | Storage stats |
| GET | `/api/v1/files/{id}/download` | Download file |
| POST | `/api/v1/files/folder` | Create folder |
| POST | `/api/v1/files/{id}/share` | Create share link |
| GET | `/api/v1/files/shared/{token}` | Access shared file |
| DELETE | `/api/v1/files/{id}` | Delete file |

## Project Structure

```
soves/
├── backend/
│   └── app/
│       ├── api/routes/     # FastAPI route handlers
│       ├── core/           # Config, security, JWT
│       ├── db/             # SQLAlchemy session
│       ├── models/         # ORM models (User, FileItem)
│       ├── schemas/        # Pydantic schemas
│       └── storage/
│           ├── base.py         # Abstract adapter interface
│           ├── registry.py     # Provider resolver
│           └── adapters/
│               ├── local.py    # Local filesystem
│               └── s3.py       # S3-compatible (R2, MinIO, AWS)
├── frontend/
│   └── src/
│       ├── components/     # React components
│       ├── hooks/          # TanStack Query hooks
│       ├── lib/            # API client, utils
│       ├── pages/          # Route pages
│       ├── store/          # Zustand state
│       └── types/          # TypeScript types
├── docker/
└── docs/
```

## License

MIT — built by Ayush (@flawnlawyer)
