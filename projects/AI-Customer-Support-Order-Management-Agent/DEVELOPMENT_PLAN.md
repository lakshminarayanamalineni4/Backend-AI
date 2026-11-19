# Development Plan — AI Customer Support & Order Management Agent

**Target:** Nestlé-style e-commerce customer support  
**Approach:** Infra first → backend modules → Chainlit chat UI → React last  
**Deploy:** After every module (GitHub Actions → AWS EC2)  
**Docs storage:** AWS S3 from day one  

Flip `- [ ]` to `- [x]` when a feature is done. Do not start the next feature until the current one's **Done when** is met. Finish a module (and deploy it) before starting the next.

---

## Constraints

| Decision          | Choice                |
|-------------------|-----------------------|
| Pre-React chat UI | **Chainlit**          |
| Final UI          | React (Module 9 only) |
| Host              | AWS EC2               |
| Policy documents  | AWS S3                |
| CI/CD             | GitHub Actions        |
| Containers        | Docker + Compose      |
| Deploy cadence    | After each module     |

---

## Stack

| Layer           | Choice                                  |
|-----------------|-----------------------------------------|
| API             | FastAPI, Pydantic                       |
| Temp chat UI    | Chainlit                                |
| Final UI        | React (Module 9)                        |
| Database        | PostgreSQL                              |
| Docs storage    | Amazon S3                               |
| Vectors         | ChromaDB (Pinecone optional later)      |
| Embeddings      | Sentence Transformers                   |
| LLM             | Gemini, OpenAI, or suitable open-source |
| Agent           | LangGraph + LangChain                   |
| Cache / session | Redis (Module 7)                        |
| Queue           | RabbitMQ (Module 7)                     |
| Auth            | JWT + RBAC                              |
| Observability   | OpenTelemetry, CloudWatch, LangSmith    |
| Testing         | Pytest                                  |

---

## Deploy-on-module flow

```text
Feature work locally
  → PR → GitHub Actions (test + build image)
  → Merge → CD deploys to EC2
  → Smoke check (/health + module-specific check)
  → Mark module done → start next module
```

**Advance only when:**
1. All features in the current module are checked (or explicitly deferred with a note).
2. The module's main journey/demo works manually on EC2.
3. At least one automated test exists for that module's happy path.

---

## Critical path

```text
M0 Docker + CI/CD + EC2 + S3 + first deploy
 → M1 Foundation (+ deploy)
 → M2 LLM + Chainlit (+ deploy)
 → M3 RAG from S3 (+ deploy)
 → M4 Tools (+ deploy)
 → M5 Agent routing / tracking (+ deploy)
 → M6 Cancel/refund/escalate workflows (+ deploy)
 → M7 Redis/RabbitMQ/tests (+ deploy)
 → M8 Production hardening (+ deploy)
 → M9 React UI (+ deploy)   ← only after backend is done
```

---

## Module 0 — Platform bootstrap

**Goal:** Empty app that deploys to AWS on every merge.

| #   | Feature                                              | Done when                                             |
|-----|------------------------------------------------------|-------------------------------------------------------|
| 0.1 | Project skeleton (FastAPI + folders)                 | Runnable `GET /health`                                |
| 0.2 | Dockerfile + docker-compose (app + Postgres)         | Local `docker compose up` works                       |
| 0.3 | GitHub Actions: lint/test/build image                | CI green on PR                                        |
| 0.4 | AWS: EC2 + security group + SSH/deploy user          | Instance reachable                                    |
| 0.5 | AWS: S3 bucket for knowledge docs                    | Bucket + IAM role/policy ready                        |
| 0.6 | Deploy pipeline: push image → pull on EC2 → restart  | `/health` live on EC2                                 |
| 0.7 | Module-based deploy convention                       | Tag/env or branch strategy so each module can ship    |

### Progress — Module 0

