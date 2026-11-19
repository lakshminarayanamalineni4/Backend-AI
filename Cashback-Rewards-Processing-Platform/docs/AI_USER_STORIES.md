# AI User Stories — BigCity Ops Knowledge Intelligence

> **Purpose:** Real-world tasks that drive GenAI / RAG / agent learning (Track B).  
> **Architecture source of truth:** `docs/AI_AGENT_CONTEXT.md`  
> **Progress:** `docs/PROJECT_PROGRESS.md`  
> **Status:** Learning requirements (Track B). Does **not** replace Identity → Document delivery order unless explicitly overridden.

These stories make requirements concrete: who asks, what they ask, what “good” looks like, and what must fail safely.

---

## Actors (frozen roles)

| Role                  | Typical AI use                                        |
|-----------------------|-------------------------------------------------------|
| `SUPPORT`             | Customer cashback questions, txn investigation        |
| `CAMPAIGN_OPERATIONS` | Eligibility, campaign rules, reward conditions        |
| `ENGINEER`            | Processing failures, RAG/API troubleshooting docs     |
| `ADMIN`               | Full access; monitoring / config (later)              |

---

## Demo corpus (prototype)

Until Document / Campaign DB entities exist, validate stories against:

- `backend/app/ai/knowledge_base/demo/campaigns.txt`
- `backend/app/ai/knowledge_base/demo/rewards_policy.txt`
- `backend/app/ai/knowledge_base/demo/faq.txt`

Structured Customer / Transaction / Reward data for T3/T7 may be **mocked** in Track B.

---

## Global acceptance rules (all stories)

1. **Grounded:** Answer only from retrieved context and/or tool results.
2. **Cite sources:** Name file / section (later: document version id).
3. **No invention:** Do not invent ₹ amounts, windows, or eligibility.
4. **Refuse clearly:** If evidence is missing or conflicting without resolution, say so.
5. **Role awareness (T6+):** Do not leak ENGINEER-only infra content to SUPPORT.

---

## T1 — Policy Q&A (Support)

| Field            | Detail                                                           |
|------------------|------------------------------------------------------------------|
| **Actor**        | `SUPPORT`                                                        |
| **Goal**         | Answer a factual cashback/policy question with citations         |
| **Example**      | “What is the maximum cashback per transaction?”                  |
| **Expected**     | ₹500; cite `rewards_policy.txt` and/or `faq.txt`                 |
| **Success**      | Correct fact + at least one source; no extra made-up caps        |
| **Fail safely**  | If not in corpus: “I don’t have that in the knowledge base.”     |
| **Track B skill**| Manual RAG end-to-end                                            |

---

## T2 — Eligibility check (Campaign Ops)

| Field            | Detail                                                                     |
|------------------|----------------------------------------------------------------------------|
| **Actor**        | `CAMPAIGN_OPERATIONS`                                                      |
| **Goal**         | Explain whether a purchase scenario appears eligible under known rules     |
| **Example**      | “Is a refunded transaction eligible for Festival Bonanza cashback?”        |
| **Expected**     | No — refunded/cancelled not eligible; cite policy + relevant campaign context |
| **Success**      | Clear yes/no + conditions used; citations                                  |
| **Fail safely**  | Missing campaign or amount details → ask for missing inputs or refuse      |
| **Track B skill**| Multi-doc retrieval + grounded reasoning                                   |

---

## T3 — Why wasn’t cashback credited? (Investigation)

| Field            | Detail                                                                                      |
|------------------|---------------------------------------------------------------------------------------------|
| **Actor**        | `SUPPORT`                                                                                   |
| **Goal**         | Investigate a specific customer/txn using tools + knowledge                                 |
| **Example**      | “Customer C-1001, txn TX-7788 — why no cashback?”                                           |
| **Expected**     | Agent calls tools (e.g. get transaction, get reward status) **and** RAG for rules; explains with evidence |
| **Success**      | Tool outputs + rule citations; no hallucinated txn state                                    |
| **Fail safely**  | Unknown txn id → say not found; do not invent settlement status                             |
| **Track B skill**| Agentic AI: multi-tool LangGraph agent (mock DB OK)                                         |

---

## T4 — Conflicting / versioned documents

| Field            | Detail                                                                                    |
|------------------|-------------------------------------------------------------------------------------------|
| **Actor**        | `CAMPAIGN_OPERATIONS` or `SUPPORT`                                                        |
| **Goal**         | Prefer current policy when sources disagree; surface conflict                             |
| **Example**      | “What’s the claim/credit window?” when two docs differ                                    |
| **Expected**     | Prefer latest version when versioning exists; otherwise state conflict + both sources     |
| **Success**      | User sees which source won and why                                                        |
| **Fail safely**  | Never silently pick a random chunk                                                        |
| **Track B skill**| Metadata / provenance (prototype: label sources; production: `DocumentVersion`)           |

