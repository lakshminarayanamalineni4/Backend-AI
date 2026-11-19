# Topic 2 — FastAPI

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Planned |
| **Prerequisites** | [01-rest-apis.md](./01-rest-apis.md) |
| **Next topic** | [03-postgresql-sqlalchemy.md](./03-postgresql-sqlalchemy.md) |

---

## Summary

*To be expanded during study session.*

FastAPI is the Python **ASGI** framework used for all HTTP endpoints in this project. It provides automatic validation (Pydantic), OpenAPI documentation, and dependency injection for database sessions and authentication.

---

## Definition

*Planned sections: ASGI vs WSGI, application instance, routers, path operations, request/response models.*

---

## Why it matters in this project

- All REST endpoints run through FastAPI (`backend/app/main.py`)
- Auto-generated `/docs` for manual testing during development
- `Depends()` pattern powers `get_db` and `get_current_user`
- Type hints + Pydantic catch bugs before runtime

---

## Core concepts

*Planned sections:*

- Application and router structure
- Path operations (`@app.get`, `@app.post`)
- Pydantic schemas vs SQLAlchemy models
- Dependency injection (`Depends`)
- Exception handlers and `HTTPException`
- Project layout: `api/routes/`, `schemas/`, `services/`

---

## Examples (cashback platform)

*Planned examples:*

- Minimal `GET /health` route
- Router registration in `main.py`
- `UserCreate` schema validation on register
- `get_current_user` dependency on `/users/me`

---

## Common pitfalls

*Planned.*

---

## Study checkpoints

*Planned.*

---

## Related topics

| Topic | Relationship |
|-------|--------------|
| [01-rest-apis.md](./01-rest-apis.md) | REST concepts FastAPI implements |
| [03-postgresql-sqlalchemy.md](./03-postgresql-sqlalchemy.md) | DB session via `Depends(get_db)` |
| [05-jwt-authentication.md](./05-jwt-authentication.md) | Auth dependencies |

---

## Implementation reference

See [checklist.md](../checklist.md) — Phase A and Phase C.