- [ ] 0.1 Skeleton
- [ ] 0.2 Docker
- [ ] 0.3 GitHub Actions CI
- [ ] 0.4 EC2 setup
- [ ] 0.5 S3 setup
- [ ] 0.6 Deploy CD
- [ ] 0.7 Module deploy convention

**Smoke after deploy:** `GET /health` returns 200 on EC2.

---

## Module 1 — Foundation

**Goal:** Secure identity and persistence before any AI.

| #   | Feature                                                    | Done when                                   |
|-----|------------------------------------------------------------|---------------------------------------------|
| 1.1 | PostgreSQL models (users, roles, conversations, messages)  | Migrations apply cleanly                    |
| 1.2 | JWT auth (register/login/refresh)                          | Protected routes reject invalid tokens      |
| 1.3 | Basic RBAC stubs (customer / support / manager / admin)    | Role check works                            |
| 1.4 | Conversation CRUD APIs                                     | Create conversation, append messages        |
| 1.5 | Config & secrets (env-based)                               | No secrets in code                          |

### Progress — Module 1

- [ ] 1.1 Models + migrations
- [ ] 1.2 JWT auth
- [ ] 1.3 RBAC stubs
- [ ] 1.4 Conversation APIs
- [ ] 1.5 Config/secrets
- [ ] Deploy Module 1

**Smoke after deploy:** Register/login works against EC2 API.

---

## Module 2 — Chat (LLM) + Chainlit UI

**Goal:** Chat that replies with an LLM, stores history, and uses Chainlit (not React).

| #   | Feature                         | Done when                                            |
|-----|---------------------------------|------------------------------------------------------|
| 2.1 | Chat API endpoint               | Messages persist in Postgres                         |
| 2.2 | LLM provider integration        | Generic Q&A works                                    |
| 2.3 | Conversation state load/save    | Multi-turn context works                             |
| 2.4 | Chainlit chat UI                | Logged-in (or session) user can chat                 |
| 2.5 | Guardrails system prompt        | “Don’t invent order/refund data” enforced in prompt  |

### Progress — Module 2

- [ ] 2.1 Chat API
- [ ] 2.2 LLM wiring
- [ ] 2.3 Session state
- [ ] 2.4 Chainlit UI
- [ ] 2.5 Safety prompt baseline
- [ ] Deploy Module 2

**Smoke after deploy:** Send a message in Chainlit on EC2; reply + history persist.

---

## Module 3 — Knowledge Base & RAG (S3)

**Goal:** Policy answers grounded in enterprise docs stored in S3.

| #   | Feature                                   | Done when                                                                            |
|-----|-------------------------------------------|--------------------------------------------------------------------------------------|
| 3.1 | Sample policy docs uploaded to S3         | Return, refund, cancel, shipping, delivery, payment, product FAQ, support guidelines |
| 3.2 | Ingestion: PDF/DOCX extract + clean       | Text extracted with metadata                                                         |
| 3.3 | Chunking + embeddings                     | Chunks stored with source IDs                                                        |
| 3.4 | ChromaDB vector store + similarity search | Query returns relevant chunks                                                        |
| 3.5 | RAG answer path in chat                   | FAQ answers cite sources; no hallucinated policies                                   |
| 3.6 | OCR for scanned PDFs (optional)           | Deferred until core RAG works                                                        |

### Progress — Module 3

- [ ] 3.1 Policy corpus in S3
- [ ] 3.2 Ingestion pipeline
- [ ] 3.3 Chunk + embed
- [ ] 3.4 Vector search
- [ ] 3.5 RAG in chat
- [ ] 3.6 OCR (optional / deferred)
- [ ] Deploy Module 3

**Smoke after deploy:** Ask refund policy question; answer cites a source document.

---

## Module 4 — External Tools / Mock APIs

**Goal:** Deterministic order/refund/ticket services the agent can call.

