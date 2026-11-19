# AI Assistant Context — BigCity AI Operations & Knowledge Intelligence Platform

## IMPORTANT — SOURCE OF TRUTH

This document is the **frozen project context** for this repository.

It is an **UPDATE** to project requirements — not a request to rebuild or restart.

* Inspect the repository before implementing.
* Preserve working code; evolve incrementally.
* Do **not** delete, reset, or restart existing implementations that already work.
* Do **not** use older “Internal Knowledge Hub”, Department-based, or HR/public-enterprise assumptions.

Progress tracking lives in: `docs/PROJECT_PROGRESS.md`

If code and this document appear to conflict:

1. Inspect the actual implementation first.
2. Do not blindly delete working code.
3. Identify the conflict, propose the smallest safe change, and wait for approval.

---

# 1. Project Name

**BigCity AI Operations & Knowledge Intelligence Platform**

Business domain: Consumer Cashback + Campaign Operations

---

# 2. Project Purpose

Internal AI-powered platform for BigCity Promotions that combines:

1. Structured business data
2. Enterprise documents
3. Campaign rules
4. Cashback and reward information
5. Transaction data
6. AI-powered retrieval and reasoning

Goals: help internal teams investigate business and technical problems using PostgreSQL, S3, ChromaDB, hybrid search, reranking, LangGraph, LLM reasoning, and grounded citations.

This is **not**:

* A generic HR knowledge base
* A public enterprise knowledge portal
* A demo FAQ chatbot

It is specifically for BigCity internal:

* Campaign operations
* Cashback operations
* Customer support investigation
* Engineering troubleshooting
* Enterprise knowledge

---

# 3. Primary Internal Users (Frozen Roles)

## ADMIN

Full platform administration: users, roles, documents, campaigns, access control, monitoring.

## CAMPAIGN_OPERATIONS

Campaign/business operations: campaign config, eligibility, rules, reward conditions.

Example: “What are the eligibility conditions for this cashback campaign?”

## SUPPORT

Customer/program support: cashback issues, transactions, rewards, combining structured data with rules.

Example: “Why was this customer's cashback not credited?”

## ENGINEER

Engineering/technical: docs, APIs, failures, cashback processing, AI/RAG infrastructure.

Example: “What happens when purchase validation fails?”

---

# 4. Frozen Role Set

Exact initial roles:

```text
ADMIN
CAMPAIGN_OPERATIONS
SUPPORT
ENGINEER
```

Do **not** introduce alternate roles (SUPER_ADMIN, EMPLOYEE, DEPARTMENT_MANAGER, KNOWLEDGE_MANAGER, etc.) unless architecture is explicitly revised.

---

# 5. Out of Scope — Do Not Introduce

```text
Department
KnowledgeCategory
DocumentAccess
DocumentEmbedding
DocumentChunk
ProcessingJob
ChatSession
ChatMessage
Feedback
```

No Department domain in the frozen architecture.

---

# 6. Frozen Database Domain

Primary entities:

```text
User
Role

Document
DocumentVersion
IngestionJob

Campaign
CampaignRule

Customer
Transaction
Reward
```

High-level relationships:

```text
Role
  ↓
User
```

```text
Document
  ↓
DocumentVersion
  ↓
IngestionJob
```

```text
Campaign
  ↓
CampaignRule
  ↓
Transaction
  ↓
Reward
```

Customer data supports transaction investigation. Exact FKs must follow frozen architecture and be reviewed before new dependencies.

---

# 7. Implementation Order

## Phase 1 — Foundation (preserve; do not recreate)

Already implemented:

* FastAPI, Python 3.12, PostgreSQL
* SQLAlchemy 2.x, Declarative Base, production base/mixins
* Database session, `DATABASE_URL`, Alembic + env
* Migrations, DB health check, global exception framework

## Phase 2 — Identity

### Role (finish completely before User)

Lifecycle:

```text
Model → Migration → Schemas → Repository → Service → Exceptions
  → CRUD API → Tests → Logging → Seed Data
```

### User (after Role is stable)

```text
User Model → Migration → Schemas → Repository → Service
  → Exceptions → CRUD API → Tests → Authentication → Authorization → RBAC
```

Do not implement User before Role is complete (including seed of the four frozen roles).

## Later phases (dependency order)

```text
Document → DocumentVersion → IngestionJob
  → Campaign → CampaignRule
  → Customer → Transaction → Reward
  → Production RAG → LangGraph → LLMOps → Deployment
```

