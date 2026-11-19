# Topic 6 — RBAC (Role-Based Access Control)

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Planned |
| **Prerequisites** | [05-jwt-authentication.md](./05-jwt-authentication.md) |
| **Next topic** | [07-docker-compose.md](./07-docker-compose.md) |

---

## Summary

*To be expanded during study session.*

**RBAC** restricts API actions based on user **roles** (e.g. `user` vs `admin`). Week 1 introduces the `role` field; admin-only routes expand in Month 3.

---

## Definition

*Planned sections: role, permission, authorization vs authentication, least privilege.*

---

## Why it matters in this project

- Regular users submit transactions and redeem rewards
- Admins review fraud flags, manage campaigns, view analytics
- Correct `401` / `403` responses clarify security behavior for API consumers

---

## Core concepts

*Planned sections:*

- `role` enum on `User` model (`user`, `admin`)
- `require_admin` dependency wrapping `get_current_user`
- Default role on registration: `user`
- Seeding an admin user for local dev (optional)

---

## Examples (cashback platform)

*Planned examples:*

- `GET /users/me` — any authenticated user
- `GET /admin/users` — admin only → `403` for `user` role

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
| [05-jwt-authentication.md](./05-jwt-authentication.md) | Identity before role check |
| [02-fastapi.md](./02-fastapi.md) | Dependencies enforce roles |

---

## Implementation reference

See [checklist.md](../checklist.md) — Phase C (light touch).