| #   | Feature                                                  | Done when                                    |
|-----|----------------------------------------------------------|----------------------------------------------|
| 4.1 | `get_order_status` / `get_order_details`                 | Known order IDs return status                |
| 4.2 | `check_cancellation_eligibility` + `cancel_order`        | Eligibility + cancel with idempotency key    |
| 4.3 | `check_refund_eligibility` + `calculate_refund_amount`   | Amount rules match sample policy             |
| 4.4 | `create_refund` + `get_refund_status`                    | Refund created; status queryable             |
| 4.5 | `create_support_ticket`                                  | Ticket linked to customer + conversation     |
| 4.6 | Timeouts, retries, error shapes                          | Failed API returns safe, typed errors        |

### Progress — Module 4

- [ ] 4.1 Order read tools
- [ ] 4.2 Cancellation tools
- [ ] 4.3 Refund eligibility/amount
- [ ] 4.4 Refund create/status
- [ ] 4.5 Support ticket tool
- [ ] 4.6 Failure handling
- [ ] Deploy Module 4

**Smoke after deploy:** Call order-status API for a known test order ID.

---

## Module 5 — Agent routing (tools + RAG)

**Goal:** Agent chooses RAG vs tools vs escalate; never invents transactional data.

| #   | Feature                                  | Done when                                       |
|-----|------------------------------------------|-------------------------------------------------|
| 5.1 | Intent classification / router           | Tracks intent → order tool; policy → RAG        |
| 5.2 | Tool registry + schemas (Pydantic)       | LLM can only call allowlisted tools             |
| 5.3 | Tool-result validation before reply      | Bad/empty results not shown as facts            |
| 5.4 | Journey 7.1: Order tracking E2E          | “Where is my order?” works end-to-end           |
| 5.5 | Escalation path for out-of-scope         | Unsupported ask → ticket tool                   |

### Progress — Module 5

- [ ] 5.1 Router
- [ ] 5.2 Tool schemas
- [ ] 5.3 Result validation
- [ ] 5.4 Order tracking E2E
- [ ] 5.5 Basic escalation
- [ ] Deploy Module 5

**Smoke after deploy:** Order tracking journey works in Chainlit on EC2.

---

## Module 6 — LangGraph workflows + human confirmation

**Goal:** Multi-step cancel/refund with explicit customer confirmation.

| #   | Feature                                       | Done when                                                              |
|-----|-----------------------------------------------|------------------------------------------------------------------------|
| 6.1 | LangGraph state machine                       | Graph checkpoints mid-flow                                             |
| 6.2 | Cancellation workflow (Journey 7.2)           | Confirm required before `cancel_order`                                 |
| 6.3 | Refund workflow (Journey 7.3)                 | RAG policy + eligibility + amount + confirm before `create_refund`     |
| 6.4 | Human escalation workflow (Journey 7.4)       | Dispute/fraud/exception → ticket                                       |
| 6.5 | Idempotency for cancel/refund                 | Duplicate confirm doesn’t double-apply                                 |
| 6.6 | Audit log of tool calls + decisions           | Every impacting action is queryable                                    |

### Progress — Module 6

- [ ] 6.1 LangGraph state
- [ ] 6.2 Cancel + confirm
- [ ] 6.3 Refund + confirm
- [ ] 6.4 Escalation journey
- [ ] 6.5 Idempotency
- [ ] 6.6 Audit logging
- [ ] Deploy Module 6

**Smoke after deploy:** Cancel and refund journeys require confirmation; escalate creates a ticket.

---

## Module 7 — Backend hardening

**Goal:** Async, cache, fuller tests matching NFRs.

| #   | Feature                                              | Done when                                       |
|-----|------------------------------------------------------|-------------------------------------------------|
| 7.1 | Redis for session/graph checkpoints                  | Restart doesn’t lose mid-confirmation           |
| 7.2 | RabbitMQ + worker for long ops                       | Refund/cancel can run async                     |
| 7.3 | Full Docker Compose (app, db, redis, mq, chroma)     | One-command local stack                         |
| 7.4 | Unit + integration + API tests                       | Pytest covers auth, RAG, tools, workflows       |
| 7.5 | E2E tests for 4 journeys                             | Tracking, cancel, refund, escalate              |
| 7.6 | Observability baseline                               | Traces/logs wired for deploy                    |

