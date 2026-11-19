# User Module

Identity entity for **BigCity AI Operations & Knowledge Intelligence Platform**.

Users are internal staff accounts. Each user belongs to exactly one **Role** (`ADMIN`, `CAMPAIGN_OPERATIONS`, `SUPPORT`, or `ENGINEER`). There is no Department entity.

JWT authentication, authorization, and RBAC are **not** part of this module yet — they follow after the User CRUD lifecycle.

---

## Architecture

```text
API  (app/api/routes/user.py)
 ↓
Service  (app/services/user_service.py)     ← validation, hashing, encrypt/decrypt, commits, logging
 ↓
Repository  (app/repositories/user_repository.py)  ← persistence only
 ↓
Database  (users table via SQLAlchemy model + Alembic)
```

| Concern | Location |
|---------|----------|
| Table / ORM | `app/db/models/user.py` |
| Migration | `app/db/migrations/versions/a1b2c3d4e5f6_create_users_table.py` |
| Request/response DTOs | `app/schemas/user.py` |
| Domain errors | `app/core/exceptions/user.py` |
| Password + mobile crypto | `app/core/security.py` |
| Unit tests | `tests/unit/services/test_user_service.py` |

Mounted in `app/main.py` at prefix `/api/v1/users`, tag `Users`.

Requires `FIELD_ENCRYPTION_KEY` in `.env` (Fernet key — see `.env.example`).

---

## Data model

| Column | Type | Notes |
|--------|------|--------|
| `id` | int PK | Auto-increment |
| `email` | string(255) | Unique, indexed, required |
| `hashed_password` | string(255) | bcrypt hash only — never plaintext |
| `full_name` | string(255) | Optional |
| `mobile_encrypted` | string(512) | Fernet ciphertext at rest |
| `mobile_hash` | string(64) | HMAC-SHA256 for uniqueness + filter |
| `role_id` | int FK → `roles.id` | Required, indexed |
| `is_active` | bool | Default `true` |
| `created_at` / `updated_at` | datetime | From `TimestampMixin` |

### Mobile PII pattern

| Layer | Behavior |
|-------|----------|
| API request/response | Plaintext `mobile_number` |
| Database | `mobile_encrypted` + `mobile_hash` only |
| List filter | `?mobile_number=` → hash → match `mobile_hash` |

Never return `password`, `hashed_password`, `mobile_encrypted`, or `mobile_hash` in API responses.

---

## API surface

Base path: `/api/v1/users`

| Method | Path | Status | Purpose |
|--------|------|--------|---------|
| `POST` | `/` | 201 | Create user |
| `GET` | `/` | 200 | List users (`offset`, `limit`, optional `mobile_number`) |
| `GET` | `/count` | 200 | Total count `{"count": N}` |
| `GET` | `/{user_id}` | 200 | Get by id (mobile decrypted) |
| `PUT` | `/{user_id}` | 200 | Partial update |
| `DELETE` | `/{user_id}` | 204 | Delete |

### Schemas

- **Create:** `email`, `password` (8–128), `mobile_number`, optional `full_name`, `role_id`, optional `is_active` (default true)
- **Update:** all fields optional (partial); password re-hashed; mobile re-encrypted/re-hashed when set
- **Response:** `id`, `email`, `full_name`, `mobile_number`, `role_id`, `is_active`, `created_at`, `updated_at`

Interactive docs: `http://127.0.0.1:8000/docs` → **Users**.

---

## Business rules (Service)

- Create / email change: reject duplicate `email` → `409 UserAlreadyExists`
- Create / mobile change: reject duplicate mobile (via hash) → `409 UserAlreadyExists`
- Create / role change: missing `role_id` → `404 RoleNotFound`
- Get / update / delete missing id → `404 UserNotFound`
- Password hashed with bcrypt before persist
- Mobile normalized, encrypted (Fernet), and HMAC-hashed before persist
- Responses decrypt mobile via `_to_response`
- Commits happen in the service (`_commit`); rollback on `SQLAlchemyError`
- Repository has no business rules — only CRUD/query helpers

---

## Status

| Step | Status |
|------|--------|
| Model → Migration → Schemas → Repo → Service → Exceptions → CRUD → Tests → Logging → Docs | ✅ |
| Seed data | ⬜ Skipped — users created via API as needed (no frozen user set) |
| Authentication (JWT) → Authorization → RBAC | ⬜ Next after this module |

---

## How to verify

```powershell
cd backend
uv run pytest tests/unit/services/test_user_service.py -v
```

Expect: `16 passed`.

With the API running (`uv run uvicorn app.main:app --reload`):

```powershell
curl http://127.0.0.1:8000/api/v1/users/count
curl "http://127.0.0.1:8000/api/v1/users/?mobile_number=%2B919876543210"
```

Expect: count JSON and list responses with plaintext `mobile_number` (never ciphertext).

---

## Next

**Authentication (JWT)** → Authorization → RBAC (protect routes using Role).
