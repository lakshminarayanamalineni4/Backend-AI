# Topic 3 — PostgreSQL + SQLAlchemy

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Planned |
| **Prerequisites** | [02-fastapi.md](./02-fastapi.md) |
| **Next topic** | [04-alembic.md](./04-alembic.md) |

---

## Summary

*To be expanded during study session.*

PostgreSQL is the primary relational database. SQLAlchemy ORM maps Python classes to tables so the FastAPI app can persist users (and later transactions, wallets) without raw SQL in every route.

---

## Definition

*Planned sections: RDBMS, tables, rows, ORM, engine, session, model, migration-ready schema.*

---

## Why it matters in this project

- Users table is the first persistent data in Week 1
- Transactions, wallet ledger, and audit logs build on the same patterns
- SQLAlchemy sessions integrate with FastAPI via `get_db` dependency

---

## Core concepts

*Planned sections:*

- Connection string (`DATABASE_URL`)
- Declarative base and `User` model
- Session lifecycle (open → commit → close)
- Primary keys (UUID vs integer)
- Indexes on `email` (unique)
- Relationship previews for transactions (Month 1)

---

## Examples (cashback platform)

*Planned examples:*

- `User` model fields: `id`, `email`, `hashed_password`, `role`, `created_at`
- Creating a user in a route with `db.add()` / `db.commit()`
- Querying by email for login

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
| [04-alembic.md](./04-alembic.md) | Schema migrations from models |
| [07-docker-compose.md](./07-docker-compose.md) | Running PostgreSQL locally |
| [05-jwt-authentication.md](./05-jwt-authentication.md) | Stores `hashed_password` |

---

## Implementation reference

See [checklist.md](../checklist.md) — Phase B.
