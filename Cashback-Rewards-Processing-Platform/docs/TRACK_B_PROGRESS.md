# Track B — GenAI Learning Progress & Agent Prompt

> **Mode:** Guide-only. The agent explains; **you implement**.  
> **Architecture:** `docs/AI_AGENT_CONTEXT.md`  
> **User stories:** `docs/AI_USER_STORIES.md`  
> **Platform progress (Identity/JWT):** `docs/PROJECT_PROGRESS.md` (Track B does not replace it)

Last updated: 2026-08-06

---

## Scoreboard

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Current step       | **2b — ChromaDB + hybrid retrieve (H2)**   |
| Current sub-step   | 2b                                         |
| Next pointer       | Chroma dense + BM25 + RRF + rerank + rewrite |
| After Track B      | Resume Authentication (JWT)                |

---

## Locked decisions (Step 2)

| Decision     | Choice                                                                 |
|--------------|------------------------------------------------------------------------|
| Shape        | `2a → 2b → 2c`                                                         |
| Retrieval    | **H2** — BM25 + RRF + Chroma dense (hybrid)                            |
| Chroma       | Production-shaped **persistent** store (disk path and/or local server) |
| Chroma verify| Install a local viewer/tool (like pgAdmin for Postgres) to inspect data|
| API          | `POST /api/v1/chat/ask`                                                |
| Auth         | Open/internal for learning — JWT later                                 |
| Persistence  | Stateless ask (no `ChatSession` / `ChatMessage` tables)                |
| Who codes    | **You implement**; agent guides only                                   |

---

## Step checklist (pointers)

### Step 1 — Requirements (user stories)
- [x] `docs/AI_USER_STORIES.md` with T1–T8, actors, success/fail, demo corpus
- **Pointer:** `docs/AI_USER_STORIES.md`
- **Status:** ✅ Done

### Step 2 — Demo KB + Chroma hybrid + Chat API
Prove / harden the manual RAG path for T1 + T5, then expose via API.

#### 2a — Demo-only KB + enrich
- [x] Stop using non-demo corpora (loader scoped to demo; folders may still exist unused)
- [x] Keep/index **demo only** under `app/ai/knowledge_base/demo/`
- [x] Enrich demo content for T1–T5 (`campaigns`, `faq`, `rewards_policy`)
- [x] Loader/path config points at demo only (`KNOWLEDGE_BASE_DIR` → `.../demo`)
- **Pointers:** `app/ai/knowledge_base/demo/`, `app/ai/rag/loaders/document_loader.py`
- **Verified:** loader prints 3 docs (2026-08-06)
- **Status:** ✅ Done
- **Optional leftover:** delete unused `enterprise/` + `public_docs/`; fix `determine_source_type` (now reports `unknown`)

#### 2b — ChromaDB + hybrid retrieve (H2)
- [ ] Add Chroma as dense vector store (replace active FAISS path)
- [ ] Production-grade persistence: config-driven path/collection, stable chunk IDs, metadata, reindex
- [ ] Keep BM25 + RRF + rerank + query rewrite wired to Chroma results
- [ ] Rebuild index from demo KB; verify rows in Chroma via local viewer or `peek`/`get`
- [ ] Verify T1 + T5 via existing service/script before API
- **Pointers:** `app/ai/rag/` (vector store, hybrid, sparse, rerank, rewrite, rag_service), `app/core/config.py`, `.env`
- **Status:** 🟡 Current

#### 2c — Chat API (flexible for LC / LangGraph)
- [ ] `POST /api/v1/chat/ask` → thin router → service → RAG pipeline
- [ ] Response: answer + sources (+ optional rewrite/debug fields if useful)
- [ ] No ChatSession/ChatMessage persistence
- [ ] Prove T1 + T5 **via API** (Postman/curl); `test_rag.py` optional smoke only
- [ ] Service shaped so Step 3/4 can call the same core
- **Pointers:** `app/api/routes/` (new chat route), `app/main.py`, `app/ai/rag/rag_service.py`
- **Status:** ⬜

