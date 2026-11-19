# Explain your Cashback Assistant project.

I built a Retrieval-Augmented Generation (RAG) chatbot using FastAPI, FAISS, Sentence Transformers, and Gemini 2.5 Flash. Documents are chunked, converted into embeddings, stored in a FAISS vector index, and retrieved using semantic similarity search. Retrieved context is passed to Gemini to generate grounded responses.

# What is the difference between: Embedding Model and LLM

An embedding model converts text into numerical vectors that capture semantic meaning, enabling similarity search and retrieval. An LLM (Large Language Model) is a deep learning model trained on large amounts of text data to understand and generate human-like responses. In a RAG system, the embedding model helps retrieve relevant information, while the LLM uses that information to generate the final answer.

# Why can't we use an LLM directly without embeddings?

LLMs generate responses based on their training data and may not know company-specific or up-to-date information. Embeddings and retrieval allow us to fetch relevant information from a knowledge base and provide it to the LLM, improving accuracy and reducing hallucinations.

# Cashback & Rewards Processing Platform 2.0

Production-grade loyalty and rewards platform — transactions, async cashback, wallets, redemption, analytics, fraud detection, and AI recommendations.

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | Angular 18+, Angular Material / PrimeNG |
| Backend | FastAPI, PostgreSQL, Alembic |
| Cache | Redis |
| Messaging | RabbitMQ |
| Infra | Docker, AWS (EC2, RDS, S3, CloudWatch) |
| CI/CD | GitHub Actions |
| Tests | Pytest (80%+ coverage target) |

## Structure (planned)

```
backend/          # FastAPI application
frontend/         # Angular application
workers/          # Background consumers
docker/
docker-compose.yml
```

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **1** (Month 1) | Auth, transactions, Docker, tests, CI | Not started |
| **2** (Month 2) | RabbitMQ rewards, wallet, redemption, Redis | Planned |
| **3** (Month 3) | Admin analytics, fraud/AI, AWS deploy | Planned |

## Documentation

Study notes, Week 1 curriculum, and step-by-step build checklists:

**[docs/README.md](./docs/README.md)** → [12-week roadmap](./docs/12-week-roadmap.md) · [Week 1 overview](./docs/week-1/README.md) · [Curriculum](./docs/week-1/curriculum.md) · [Checklist](./docs/week-1/checklist.md) · [Topics](./docs/week-1/topics/README.md)

## Local development

> Week 1 scaffold: follow [docs/week-1/checklist.md](./docs/week-1/checklist.md). Runtime instructions will be added here once the backend is in place.

## Roadmap

For the full three-month execution plan, start with [docs/12-week-roadmap.md](./docs/12-week-roadmap.md). It breaks the project into weekly deliverables across backend, Angular, Docker, automation, deployment, Redis, RabbitMQ, and AWS.

## Main project chat

Use the pinned Cursor chat for this repo for ongoing work. Project context is also stored in `.cursor/rules/cashback-platform.mdc` so new chats inherit the same plan and decisions.
