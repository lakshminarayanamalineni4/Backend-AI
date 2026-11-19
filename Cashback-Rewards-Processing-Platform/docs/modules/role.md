# Role Module

Identity foundation entity for **BigCity AI Operations & Knowledge Intelligence Platform**.

Roles define the frozen access set used by internal teams. **User** depends on Role. There is no Department entity in the frozen architecture.

## Frozen role names

```text
ADMIN
CAMPAIGN_OPERATIONS
SUPPORT
ENGINEER
```

These four names are present in the database. Role is complete.

---

## Next identity work

**User** CRUD lifecycle is complete (`docs/modules/user.md`). Next: Authentication (JWT) → Authorization → RBAC.

## Architecture

```text
API  (app/api/routes/role.py)
 ↓
Service  (app/services/role_service.py)     ← validation, uniqueness, commits, logging
 ↓
Repository  (app/repositories/role_repository.py)  ← persistence only
 ↓
Database  (roles table via SQLAlchemy model + Alembic)
```

| Concern | Location |
|---------|----------|
| Table / ORM | `app/db/models/role.py` |
| Migration | `app/db/migrations/versions/ceb1f25f7b58_create_roles_table.py` |
| Request/response DTOs | `app/schemas/role.py` |
| Domain errors | `app/core/exceptions/role.py` |
| Unit tests | `tests/unit/services/test_role_service.py` |

Mounted in `app/main.py` at prefix `/api/v1/roles`, tag `Roles`.

---

## Data model

| Column | Type | Notes |
|--------|------|--------|
| `id` | int PK | Auto-increment |
| `name` | string(50) | Unique, indexed, required |
| `description` | text | Optional |
| `created_at` / `updated_at` | datetime | From `TimestampMixin` |

---

## API surface

Base path: `/api/v1/roles`

| Method | Path | Status | Purpose |
|--------|------|--------|---------|
| `POST` | `/` | 201 | Create role |
| `GET` | `/` | 200 | List roles (`offset`, `limit`) |
| `GET` | `/count` | 200 | Total count `{"count": N}` |
| `GET` | `/{role_id}` | 200 | Get by id |
| `PUT` | `/{role_id}` | 200 | Partial update |
| `DELETE` | `/{role_id}` | 204 | Delete |

### Schemas

- **Create:** `name` (2–50 chars), optional `description` (max 500)
- **Update:** both fields optional (partial)
- **Response:** `id`, `name`, `description`, `created_at`, `updated_at`

Interactive docs: `http://127.0.0.1:8000/docs` → **Roles**.

---

## Business rules (Service)

- Create / rename: reject duplicate `name` → `409 RoleAlreadyExists`
- Get / update / delete missing id → `404 RoleNotFound`
- Commits happen in the service (`_commit`); rollback on `SQLAlchemyError`
- Repository has no business rules — only CRUD/query helpers

---

## Status

| Step | Status |
|------|--------|
| Model → Migration → Schemas → Repo → Service → Exceptions → CRUD → Tests → Logging → Docs | ✅ |
| Seed data (four frozen roles) | ✅ Present in DB |

---

## How to verify

```powershell
cd backend
uv run pytest tests/unit/services/test_role_service.py -v
```

Expect: all tests passed.

With the API running (`uv run uvicorn app.main:app --reload`):

```powershell
curl http://127.0.0.1:8000/api/v1/roles/count
curl http://127.0.0.1:8000/api/v1/roles
```

Expect: `{"count": 4}` (or at least the four frozen names) and a list including `ADMIN`, `CAMPAIGN_OPERATIONS`, `SUPPORT`, `ENGINEER`.

---

## Next identity entity

**User** docs: `docs/modules/user.md`. Next platform step: **Authentication (JWT)**.
