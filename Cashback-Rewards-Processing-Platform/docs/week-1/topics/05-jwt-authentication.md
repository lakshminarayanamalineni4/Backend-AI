# Topic 5 — JWT Authentication

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Planned |
| **Prerequisites** | [01-rest-apis.md](./01-rest-apis.md), [02-fastapi.md](./02-fastapi.md) |
| **Next topic** | [06-rbac.md](./06-rbac.md) |

---

## Summary

*To be expanded during study session.*

**JSON Web Tokens (JWT)** provide stateless authentication. After login, the client sends a signed access token on each request; the server verifies the signature and expiry without storing sessions.

---

## Definition

*Planned sections: access token, refresh token, claims, signing (HS256), expiry, Bearer scheme, bcrypt password hashing.*

---

## Why it matters in this project

- Core Week 1 deliverable: register, login, protected `/users/me`
- Angular JWT interceptor will attach tokens to API calls
- Refresh tokens allow re-issuing access tokens without re-entering password

---

## Core concepts

*Planned sections:*

- Register: hash password with bcrypt, store hash only
- Login: verify password, issue tokens
- Access token: short-lived, used on API calls
- Refresh token: longer-lived, used at `POST /auth/refresh`
- `Authorization: Bearer <token>` header
- FastAPI `OAuth2PasswordBearer` or custom dependency

---

## Examples (cashback platform)

*Planned examples:*

- Token payload: `sub` (user id), `exp`, optional `role`
- Login response shape
- Verifying token in `get_current_user`

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
| [01-rest-apis.md](./01-rest-apis.md) | Bearer header on protected routes |
| [06-rbac.md](./06-rbac.md) | Role claim in token or DB lookup |
| [08-environment-config.md](./08-environment-config.md) | `JWT_SECRET` must stay secret |

---

## Implementation reference

See [checklist.md](../checklist.md) — Phase C.