---

# 8. Knowledge / Document Domain

After Identity:

```text
Document → DocumentVersion → IngestionJob
```

Support: metadata, lifecycle, versioning, S3, hashing, duplicate detection, ingestion status, processing metadata.

Target ingestion pipeline:

```text
Upload → S3 → Document → DocumentVersion → IngestionJob
  → Extraction → Hash / Duplicate Detection → Chunking
  → Embedding → ChromaDB
```

---

# 9. Campaign Domain

```text
Campaign → CampaignRule
```

Support campaign configuration, status, dates, eligibility, cashback/reward rules, purchase validation. Model rules in `CampaignRule`, not in API endpoints.

---

# 10. Customer / Transaction / Reward Domain

Operational investigation:

```text
Customer + Transaction + Campaign + CampaignRule + Reward + Knowledge
  → AI Investigation → Grounded Explanation
```

---

# 11–12. AI / RAG Architecture

Prototype RAG under `app/ai/rag/` (e.g. `chunk.py`, `embed.py`, `search.py`):

* Keep as learning/reference baseline
* Do **not** delete
* Not final production architecture

Production target:

```text
Upload → S3 → PostgreSQL metadata → DocumentVersion → IngestionJob
  → Extraction → Semantic chunking → Embeddings → ChromaDB
  → Hybrid retrieval → Reranking → Context assembly
  → LangGraph → LLM → Grounded answer → Citations
```

Must support: metadata-aware retrieval, RBAC, version awareness, source attribution, filtering, reranking, context limits, hallucination reduction.

---

# 13. LLM

Current: **Google Gemini 2.5 Flash**

Keep provider configurable for later OpenAI/open-source swaps. Do not switch models without a specific reason.

---

# 14. Embeddings

Prototype: `sentence-transformers/all-MiniLM-L6-v2` — acceptable for learning/baseline.

Production later: config, version tracking, dimension validation, batching, persistence, re-indexing. Do not change the model until production retrieval is ready.

---

# 15. Vector Database

Production target: **ChromaDB**

FAISS = prototype/local learning only. Do not build production around rebuilding an in-memory FAISS index.

---

# 16. LangGraph

Orchestration later (do not introduce multi-agent complexity early). Potential agents: Knowledge, Campaign, Transaction Investigation — after reliable retrieval and structured-data access exist.

---

# 17. LLMOps Roadmap (after core platform)

Prompt/model/embedding/chunking/retrieval config tracking; AI request, token, and latency logging; RAG/retrieval/answer evaluation; observability.

---

# 18. Infrastructure Roadmap

Docker, Compose, PostgreSQL, Redis, S3, RDS, ECS/EC2, GitHub Actions / CI/CD.

Redis later: cache, job status, rate limits. Background jobs later: ingestion, OCR, embeddings, indexing.

Add infrastructure only when it serves a real requirement.

---

# 19. Production Coding Approach

Per entity:

```text
1. Inspect architecture/dependencies
2. SQLAlchemy Model
3. Alembic Migration
4. Pydantic Schemas
5. Repository (+ count/list/pagination where applicable)
6. Service
7. Domain Exceptions
8. CRUD API
9. Tests
10. Logging
11. Seed Data if required
12. Docs / health considerations
```

Use: SQLAlchemy 2.x, Pydantic v2, type hints, DI, repository + service patterns, thin routers, explicit exceptions, transaction boundaries, production validation.

---

# 20. Existing Database Structure (actual)

```text
app/db/base.py
app/db/session.py
app/db/models/          # includes mixins.py
app/db/migrations/
app/repositories/       # established location — do not move without approval
```

Do **not** invent a second repository path or move files without a compelling reason.

Architecture layering:

```text
API → Service → Repository → Database
```

Business logic only in Services; persistence only in Repositories; routers stay thin.

---

# 21. Alembic

* Uses `settings.DATABASE_URL`
* Metadata: `Base.metadata`
* Models imported for autogenerate discovery
* Role migration applied: `ceb1f25f7b58_create_roles_table`
* Never modify an already-applied migration; create a new one for schema changes

---

# 22. Database Health Check

Existing health endpoint returns connected status when healthy. Reuse for Docker/AWS readiness — do not replace with ad-hoc raw DB test endpoints.

---

# 23. Technology Stack

