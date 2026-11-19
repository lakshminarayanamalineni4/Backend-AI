# Week 1 Implementation Checklist

Manual step-by-step guide for building the auth MVP. Complete [curriculum topics](./curriculum.md) in parallel or immediately before each phase.

> **Prerequisite:** Python 3.11+, Docker Desktop, Git Bash (Windows) or equivalent shell.

---

## Phase A — Backend shell

### Create folder structure

From the repository root:

```
backend/
  app/
    api/
      routes/
    core/
    models/
    schemas/
    services/
  tests/
docker/
```

`alembic/` is created in Phase B via `alembic init`.

### Python environment

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate    # Windows Git Bash
pip install fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary alembic \
  "python-jose[cryptography]" "passlib[bcrypt]" pydantic-settings python-multipart
pip freeze > requirements.txt
```

### Files to create

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app instance + `GET /health` |
| `backend/app/core/config.py` | Settings from environment (`DATABASE_URL`, `JWT_SECRET`) |
| `backend/.env.example` | Documented template (no real secrets) |
| `.env` | Local secrets (gitignored) |

### Verify

```bash
uvicorn app.main:app --reload --port 8000
```

- Open http://127.0.0.1:8000/health → expect `{"status":"ok"}`
- Open http://127.0.0.1:8000/docs → Swagger UI loads

**Topics:** REST APIs (1), FastAPI (2), Environment config (8)

---

## Phase B — Database and migrations

### Files to create

| File | Purpose |
|------|---------|
| `docker-compose.yml` | PostgreSQL service on port `5432` |
| `backend/app/core/database.py` | SQLAlchemy engine + `SessionLocal` + `get_db` |
| `backend/app/models/user.py` | `User` ORM model (`id`, `email`, `hashed_password`, `role`, timestamps) |
| `backend/alembic.ini` | Alembic configuration |
| `backend/alembic/env.py` | Migration runtime (imports models) |

### Commands

```bash
# From repo root
docker compose up -d

# From backend/ with venv active
alembic init alembic
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

### Verify

- `docker compose ps` → PostgreSQL container running
- `alembic current` → shows latest revision
- Connect to DB (optional): confirm `users` table exists

**Topics:** PostgreSQL + SQLAlchemy (3), Alembic (4), Docker Compose (7)

---

## Phase C — Authentication

### Files to create

| File | Purpose |
|------|---------|
| `backend/app/schemas/user.py` | Pydantic: `UserCreate`, `UserRead`, `Token`, `LoginRequest` |
| `backend/app/services/auth.py` | Password hashing, JWT create/verify, user lookup |
| `backend/app/api/deps.py` | `get_current_user`, optional `require_admin` |
| `backend/app/api/routes/auth.py` | `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh` |
| `backend/app/api/routes/users.py` | `GET /users/me` |

Register routers in `backend/app/main.py`.

### Environment variables (`.env`)

```env
DATABASE_URL=postgresql://cashback:cashback@localhost:5432/cashback
JWT_SECRET=change-me-in-production-use-long-random-string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Verify (Swagger `/docs` or curl)

| Request | Expected |
|---------|----------|
| `POST /auth/register` | `201`, user JSON without password |
| `POST /auth/login` | `200`, `access_token` + `refresh_token` |
| `GET /users/me` + Bearer | `200`, current user |
| `GET /users/me` without token | `401` |

**Topics:** JWT (5), RBAC (6), REST APIs (1)

---

## Phase D — Tests

### Install test dependencies

```bash
pip install pytest httpx
pip freeze > requirements.txt
```

### Files to create

| File | Purpose |
|------|---------|
| `backend/tests/conftest.py` | Test client, test DB session, auth helpers |
| `backend/tests/test_auth.py` | Register, login, duplicate email, protected route |

### Verify

```bash
pytest -v
```

All tests should pass.

**Topics:** Pytest (9)

---

## Phase E — Frontend (optional, end of Week 1)

| Item | Owner | Notes |
|------|-------|-------|
| Angular scaffold | AI-assisted | `frontend/` with standalone components |
| Login / register pages | AI-assisted | Wire to `POST /auth/*` |
| JWT interceptor | AI-assisted | Attach Bearer token to API calls |
| Route guards | AI-assisted | Redirect unauthenticated users |

**Prerequisite:** Phase C auth endpoints working and tested.

---

## Suggested `.gitignore` entries

Ensure these are ignored before first commit:

```
.env
backend/.venv/
__pycache__/
*.pyc
.pytest_cache/
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Connection refused` on DB | PostgreSQL not running | `docker compose up -d` |
| `alembic` cannot find models | `env.py` missing model imports | Import `User` in `alembic/env.py` |
| `401` on valid token | Wrong `JWT_SECRET` or expired token | Re-login; check `.env` |
| `ModuleNotFoundError: app` | Wrong working directory | Run `uvicorn` from `backend/` |

---

## Next steps after Week 1

- Transaction models and `POST /transactions` (Phase 1 continuation)
- GitHub Actions CI running pytest
- Angular auth UI end-to-end
- Tag `phase-1` when Month 1 scope is complete
