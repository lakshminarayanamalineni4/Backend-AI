# 03 - Docker and Containerization

## Overview

Docker is a containerization platform that packages an application along with its runtime, dependencies, libraries, and configuration into a portable unit called a **container**. This ensures that the application behaves consistently across development, testing, staging, and production environments.

In AI Developer OS, Docker provides a reproducible development environment, while Docker Compose orchestrates multiple services such as FastAPI, PostgreSQL, Redis, RabbitMQ, and background workers.

This document explains Docker from first principles, covers the implementation used in AI Developer OS, and documents the reasoning behind every architectural decision.

---

# 1. Problem Statement

Modern software development faces several challenges:

* Applications work on one developer's machine but fail on another.
* Different operating systems require different installation steps.
* Managing Python versions, dependencies, databases, Redis, and message brokers becomes difficult.
* Onboarding new developers takes significant time.
* Production environments differ from local development.

Example:

Developer A

* Python 3.12
* PostgreSQL 17
* Redis 8

Developer B

* Python 3.11
* PostgreSQL 16
* Redis not installed

Even with the same source code, the application may behave differently.

Docker solves this by packaging everything required to run the application into isolated containers.

---

# 2. Why Docker?

Docker provides:

* Environment consistency
* Dependency isolation
* Fast onboarding
* Portable deployments
* Easy scaling
* Lightweight execution compared to Virtual Machines

Instead of documenting installation steps, the project itself becomes the environment.

---

# 3. Docker Architecture

```
Developer
     │
     ▼
Docker CLI
     │
     ▼
Docker Engine
     │
     ├──────── Builds Images
     ├──────── Runs Containers
     └──────── Manages Networks & Volumes
```

### Docker CLI

Interface used to execute Docker commands.

Example:

```bash
docker build
docker run
docker compose up
```

---

### Docker Engine

Responsible for:

* Building images
* Running containers
* Managing images
* Managing networks
* Managing volumes

---

### Docker Image

A Docker Image is an immutable blueprint that contains:

* Operating System
* Python
* Dependencies
* Application code
* Configuration
* Startup command

Images are read-only.

---

### Docker Container

A container is a running instance of an image.

One image can create multiple containers.

```
Docker Image
      │
      ├──── Container A
      ├──── Container B
      └──── Container C
```

---

# 4. Dockerfile

A Dockerfile is a set of instructions used to build an image.

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

CMD ["uv","run","uvicorn","app.main:app"]
```

Each instruction creates a new image layer.

---

# 5. Docker Image Layers

Docker executes Dockerfile instructions one by one.

Each instruction creates a layer.

Example:

```
FROM
↓

WORKDIR

↓

COPY pyproject.toml

↓

RUN uv sync

↓

COPY .

↓

CMD
```

Layers are cached independently.

If a layer doesn't change, Docker reuses it instead of rebuilding it.

---

# 6. Docker Build Cache

Docker stores previously built layers.

When rebuilding an image:

* unchanged layers are reused
* changed layers are rebuilt
* all dependent layers below them are rebuilt

Example:

```
COPY pyproject.toml
↓

RUN uv sync
↓

COPY .
```

Changing only `app/main.py` rebuilds only the last `COPY .` layer.

Changing `pyproject.toml` invalidates the dependency installation layer, so Docker rebuilds everything after that.

---

# 7. Why Copy Dependencies First?

Instead of:

```dockerfile
COPY . .

RUN uv sync
```

we use:

```dockerfile
COPY pyproject.toml uv.lock ./

RUN uv sync

COPY . .
```

Reason:

* Dependencies change rarely.
* Application code changes frequently.
* Docker cache avoids reinstalling dependencies for every code change.

This significantly reduces build time during development and CI/CD.

---

# 8. Build Context

When building an image:

```bash
docker build .
```

the `.` represents the **build context**.

Docker sends the contents of the current directory to the Docker Engine.

Only files inside the build context can be copied by the Dockerfile.

---

### Build Context in Compose

```yaml
build:
  context: .
```

means the project root is the build context.

---

# 9. .dockerignore

Before sending the build context to Docker Engine, Docker excludes files listed in `.dockerignore`.

Typical entries:

```
.git
.venv
__pycache__
.pytest_cache
.env
```

Benefits:

* Faster builds
* Smaller build context
* Better security

---

# 10. Development vs Production Dockerfiles

Development:

* Debugging enabled
* Live reload
* Development dependencies
* Faster iteration

Production:

* Smaller image
* No development packages
* Optimized runtime
* Immutable container

---

# 11. Docker Compose

Docker Compose defines and manages an entire multi-container application using a single YAML file.

Instead of manually running multiple `docker run` commands, Compose describes the complete application stack.

Example:

```
FastAPI

