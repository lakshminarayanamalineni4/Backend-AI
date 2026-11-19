# Project Progress — BigCity AI Operations & Knowledge Intelligence Platform

> Source of truth for architecture & rules: `docs/AI_AGENT_CONTEXT.md`  
> This file tracks **what is done**, **percentages**, and **the next step only**.

Last updated: 2026-07-26 (User CRUD lifecycle complete — docs done; seed skipped)

---

## Sprint Clock (15-hour target)

| Field | Value |
|-------|-------|
| Hours used | 5.5 / 15 |
| Hours remaining | 9.5 |
| Sprint goal | User (Identity) → Auth |
| Status | 🟡 In Progress |

---

## Scoreboard

| Metric | Value |
|--------|-------|
| Current entity | **User** (CRUD lifecycle ✅) |
| Current step | **Authentication (JWT)** (next) |
| Role progress | **100%** |
| User progress | **100%** (CRUD lifecycle 11/11; Auth separate) |
| Identity domain | **~85%** (Role ✅; User CRUD ✅; Auth/RBAC pending) |
| Overall platform | **~27%** |
| Next step | Authentication (JWT) |
| Blocked on | — |

### Overall weight (for % math)

| Domain | Weight | Done | Contribution |
|--------|--------|------|--------------|
| Foundation | 10% | 100% | 10.0 |
| Identity (Role → User → Auth/RBAC) | 20% | ~85% | 17.0 |
| Document domain | 20% | 0% | 0.0 |
| Campaign domain | 15% | 0% | 0.0 |
| Customer / Transaction / Reward | 15% | 0% | 0.0 |
| Production RAG / LangGraph / LLMOps / Deploy | 20% | ~0% (prototype RAG exists, not counted as delivery) | 0.0 |
| **Overall** | **100%** | | **~27%** |

---

## Progress Legend

* ✅ Completed — implemented and verified
* 🟡 In Progress — current work
* ⬜ Not Started
* ⛔ Blocked / out of scope

---

## 1. Foundation

| Item | Status |
|------|--------|
| FastAPI / Python 3.12 | ✅ |
| PostgreSQL | ✅ |
| SQLAlchemy 2.x | ✅ |
| Base ORM / mixins | ✅ |
| Database session / `DATABASE_URL` | ✅ |
| Alembic + env configuration | ✅ |
| Database migrations | ✅ |
| Database health check | ✅ |
| Global exception framework | ✅ |

**Foundation: 100%**

---

## 2. Identity — Role ✅

Lifecycle complete:

| # | Step | Status |
|---|------|--------|
| 1 | SQLAlchemy Model | ✅ |
| 2 | Alembic Migration (`ceb1f25f7b58_create_roles_table`) | ✅ |
| 3 | Pydantic Schemas | ✅ |
| 4 | Repository (+ `count()`) | ✅ |
| 5 | Service | ✅ |
| 6 | Exceptions | ✅ |
| 7 | CRUD API (`/api/v1/roles`) | ✅ |
| 8 | Unit Tests (service — 12 tests) | ✅ |
| 9 | Logging (service + app INFO handler) | ✅ |
| 10 | Module documentation | ✅ |
| 11 | Seed Data (four frozen roles) | ✅ (present in DB via API; dedicated seed script skipped) |

**Role: 100% (11/11)**

### Role files (reference)

* `backend/app/db/models/role.py`
* `backend/app/db/migrations/versions/ceb1f25f7b58_create_roles_table.py`
* `backend/app/schemas/role.py`
* `backend/app/repositories/role_repository.py`
* `backend/app/services/role_service.py`
* `backend/app/core/exceptions/role.py`
* `backend/app/api/routes/role.py` → `/api/v1/roles`
* `backend/tests/unit/services/test_role_service.py`
* `docs/modules/role.md`

---

## 3. Identity — User ✅ (CRUD lifecycle)

| # | Step | Status |
|---|------|--------|
| 1 | SQLAlchemy Model | ✅ |
| 2 | Alembic Migration (`a1b2c3d4e5f6_create_users_table`) | ✅ |
| 3 | Pydantic Schemas | ✅ |
| 4 | Repository (+ `count()`, mobile hash lookup) | ✅ |
| 5 | Service | ✅ |
| 6 | Exceptions | ✅ |
| 7 | CRUD API (`/api/v1/users`) | ✅ |
| 8 | Unit Tests (service — 16 tests) | ✅ |
| 9 | Logging (service) | ✅ |
| 10 | Module documentation | ✅ `docs/modules/user.md` |
| 11 | Seed Data | ✅ Skipped — no frozen user set; create via API |

**User CRUD lifecycle: 100% (11/11)**

### Auth follow-on (Identity — not started)