### Progress — Module 7

- [ ] 7.1 Redis state
- [ ] 7.2 RabbitMQ workers
- [ ] 7.3 Full Docker stack
- [ ] 7.4 Automated tests
- [ ] 7.5 Journey E2E
- [ ] 7.6 Observability baseline
- [ ] Deploy Module 7

**Smoke after deploy:** Full stack healthy; mid-confirmation survives app restart.

---

## Module 8 — Production hardening (backend)

**Goal:** Deployable, observable, role-complete backend (still Chainlit UI).

| #   | Feature                                               | Done when                                            |
|-----|-------------------------------------------------------|------------------------------------------------------|
| 8.1 | Full RBAC (customer / support / manager / admin)      | Role-gated APIs                                      |
| 8.2 | OpenTelemetry + CloudWatch                            | Traces span message → RAG → tools → reply            |
| 8.3 | LangSmith (or equiv.) for AI eval                     | Sample traces/evals visible                          |
| 8.4 | CI/CD hardening                                       | Test + build + deploy pipeline solid                 |
| 8.5 | PII/payment data protection review                    | Secrets, masking, least privilege                    |
| 8.6 | Audit completeness                                    | Customer-impacting actions fully auditable           |

### Progress — Module 8

- [ ] 8.1 Full RBAC
- [ ] 8.2 Observability
- [ ] 8.3 AI tracing/eval
- [ ] 8.4 CI/CD hardening
- [ ] 8.5 Security hardening
- [ ] 8.6 Audit completeness
- [ ] Deploy Module 8

**Smoke after deploy:** Role checks, traces, and audit logs verified on EC2.

---

## Module 9 — React UI (last)

**Goal:** Replace Chainlit with React chat; same backend APIs.

| #   | Feature                               | Done when                                       |
|-----|---------------------------------------|-------------------------------------------------|
| 9.1 | React chat UI                         | Send/receive messages                           |
| 9.2 | Auth + conversation wiring            | Uses Module 1–2 APIs                            |
| 9.3 | Confirmation UX for cancel/refund     | Matches Module 6 flows                          |
| 9.4 | Deploy frontend                       | Served (nginx on EC2 or S3+CloudFront)          |
| 9.5 | Retire Chainlit (optional)            | Chainlit removed or kept for internal demo      |

### Progress — Module 9

- [ ] 9.1 React chat UI
- [ ] 9.2 Auth + conversation wiring
- [ ] 9.3 Confirmation UX
- [ ] 9.4 Deploy frontend
- [ ] 9.5 Retire Chainlit (optional)

**Smoke after deploy:** All four journeys work through React.

---

## Example customer journeys (acceptance)

| Journey                | Module | Behaviour                                                                    |
|------------------------|--------|------------------------------------------------------------------------------|
| 7.1 Order tracking     | 5      | Identify order → order-status API → status + delivery info                   |
| 7.2 Order cancellation | 6      | Eligibility → explain → **explicit confirm** → cancel API                    |
| 7.3 Simple refund      | 6      | Order details → RAG policy → eligibility → amount → **confirm** → refund API |
| 7.4 Human escalation   | 6      | Complex/risky/unsupported → support ticket                                   |

---

## Required external tools (Module 4+)

- `get_order_status(order_id)`
- `get_order_details(order_id)`
- `check_cancellation_eligibility(order_id)`
- `cancel_order(order_id)`
- `check_refund_eligibility(order_id)`
- `calculate_refund_amount(order_id)`
- `create_refund(order_id, amount, reason)`
- `get_refund_status(refund_id)`
- `create_support_ticket(customer_id, conversation_id, reason)`

---

## Source requirement

See `Autonomous_Customer_Support_Refund_Agent_Requirement.docx` in this repository for the full enterprise requirement document.
