# Topic 8 — Environment Configuration

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Planned |
| **Prerequisites** | [02-fastapi.md](./02-fastapi.md) |
| **Next topic** | [09-pytest.md](./09-pytest.md) |

---

## Summary

*To be expanded during study session.*

**Environment configuration** separates secrets and environment-specific values (database URL, JWT secret) from application code using `.env` files and typed settings classes.

---

## Definition

*Planned sections: environment variables, `.env`, `pydantic-settings`, twelve-factor config, secrets management.*

---

## Why it matters in this project

- `JWT_SECRET` must differ between local, CI, and production
- Database host changes from `localhost` (Docker) to RDS (AWS) without code changes
- `.env.example` documents required variables for new contributors

---

## Core concepts

*Planned sections:*

- `Settings` class with `BaseSettings`
- Loading from `.env` automatically
- Required vs optional variables with defaults (dev only)
- Never commit `.env` — use `.gitignore`
- `.env.example` as safe template

---

## Examples (cashback platform)

*Planned examples:*

```env
DATABASE_URL=postgresql://cashback:cashback@localhost:5432/cashback
JWT_SECRET=change-me-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

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
| [05-jwt-authentication.md](./05-jwt-authentication.md) | Reads `JWT_SECRET` |
| [07-docker-compose.md](./07-docker-compose.md) | `DATABASE_URL` host/port |

---

## Implementation reference

See [checklist.md](../checklist.md) — Phase A and Phase C.