## Backend

* Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL, Pydantic v2
* JWT/RBAC after User

## AI

* Gemini 2.5 Flash, sentence-transformers (prototype OK), ChromaDB (production target), LangGraph later

## Infra later

* Docker Compose, Redis, S3, RDS, ECS/EC2, GitHub Actions

---

# 24. How Cursor Should Work

Before any feature:

1. Inspect repo, frozen architecture, dependencies, migrations, existing patterns.
2. Reuse abstractions; no duplicate implementations.
3. No new tables without architectural justification.
4. No unnecessary renames/moves.

For each requested task, briefly explain: what / why / files / dependencies / migration needed / tests — then implement.

After implementation: files changed, commands, tests, expected result, follow-up.

---

# Teach-First Learning Mode (Mandatory)

The user must **fully understand** every step. Do not dump finished code and move on.

For each step:

1. **Explain first** — what, why, which layer, how it fits.
2. **Break it down** — one concept/file at a time.
3. **Show code with commentary**.
4. **Hand off execution** — exact commands for the user.
5. **Wait for confirmation** — do not mark done until the user confirms.
6. **Then update progress** — only after confirmation, update `docs/PROJECT_PROGRESS.md`.

Prefer guided implementation over silent bulk edits.

---

# Session Rules (Mandatory)

1. **One step only** per response unless the user explicitly asks for more.
2. **Teach first** — follow Teach-First Learning Mode.
3. After every completed step (user confirmed), update `docs/PROJECT_PROGRESS.md`.
4. Do not start the next entity until the current entity lifecycle is complete.
5. Do not touch production RAG / S3 / OCR / LangGraph until Identity (Role → User) is complete, unless the user explicitly overrides.
6. Always report: current entity, step, entity %, overall %, next single step title.
7. End implementation replies with a **User action checklist**. Do not mark complete until the user confirms.

---

# Generic Progress Prompts

## A) Start / Continue Work (default)

```text
Follow docs/AI_AGENT_CONTEXT.md as source of truth.
Read docs/PROJECT_PROGRESS.md for current status.
One step only. Do not skip lifecycle steps.
Do not start the next entity early.
Do not introduce Department or out-of-scope entities.
Teach-first: explain what we will implement and why, then guide me one piece at a time.
I will run the commands and tests myself — give me exact commands and what success looks like.
Do not mark the step complete or update progress until I confirm I ran/tested it.
Implement / guide the CURRENT NEXT STEP only.
```

## B) Update Progress Only (no code)

```text
Read docs/AI_AGENT_CONTEXT.md and docs/PROJECT_PROGRESS.md.
I just completed: <entity> — <step name>.
Update PROJECT_PROGRESS.md checklists and percentages to match reality.
Do not write application code.
Confirm: entity %, overall %, and the next single step.
```

## C) View Progress Only

```text
Read docs/AI_AGENT_CONTEXT.md and docs/PROJECT_PROGRESS.md.
Show current progress only:
- Current entity + step
- Entity checklist
- Overall %
- Hours used / remaining (if tracked)
- Next single step
No code changes.
```

## D) End of Step (after YOU verified)

```text
Step done: <entity> — <step name>.
I ran the commands/tests and understand the change.
Update docs/PROJECT_PROGRESS.md.
Give only:
1) what changed (1–3 bullets)
2) entity % and overall %
3) next single step title
Do not implement the next step yet.
```

## E) Explain Only (no code yet)

```text
Follow docs/AI_AGENT_CONTEXT.md.
Read docs/PROJECT_PROGRESS.md.
Explain the CURRENT NEXT STEP only:
- what / why / where in the architecture
- files we will touch
- design choices and trade-offs
- exact commands I will run to verify
Do not write or edit application code yet. Wait for me to say "implement".
```

---

# Current Snapshot (keep in sync with PROJECT_PROGRESS.md)

* **Project:** BigCity AI Operations & Knowledge Intelligence Platform
* **Phase:** Identity — Authentication
* **Current entity:** User (CRUD ✅)
* **Current step:** Authentication (JWT)
* **Role progress:** 100%
* **User CRUD progress:** 100%
* **Identity domain:** ~85% (Auth/RBAC pending)
* **Overall progress:** ~27%
* **Next step:** Authentication (JWT)
* **Blocked on:** none
* **Out of scope:** Department and other entities listed in §5
* **After JWT:** Authorization → RBAC