PostgreSQL

Redis

RabbitMQ
```

can all be started using:

```bash
docker compose up
```

---

# 12. Services

A service describes how Docker should create and manage a container.

Example:

```yaml
services:
  fastapi:
```

A service is **not** an image.

A service is **not** a container.

It is the configuration that Docker Compose uses to create one or more containers.

---

# 13. Build

For development we use:

```yaml
build:
  context: .
  dockerfile: docker/Dockerfile.dev
```

### context

Specifies the build context.

Docker uses the current project directory and sends it to Docker Engine.

### dockerfile

Specifies which Dockerfile should be used.

Since AI Developer OS stores Dockerfiles inside the `docker/` directory, the path must be explicitly provided.

---

# 14. Ports

Compose exposes container ports using:

```yaml
ports:
  - "8000:8000"
```

Syntax:

```
HOST_PORT : CONTAINER_PORT
```

The first value is the host machine's port.

The second value is the container's port.

The property is named `ports` because one service can expose multiple ports.

Example:

```yaml
ports:
  - "8000:8000"
  - "9090:9090"
```

---

# 15. Volumes

Volumes allow files to be shared between the host machine and the container.

Development configuration:

```yaml
volumes:
  - .:/app
```

Meaning:

```
Host Directory
        │
        ▼
Current Project (.)
        │
        ▼
Mounted into
        │
        ▼
Container (/app)
```

Any file changes made on the host become immediately visible inside the container.

No rebuild is required.

---

# 15A. Named Volumes

A named volume is a Docker-managed storage location that exists independently of any container.

Unlike bind mounts, Docker owns and manages the storage, allowing data to persist even when containers are removed or recreated.

Example:

```yaml
services:
  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Architecture:

```
Docker Host

├── PostgreSQL Container
│
└── Named Volume
      │
      ├── Database Files
      ├── Tables
      ├── Users
      └── WAL Logs
```

Benefits:

- Persistent storage
- Better filesystem performance
- Cross-platform consistency
- Correct file permissions
- Easy backup and restore
- Independent of container lifecycle

Named volumes are recommended for:

- PostgreSQL
- Redis
- RabbitMQ
- Uploaded files
- Application-generated data

---

# 15B. Bind Mount vs Named Volume

Docker provides two primary mechanisms for sharing data.

## Bind Mount

Example:

```yaml
volumes:
  - .:/app
```

Docker uses an existing directory from the host machine.

Typical use cases:

- Source code
- Configuration files
- Development

Advantages:

- Immediate file synchronization
- Easy editing from IDE
- Perfect for development

Disadvantages:

- Host OS dependent
- File permission differences
- Lower performance for databases

---

## Named Volume

Example:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Docker creates and manages the storage.

Typical use cases:

- PostgreSQL
- Redis
- RabbitMQ
- Persistent application data

Advantages:

- Better performance
- Better isolation
- Docker manages permissions
- Cross-platform consistency
- Easier backups

---

## Comparison

| Bind Mount | Named Volume |
|------------|--------------|
| Host managed | Docker managed |
| Used for source code | Used for application data |
| Developers edit files | Applications manage files |
| Best for development | Best for production data |
| Directly visible on host | Managed internally by Docker |

Rule of Thumb:

- Developers edit it → Bind Mount
- Application manages it → Named Volume

---

# 15C. Docker Resources

Docker manages several types of resources independently.

```
Docker Host

├── Images
├── Containers
├── Networks
└── Volumes
```

Each resource has its own lifecycle.

Containers are ephemeral.

Volumes are persistent.

Networks connect containers.

Images are immutable templates.

Because volumes are independent resources, deleting a container does not automatically delete its volume.

---

# 15D. Anonymous vs Named Volumes

Docker supports two kinds of Docker-managed volumes.

## Anonymous Volume

Docker automatically generates a random name.

Example:

```
942d90639ee1fe0bcfe7b8aba4e9d003...
```

Useful for temporary storage.

Not recommended for long-term application data.

---

## Named Volume

Developer specifies the name.

Example:

```yaml
volumes:
  postgres_data:
```

