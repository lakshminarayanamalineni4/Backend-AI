# Week 1 Curriculum

Ordered learning objectives for the backend auth MVP. Complete topics sequentially; implementation in [checklist.md](./checklist.md) maps to topics 2–9.

## Topic map

```
REST APIs → FastAPI → PostgreSQL/SQLAlchemy → Alembic
    → JWT → RBAC → Docker Compose → Env config → Pytest
```

---

## Topic 1 — REST APIs

**Document:** [topics/01-rest-apis.md](./topics/01-rest-apis.md)  
**Status:** Documented

**Learning objectives**

- Explain what a REST API is and how HTTP clients communicate with servers
- Map HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) to CRUD operations
- Interpret common status codes (`200`, `201`, `400`, `401`, `403`, `404`, `422`, `500`)
- Design resource-oriented URLs for the cashback platform
- Read and write JSON request/response bodies for auth endpoints

**Maps to implementation:** All API routes; testing via Postman or `/docs`

---

## Topic 2 — FastAPI

**Document:** [topics/02-fastapi.md](./topics/02-fastapi.md)  
**Status:** Planned

**Learning objectives**

- Describe FastAPI’s role as an ASGI web framework
- Create routes, path parameters, and query parameters
- Use Pydantic models for request/response validation
- Understand dependency injection (`Depends`) for DB sessions and auth
- Navigate auto-generated OpenAPI docs at `/docs`

**Maps to implementation:** `backend/app/main.py`, routers, `schemas/`, `api/deps.py`

---

## Topic 3 — PostgreSQL + SQLAlchemy

**Document:** [topics/03-postgresql-sqlalchemy.md](./topics/03-postgresql-sqlalchemy.md)  
**Status:** Planned

**Learning objectives**

- Explain relational storage for users and future transaction data
- Define SQLAlchemy ORM models and table relationships
- Use sessions for create/read/update patterns
- Understand connection strings and connection pooling basics

**Maps to implementation:** `backend/app/core/database.py`, `backend/app/models/user.py`

---

## Topic 4 — Alembic

**Document:** [topics/04-alembic.md](./topics/04-alembic.md)  
**Status:** Planned

**Learning objectives**

- Explain database migrations vs. ad-hoc SQL scripts
- Generate revisions with `--autogenerate`
- Apply and roll back migrations with `upgrade` / `downgrade`
- Keep schema in sync across local, CI, and production

**Maps to implementation:** `backend/alembic/`, `alembic.ini`

---

## Topic 5 — JWT + refresh tokens

**Document:** [topics/05-jwt-authentication.md](./topics/05-jwt-authentication.md)  
**Status:** Planned

**Learning objectives**

- Contrast stateless JWT auth with server-side sessions
- Structure access vs. refresh tokens and expiry
- Hash passwords with bcrypt; never store plaintext
- Validate tokens on protected routes via FastAPI dependencies

**Maps to implementation:** `backend/app/services/auth.py`, `POST /auth/login`, `GET /users/me`

---

## Topic 6 — RBAC basics

**Document:** [topics/06-rbac.md](./topics/06-rbac.md)  
**Status:** Planned

**Learning objectives**

- Define Role-Based Access Control (`user`, `admin`)
- Enforce role checks on route dependencies
- Return `403 Forbidden` vs. `401 Unauthorized` correctly

**Maps to implementation:** `role` column on `User`, admin-only routes (light touch in Week 1)

---

## Topic 7 — Docker Compose

**Document:** [topics/07-docker-compose.md](./topics/07-docker-compose.md)  
**Status:** Planned

**Learning objectives**

- Run PostgreSQL as a containerized service
- Understand ports, volumes, and service networking
- Use `docker compose up -d` for reproducible local dev

**Maps to implementation:** `docker-compose.yml` at repo root

---

## Topic 8 — Environment configuration

**Document:** [topics/08-environment-config.md](./topics/08-environment-config.md)  
**Status:** Planned

**Learning objectives**

- Separate secrets from code using `.env` and `pydantic-settings`
- Document required variables in `.env.example`
- Avoid committing secrets (`.gitignore`)

**Maps to implementation:** `backend/app/core/config.py`, `.env`, `.env.example`

---

## Topic 9 — Pytest

**Document:** [topics/09-pytest.md](./topics/09-pytest.md)  
**Status:** Planned

**Learning objectives**

- Write integration tests for HTTP endpoints with `httpx` / `TestClient`
- Use fixtures for test database and authenticated clients
- Assert status codes and response bodies for auth flows

**Maps to implementation:** `backend/tests/conftest.py`, `backend/tests/test_auth.py`

---

## Progress tracker

Copy this table into your notes and update as you go:

| # | Topic | Studied | Implemented | Notes |
|---|-------|---------|-------------|-------|
| 1 | REST APIs | ☐ | ☐ | |
| 2 | FastAPI | ☐ | ☐ | |
| 3 | PostgreSQL + SQLAlchemy | ☐ | ☐ | |
| 4 | Alembic | ☐ | ☐ | |
| 5 | JWT | ☐ | ☐ | |
| 6 | RBAC | ☐ | ☐ | |
| 7 | Docker Compose | ☐ | ☐ | |
| 8 | Environment config | ☐ | ☐ | |
| 9 | Pytest | ☐ | ☐ | |