| Step | Status |
|------|--------|
| Authentication (JWT) | ⬜ **NEXT** |
| Authorization | ⬜ |
| RBAC (role-based route protection) | ⬜ |

Depends on: Role ✅, User CRUD ✅.

### Verified (2026-07-26)

| Capability | Status | Notes |
|------------|--------|-------|
| Model / migration / schemas | ✅ | `users` table; FK to `roles` |
| Mobile PII | ✅ | Fernet encrypt at rest; HMAC hash for filter; decrypt in responses |
| Password hashing | ✅ | bcrypt via `app/core/security.py` |
| Repository CRUD + count | ✅ | `app/repositories/user_repository.py` |
| Service + exceptions | ✅ | email/mobile uniqueness, role FK, not-found |
| CRUD routes mounted | ✅ | create / list (+ mobile filter) / count / get / update / delete |
| Service unit tests | ✅ | 16 passed |
| Logging | ✅ | service logger |
| Module doc | ✅ | `docs/modules/user.md` |
| JWT / RBAC | ⬜ | next |

### User files (reference)

* `backend/app/db/models/user.py`
* `backend/app/db/migrations/versions/a1b2c3d4e5f6_create_users_table.py`
* `backend/app/schemas/user.py`
* `backend/app/repositories/user_repository.py`
* `backend/app/services/user_service.py`
* `backend/app/core/exceptions/user.py`
* `backend/app/core/security.py`
* `backend/app/api/routes/user.py` → `/api/v1/users`
* `backend/tests/conftest.py`
* `backend/tests/unit/services/test_user_service.py`
* `docs/modules/user.md`

---

## 4. Document Domain

| Entity | Status |
|--------|--------|
| Document | ⬜ |
| DocumentVersion | ⬜ |
| IngestionJob | ⬜ |

**Documents: 0%**

---

## 5. Campaign Domain

| Entity | Status |
|--------|--------|
| Campaign | ⬜ |
| CampaignRule | ⬜ |

**Campaign: 0%**

---

## 6. Customer / Transaction / Reward

| Entity | Status |
|--------|--------|
| Customer | ⬜ |
| Transaction | ⬜ |
| Reward | ⬜ |

**Ops investigation domain: 0%**

---

## 7. AI Pipeline (production)

| Step | Status |
|------|--------|
| Prototype RAG (`app/ai/rag/`) | ✅ Exists — reference only |
| Production S3 pipeline | ⬜ |
| Production chunking / embeddings | ⬜ |
| ChromaDB | ⬜ |
| Hybrid retrieval / reranking | ⬜ |
| Access-controlled retrieval | ⬜ |
| LangGraph | ⬜ |
| LLMOps | ⬜ |
| Production deployment | ⬜ |

**Production AI: 0% delivery** — do not start until Identity (Role → User → Auth/RBAC) is complete, unless explicitly overridden.

---

## Out of scope (do not implement)

Frozen architecture excludes:

* Department
* KnowledgeCategory, DocumentAccess, DocumentEmbedding, DocumentChunk
* ProcessingJob, ChatSession, ChatMessage, Feedback
* Alternate role sets (EMPLOYEE, SUPER_ADMIN, etc.)

Previous learning-phase corpora / FAISS tutorial path remain study references only — not delivery criteria.

---

## Step Log

| Date | Entity | Step | Notes |
|------|--------|------|-------|
| 2026-07-25 | Role | 1–7 | Model → Migration → Schemas → Repo → Service → Exceptions → CRUD API |
| 2026-07-25 | Role | 8 | Unit tests: 12 passed (SQLite in-memory + pytest) |
| 2026-07-25 | Role | 9 | Service logging + app INFO handler in `main.py` |
| 2026-07-25 | Role | 10 | Module doc: `docs/modules/role.md` |
| 2026-07-25 | Docs | — | Context updated to frozen BigCity AI Ops platform; Department removed from plan |
| 2026-07-25 | Role | 11 | Four frozen roles present in DB (API); seed script skipped — Role complete |
| 2026-07-26 | User | 1–7 | Model → Migration → Schemas → Repo → Service → Exceptions → CRUD API (+ mobile encrypt/hash) |
| 2026-07-26 | User | 8 | Unit tests: 16 passed |
| 2026-07-26 | User | 9 | Service logging verified |
| 2026-07-26 | User | 10–11 | Module doc `docs/modules/user.md`; seed skipped — User CRUD lifecycle complete |

---

## How to update this file after each step

1. Mark the finished step ✅
2. Move 🟡 to the next step
3. Recalculate entity % = completed_steps / total_steps × 100
4. Recalculate Overall using the weight table
5. Append a row to **Step Log**
6. Optionally bump **Hours used**

Use prompts in `docs/AI_AGENT_CONTEXT.md` → **Generic Progress Prompts** (sections A–E).
