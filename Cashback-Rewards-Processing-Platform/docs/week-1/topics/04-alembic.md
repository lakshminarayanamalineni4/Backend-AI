# Topic 4 — Alembic

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Planned |
| **Prerequisites** | [03-postgresql-sqlalchemy.md](./03-postgresql-sqlalchemy.md) |
| **Next topic** | [05-jwt-authentication.md](./05-jwt-authentication.md) |

---

## Summary

*To be expanded during study session.*

Alembic manages **database migrations** — versioned, repeatable changes to PostgreSQL schema. It keeps local, CI, and production databases aligned as models evolve.

---

## Definition

*Planned sections: revision, upgrade, downgrade, autogenerate, head, migration history.*

---

## Why it matters in this project

- First migration creates the `users` table in Week 1
- Adding `transactions`, `wallets`, and indexes in later phases requires safe, tracked changes
- Interview narrative: demonstrates production-grade DB workflow

---

## Core concepts

*Planned sections:*

- `alembic init` and project layout
- `env.py` and model metadata import
- `revision --autogenerate` vs hand-written migrations
- `upgrade head` and `downgrade -1`
- Never edit applied migrations in shared environments

---

## Examples (cashback platform)

*Planned examples:*

- Initial `create users table` revision
- Adding `role` column in a later revision (hypothetical)

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
| [03-postgresql-sqlalchemy.md](./03-postgresql-sqlalchemy.md) | Models drive autogenerate |
| [07-docker-compose.md](./07-docker-compose.md) | Target database for migrations |

---

## Implementation reference

See [checklist.md](../checklist.md) — Phase B.
