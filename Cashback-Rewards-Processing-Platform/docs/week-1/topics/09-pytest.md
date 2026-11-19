# Topic 9 — Pytest

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Planned |
| **Prerequisites** | [01-rest-apis.md](./01-rest-apis.md), [02-fastapi.md](./02-fastapi.md) |
| **Next topic** | Month 1 — transactions, CI |

---

## Summary

*To be expanded during study session.*

**Pytest** is the test runner for the FastAPI backend. Week 1 tests verify auth endpoints return correct status codes and JSON, forming the base for the 80%+ coverage goal by Phase 3.

---

## Definition

*Planned sections: test function, fixture, assertion, test client, integration vs unit test, coverage.*

---

## Why it matters in this project

- Proves register/login/protected routes work after every change
- GitHub Actions CI will run `pytest` on each push (Month 1)
- Interview narrative: production-grade backends are tested, not only manual `/docs` clicks

---

## Core concepts

*Planned sections:*

- `TestClient` from FastAPI / `httpx`
- `conftest.py` fixtures: `db`, `client`, `auth_headers`
- Test database strategy (SQLite in-memory or separate Postgres DB)
- Asserting `response.status_code` and `response.json()`
- Running `pytest -v` and `pytest --cov`

---

## Examples (cashback platform)

*Planned examples:*

- `test_register_success` → `201`
- `test_register_duplicate_email` → `400`
- `test_login_invalid_password` → `401`
- `test_users_me_requires_auth` → `401`
- `test_users_me_with_token` → `200`

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
| [01-rest-apis.md](./01-rest-apis.md) | Tests assert REST contracts |
| [05-jwt-authentication.md](./05-jwt-authentication.md) | Auth flow under test |

---

## Implementation reference

See [checklist.md](../checklist.md) — Phase D.
