# Topic 7 — Docker Compose

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Planned |
| **Prerequisites** | None (can study in parallel with Topic 3) |
| **Next topic** | [08-environment-config.md](./08-environment-config.md) |

---

## Summary

*To be expanded during study session.*

**Docker Compose** runs multi-container local environments from a single `docker-compose.yml`. Week 1 uses it to start PostgreSQL with consistent credentials and ports on every machine.

---

## Definition

*Planned sections: image, container, service, volume, port mapping, compose file, `docker compose up`.*

---

## Why it matters in this project

- Developers avoid installing PostgreSQL natively on Windows/Mac/Linux
- Same `DATABASE_URL` works for everyone
- Later phases add Redis, RabbitMQ, and optionally the API container

---

## Core concepts

*Planned sections:*

- `postgres` service definition
- Environment variables for DB user/password/database name
- Port `5432:5432`
- Named volume for data persistence
- `docker compose up -d`, `ps`, `down`, `logs`

---

## Examples (cashback platform)

*Planned examples:*

- Minimal `docker-compose.yml` for PostgreSQL only
- Connection string matching compose env vars

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
| [03-postgresql-sqlalchemy.md](./03-postgresql-sqlalchemy.md) | App connects to composed DB |
| [08-environment-config.md](./08-environment-config.md) | `DATABASE_URL` points at container |

---

## Implementation reference

See [checklist.md](../checklist.md) — Phase B.