---

## T5 — Vague query rewrite

| Field            | Detail                                                                                      |
|------------------|---------------------------------------------------------------------------------------------|
| **Actor**        | `SUPPORT` (or customer-facing phrasing relayed by Support)                                  |
| **Goal**         | Turn conversational language into a retrieval-friendly query, then answer the **original** ask |
| **Example**      | “Why didn’t I get my money back?”                                                           |
| **Expected**     | Rewrite toward cashback/credit/eligibility language → hybrid retrieve → rerank → answer     |
| **Success**      | Better retrieval than raw vague query; final answer still addresses user wording            |
| **Fail safely**  | After rewrite still weak → say insufficient context                                         |
| **Track B skill**| Query rewriting + hybrid RAG (already in `RAGService`)                                      |

---

## T6 — Role-scoped answers (RBAC)

| Field            | Detail                                                                           |
|------------------|----------------------------------------------------------------------------------|
| **Actor**        | `SUPPORT` vs `ENGINEER`                                                          |
| **Goal**         | Same question, different allowed corpus                                          |
| **Example**      | “What happens when purchase validation fails?”                                   |
| **Expected**     | ENGINEER may see engineering/RAG runbooks; SUPPORT gets ops-safe explanation only |
| **Success**      | Retrieval filtered by role; no infra leakage to SUPPORT                          |
| **Fail safely**  | SUPPORT: “Not available for your role” rather than partial leak                  |
| **Track B skill**| AuthZ story; implement fully after JWT/RBAC (mock filter OK in Track B)          |

---

## T7 — Human-in-the-loop payout decision

| Field            | Detail                                                                      |
|------------------|-----------------------------------------------------------------------------|
| **Actor**        | `SUPPORT` (approver)                                                        |
| **Goal**         | Agent proposes an action; human must approve before “credit”                |
| **Example**      | Agent: “Evidence suggests miss; propose credit ₹50 for TX-7788. Approve?”   |
| **Expected**     | LangGraph interrupt; no side effect until approve/reject                    |
| **Success**      | Reject leaves system unchanged; approve recorded as decision (mock OK)      |
| **Fail safely**  | Never auto-credit in Track B                                                |
| **Track B skill**| HITL / LangGraph interrupts                                                 |

---

## T8 — Bad retrieval retry (self-correcting RAG)

| Field            | Detail                                                                              |
|------------------|-------------------------------------------------------------------------------------|
| **Actor**        | Any internal user                                                                   |
| **Goal**         | If retrieved context is weak, rewrite and retry; stop after N attempts              |
| **Example**      | First retrieve off-topic → rewrite → better chunks → answer                         |
| **Expected**     | Grade relevance → retry path → capped attempts → refuse if still weak               |
| **Success**      | Observable attempts; no infinite loop; grounded final answer or clean refusal       |
| **Fail safely**  | Max attempts exceeded → “Could not find reliable sources.”                          |
| **Track B skill**| LangGraph conditional routing + real `RAGService` (upgrade `retry_workflow.py`)     |

---

## Track B delivery order (learning)

| Order | Story   | Milestone                                         |
|-------|---------|---------------------------------------------------|
| 1     | T1, T5  | Manual RAG proven on demo corpus                  |
| 2     | T2      | Multi-doc grounded eligibility                    |
| 3     | T8      | Real retrieval inside LangGraph retry             |
| 4     | T3      | Multi-tool investigation agent (mock DB)          |
| 5     | T7      | HITL approval node                                |
| 6     | T4, T6  | Provenance + role filter (deeper / post-Auth)     |

Then resume platform path: **Authentication (JWT) → Authorization → RBAC**.

---

## Interview one-liner (after Track B)

> “I built a cashback-ops knowledge assistant: hybrid RAG (dense + BM25 + RRF + rerank + query rewrite) grounded on Gemini, then wrapped it in LangGraph for self-correcting retrieval and a multi-tool investigation agent with human approval for payout proposals.”

---

## Out of scope for these stories

Do not invent entities banned in `AI_AGENT_CONTEXT.md` (§5): Department, ChatSession, DocumentChunk tables, etc.  
Prototype RAG under `app/ai/rag/` stays reference; production Chroma/S3 waits for Document domain unless overridden.
