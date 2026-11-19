-- prompt 1 --
Read C:\Users\User\OneDrive - Premier Sales Promotions\Documents\Prep\Backend+AI\Cashback-Rewards-Processing-Platform\docs\12-week-roadmap.md first.

Use it as the source of truth for the project.

Then help me with:
week 1 day 1 continution

-- prompt 2 --
Act as a senior backend engineer mentor, not just a code generator.
I am building everything manually and want to understand every decision before implementing it.

I am building this project manually and I want to understand every step instead of blindly generating code.

Before writing any code:

1. Explain why this component/file/module is needed.
2. Explain where it fits in the overall project architecture.
3. Explain what problem it solves.
4. Explain alternative approaches and why we are choosing this approach.
5. Explain industry best practices related to this implementation.
6. Explain how this would be implemented in a production-grade system.

When generating code:

1. Explain each file that needs to be created.
2. Explain why the file should exist.
3. Explain the purpose of each class, function, variable, and configuration.
4. Add comments where appropriate.
5. Explain why specific libraries, frameworks, or patterns are being used.
6. Explain how the code interacts with the rest of the project.

After generating code:

1. Walk through the code line by line.
2. Explain the execution flow.
3. Explain how data moves through the system.
4. Explain common mistakes and pitfalls.
5. Explain performance considerations.
6. Explain security considerations.
7. Explain how this would scale in production.

For project planning:

1. Tell me what I have already completed.
2. Tell me what I am currently working on.
3. Tell me what should be built next.
4. Explain why that next step is important.
5. Break large tasks into small implementation steps.
6. Do not skip foundational concepts.

Assume I am preparing for Backend Engineer interviews and want to understand the reasoning behind every architectural and coding decision.

Act as a senior backend engineer mentor, not just a code generator.


# AI Model Usage Guide for Cashback & Rewards Processing Platform

## Project Context

Project Stack:

* Python
* FastAPI
* PostgreSQL
* RabbitMQ
* Redis
* Docker
* AWS
* JWT Authentication
* RBAC
* Pytest
* GitHub Actions

---

# 1. Qwen3 Coder Next (Default Model)

Use for:

* Daily coding
* API development
* SQLAlchemy models
* Database migrations
* Unit tests
* Refactoring code
* Docker files
* CI/CD pipelines

### Example Prompts

Analyze the current code and suggest improvements.

Create FastAPI CRUD endpoints for Campaigns with:

* JWT Authentication
* RBAC
* Pagination
* Validation
* Error Handling

Generate SQLAlchemy models for:

* User
* Campaign
* CashbackTransaction
* Reward

Write pytest test cases for these endpoints.

Generate a Dockerfile and docker-compose.yml for:

* FastAPI
* PostgreSQL
* RabbitMQ
* Redis

---

# 2. DeepSeek V3 (Architecture & Design)

Use for:

* System design
* Production readiness reviews
* Scalability discussions
* Event-driven architecture
* Database design
* Performance optimization

### Example Prompts

Act as a senior backend architect.

Review this project structure and suggest production-grade improvements.

Design an event-driven cashback processing workflow using RabbitMQ.

Suggest PostgreSQL indexes for high-volume cashback transactions.

Design a scalable rewards engine that can process millions of transactions.

Review this architecture and identify bottlenecks.

How should I implement idempotency in cashback processing?

---

# 3. DeepSeek R1 (Debugging & Reasoning)

Use for:

* Debugging difficult issues
* Root cause analysis
* SQL optimization
* Interview preparation
* Algorithmic reasoning

### Example Prompts

Act as a senior backend engineer.

Analyze this error and explain:

* Root cause
* Impact
* Fix
* Prevention

Review this SQL query and identify performance issues.

Debug this RabbitMQ consumer.

Explain why this API is returning a timeout.

Conduct a backend interview based on my solution.

Review my design and challenge my assumptions.

---

# 4. Gemini 2.5 Flash (Learning & Documentation)

Use for:

* Learning concepts
* Documentation summaries
* Quick explanations
* Technology comparisons

### Example Prompts

Explain RabbitMQ exchanges, queues and routing keys.

Teach me Redis caching strategies used in production.

Summarize FastAPI dependency injection.

Compare RabbitMQ vs Kafka for cashback processing.

Explain PostgreSQL transaction isolation levels with examples.

Create a learning roadmap for distributed systems.

---

# Best Prompt Template

Use this whenever possible.

Project Context:

I am building a Cashback & Rewards Processing Platform.

Tech Stack:

* FastAPI
* PostgreSQL
* RabbitMQ
* Redis
* Docker
* AWS

Requirements:

* Production-ready
* Scalable
* Secure
* Maintainable

Task: <your task here>

Provide:

1. Explanation
2. Implementation
3. Best Practices
4. Potential Pitfalls
5. Improvements

---

# Recommended Workflow

Coding
→ Qwen3 Coder Next

Architecture
→ DeepSeek V3

Debugging
→ DeepSeek R1

Learning
→ Gemini 2.5 Flash