Docker Compose creates:

```
ai-developer-os_postgres_data
```

Advantages:

- Easy to identify
- Easy to inspect
- Easy to backup
- Easy to reuse
- Recommended for production

---

# 15E. Volume Lifecycle

When running:

```bash
docker compose up
```

Docker performs the following:

```
Read compose file

↓

Check whether volume exists

↓

No
│
├── Create Volume
│
└── Yes
      │
      ▼
Reuse Existing Volume

↓

Create Container

↓

Attach Volume

↓

Start Application
```

Docker creates a named volume only once.

Future executions reuse the existing volume.

Deleting containers does not remove named volumes.

To remove named volumes:

```bash
docker compose down -v
```

---

# 15F. Container Lifecycle vs Volume Lifecycle

Container

```
Create

↓

Run

↓

Stop

↓

Delete
```

Volume

```
Create

↓

Attach

↓

Detach

↓

Reuse

↓

Delete (only when explicitly removed)
```

This separation allows database data to survive container recreation.

---

# 15G. Why Databases Should Use Named Volumes

Without a named volume:

```
PostgreSQL Container

↓

Database Files

↓

Container Deleted

↓

Database Lost
```

With a named volume:

```
Named Volume

↓

Database Files

↓

Container Deleted

↓

Volume Remains

↓

New Container

↓

Same Database
```

For this reason, databases should never store important data only inside the container filesystem.

---

# 15H. Why Not Bind Mount Database Files?

Technically, this is possible:

```yaml
volumes:
  - ./postgres-data:/var/lib/postgresql/data
```

However, it is generally discouraged.

Reasons:

- Lower performance
- Host filesystem differences
- Permission issues
- Risk of accidental modification
- Database files are implementation details

Databases are designed to manage their own storage.

Docker named volumes provide a safer and more portable solution.

---

# 16A. Docker Compose Resource Model

Docker Compose manages infrastructure resources.

Resources include:

- Services
- Networks
- Volumes

Compose first parses the complete YAML file into an internal model.

Conceptually:

```
Read compose file

↓

Build internal model

↓

Create Volumes

↓

Create Networks

↓

Create Containers

↓

Attach Resources

↓

Start Services
```

Compose does not execute the YAML line by line.

Instead, it first understands the complete infrastructure before creating resources.

---

# 16B. Explicit vs Implicit Configuration

Docker Compose can automatically create named volumes when referenced.

Example:

```yaml
services:
  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

However, explicitly declaring infrastructure resources improves readability.

Recommended:

```yaml
services:
  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Benefits:

- Self-documenting infrastructure
- Easier maintenance
- Easier to extend
- Consistent with large production projects

Engineering Principle:

> Explicit is better than implicit.

Meaning:

Clearly express your intent instead of relying on automatic behavior or assumptions.

---

# 16C. Why Declare Volumes Twice?

At first glance, it appears the volume is declared twice.

Actually, two different things are happening.

Definition:

```yaml
volumes:
  postgres_data:
```

Defines a Docker resource.

Usage:

```yaml
services:
  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

Attaches that resource to a specific container.

Similar examples:

Python:

```python
class User:
    pass

user = User()
```

SQL:

```sql
CREATE TABLE users;

SELECT * FROM users;
```

Git:

```bash
git branch develop