**Step 2 done when:** 2a–2c checkboxes complete and T1+T5 work through `/api/v1/chat/ask`.

### Step 3 — LangChain wrapper (same pipeline)
- [ ] Expose hybrid+rerank path as LangChain retriever/chain
- [ ] Same grounding; call from service or thin adapter (API still works)
- **Pointers:** `app/ai/langchain_learning/` → evolve toward real wrapper
- **Stories:** T1 (and/or T5) via LangChain path
- **Status:** ⬜

### Step 4 — LangGraph self-correcting RAG (T8)
- [ ] Real retrieve in LangGraph: retrieve → grade → rewrite/retry → answer (max N)
- [ ] Wire to same RAG/Chroma core from Step 2
- **Pointers:** `app/ai/langgraph/retry_workflow.py` + RAG service
- **Status:** ⬜

### Step 5 — Investigation agent + HITL (T3 + T7 lite)
- [ ] Multi-tool agent: RAG + mock txn/reward for T3
- [ ] HITL approve/reject for payout proposal (no auto-credit)
- [ ] Prefer calling through chat/ask or adjacent endpoint still service-based
- **Pointers:** `app/ai/langgraph/` (new/extended agent)
- **Status:** ⬜

---

## After Track B

Resume platform path: **Authentication (JWT) → Authorization → RBAC**  
(`docs/PROJECT_PROGRESS.md`).

---

## Out of scope during Track B (unless you override)

- `ChatSession` / `ChatMessage` / other banned entities (`AI_AGENT_CONTEXT` §5)
- Full Document → S3 production ingestion
- JWT on chat (deferred)
- Implementing code for the user (guide only)

---

## Generic prompt (copy-paste each session)

```text
You are my GenAI Track B guide for the BigCity AI Ops platform.

SOURCE OF TRUTH
- Architecture: docs/AI_AGENT_CONTEXT.md
- User stories: docs/AI_USER_STORIES.md
- Track B progress + this prompt: docs/TRACK_B_PROGRESS.md
- Platform Identity progress: docs/PROJECT_PROGRESS.md (do not skip JWT forever; resume after Track B)

LOCKED TRACK B PLAN
1) Requirements (user stories) — DONE
2) Demo KB + Chroma hybrid + Chat API — substeps 2a → 2b → 2c
   - 2a: demo-only KB + enrich
   - 2b: Chroma dense + BM25 + RRF + rerank + rewrite (H2)
   - 2c: POST /api/v1/chat/ask, stateless, no auth (JWT later), thin router → service
3) LangChain wrapper around the same pipeline
4) LangGraph self-correcting RAG (T8) using real retrieval
5) Investigation agent (T3) + HITL lite (T7); mock DB OK

WORKING RULES
- Guide only: explain what/why/where, show example snippets if needed, give exact commands.
- I implement everything. Do NOT write or edit application code unless I explicitly say "implement this for me".
- One step (or one sub-step) only per response. Do not jump ahead.
- Teach-first: explain → wait for me to implement/verify → I confirm → then update docs/TRACK_B_PROGRESS.md checkboxes.
- Do not mark a step complete until I confirm I ran/tested it.
- Preserve working code; evolve, do not restart the whole AI stack.
- No out-of-scope entities (ChatSession, ChatMessage, Department, etc.).
- Interview angle: I should be able to explain each completed step as a realtime project decision.

CURRENT FOCUS
Read docs/TRACK_B_PROGRESS.md Scoreboard.
Work ONLY on the Current step / sub-step listed there.
State: what we will do, why, files I will touch, success criteria, exact commands I should run.
Then stop and wait for me to implement and confirm.

When I say "step done" or "confirmed":
- Update docs/TRACK_B_PROGRESS.md (checkboxes + Scoreboard current/next).
- Give a 2–3 line recap and the next single pointer only — do not start the next step until I ask.
```

---

## How to use

1. Paste the **Generic prompt** at the start of a session (or say “follow TRACK_B_PROGRESS”).  
2. Implement what the guide describes.  
3. Reply **“confirmed”** / **“step done”** when verified.  
4. Guide updates this file’s checkboxes and Scoreboard.
