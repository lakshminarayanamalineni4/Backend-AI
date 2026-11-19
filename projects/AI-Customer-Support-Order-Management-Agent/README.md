# AI Customer Support & Order Management Agent

Agentic AI customer-service assistant for a Nestlé-style e-commerce platform. The assistant answers policy questions via RAG, tracks orders, cancels eligible orders, processes simple refunds through controlled APIs, and escalates complex cases to human support.

## Approach

- **Infra first:** Docker, GitHub Actions, AWS EC2, and S3 before feature work
- **Backend first:** Full agent stack before the production frontend
- **Temporary UI:** [Chainlit](https://docs.chainlit.io/) for chat until backend is complete
- **React last:** Production chat UI only after Modules 0–8
- **Deploy per module:** Each module ends with a deploy to EC2

## Documentation

| File | Purpose |
|------|---------|
| [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) | Module-wise build plan and progress checklist |
| [Autonomous_Customer_Support_Refund_Agent_Requirement.docx](./Autonomous_Customer_Support_Refund_Agent_Requirement.docx) | Full product requirements |

## Progress

Track feature completion in [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md). Current focus: **Module 0 — Platform bootstrap**.

## Stack (summary)

FastAPI · PostgreSQL · LangGraph/LangChain · ChromaDB · Chainlit (temp) · React (final) · Redis · RabbitMQ · Docker · GitHub Actions · AWS EC2 + S3