git checkout develop
```

Resources are defined once and referenced wherever needed.

---

# 22A. Docker Debugging Commands

## View Resolved Compose Configuration

```bash
docker compose config
```

Shows:

- Expanded environment variables
- Resolved build configuration
- Generated resource names

---

## View Running Containers

```bash
docker ps
```

---

## View All Containers

```bash
docker ps -a
```

---

## View Docker Images

```bash
docker images
```

---

## View Docker Volumes

```bash
docker volume ls
```

---

## Inspect a Volume

```bash
docker volume inspect <volume-name>
```

---

## Inspect a Container

```bash
docker inspect <container-name>
```

---

## View Logs

```bash
docker compose logs
```

---

## Stop Containers

```bash
docker compose down
```

---

## Stop Containers and Remove Named Volumes

```bash
docker compose down -v
```

---

## Remove Unused Docker Resources

```bash
docker system prune
```

---

# 22B. Frequently Used Docker Commands Explained

## Build Image

```bash
docker build -f docker/Dockerfile.dev -t ai-developer-os:dev .
```

Meaning:

- `docker build` → Build an image.
- `-f` → Specify Dockerfile path.
- `-t` → Assign image name and tag.
- `.` → Current directory is the build context.

---

## Run Container

```bash
docker run -p 8000:8000 ai-developer-os:dev
```

Meaning:

- `docker run` → Create and start a container.
- `-p` → Publish container ports.
- `8000:8000` → HOST_PORT : CONTAINER_PORT.

---

## Start Compose

```bash
docker compose up
```

Creates required resources and starts all services.

---

## Build and Start

```bash
docker compose up --build
```

Rebuilds images before starting services.

---

## Stop Services

```bash
docker compose down
```

Removes:

- Containers
- Compose network

Keeps:

- Images
- Named volumes

---

## Remove Everything

```bash
docker compose down -v
```

Removes:

- Containers
- Networks
- Named volumes

Keeps:

- Images

# 16. Live Reload

Our development Dockerfile starts Uvicorn using:

```dockerfile
CMD ["uv","run","uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]
```

Workflow:

```
Edit Code

↓

Bind Mount

↓

Container sees updated file

↓

Uvicorn detects change

↓

Automatic Restart

↓

Browser refresh shows latest code
```

---

# 17. Why Keep COPY . . ?

Even though development uses bind mounts, we still keep:

```dockerfile
COPY . .
```

Reason:

The Docker image should always contain the complete application.

During development:

```
Image

↓

Bind Mount overlays /app
```

During production:

```
Image

↓

Container
```

Without `COPY . .`, the production image would not contain the application code.

---

# 18. AI Developer OS Implementation

Current Docker Compose configuration:

```yaml
services:
  fastapi:
    build:
      context: .
      dockerfile: docker/Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

Development Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

CMD ["uv","run","uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]
```

---

# 19. Best Practices

* Use official base images.
* Keep images as small as possible.
* Copy dependency files before application code.
* Use `.dockerignore`.
* Separate development and production Dockerfiles.
* Use bind mounts only during development.
* Use immutable images in production.
* Avoid `container_name` in Docker Compose unless required.
* Use service names instead of IP addresses.
* Store secrets using environment variables.

---

# 20. Common Mistakes

* Copying the entire project before installing dependencies.
* Using `localhost` between containers.
* Storing database data inside containers.
* Forgetting `.dockerignore`.
* Using bind mounts in production.
* Rebuilding the image for every code change.
* Hardcoding container names in Compose.
* Installing development packages in production images.

---

# 21. Interview Questions

* Why was Docker created?
* Difference between Virtual Machines and Containers?
* Docker Image vs Docker Container?
* What is Docker Engine?
* What is a Dockerfile?
* What is Docker Hub?
* What is Docker Build Cache?
* What is a Docker Image Layer?
* Why copy dependency files before application code?
* What is Build Context?
* What does `context: .` mean?
* Why use `.dockerignore`?
* Difference between Dockerfile and Docker Compose?
* What is a Service?
* What is `HOST_PORT:CONTAINER_PORT`?
* Why is `ports` a list?
* What are bind mounts?
* Difference between bind mounts and named volumes?
* Why use `--reload` in development?
* Why keep `COPY . .` when using volumes?
* Why avoid `container_name` in Compose?
* Why use official images for PostgreSQL and Redis?

---

# 22. Commands Reference

## Build Image

```bash
docker build -f docker/Dockerfile.dev -t ai-developer-os:dev .
```

## Run Container

```bash
docker run -p 8000:8000 ai-developer-os:dev
```

## Build and Start with Compose

```bash
docker compose up --build
```

## Start Existing Containers

```bash
docker compose up
```

## Stop Containers

```bash
docker compose down
```

## View Running Containers

```bash
docker ps
```

## View All Containers

```bash
docker ps -a
```

## View Images

```bash
docker images
```

## View Logs

```bash
docker compose logs
```

## Remove Unused Resources

```bash
docker system prune
```

---

# Summary

By completing this phase of AI Developer OS, we achieved:

* Built optimized Docker images using `uv`.
* Leveraged Docker layer caching for faster rebuilds.
* Created development-specific Dockerfiles.
* Understood build contexts and `.dockerignore`.
* Implemented Docker Compose for service orchestration.
* Configured port mapping for FastAPI.
* Mounted source code using bind mounts.
* Enabled live code reloading with Uvicorn.
* Established a production-ready Docker development workflow that will scale seamlessly as PostgreSQL, Redis, RabbitMQ, and additional services are introduced.
