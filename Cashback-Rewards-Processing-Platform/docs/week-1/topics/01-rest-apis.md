# Topic 1 — REST APIs

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Complete |
| **Prerequisites** | Basic HTTP familiarity |
| **Next topic** | [02-fastapi.md](./02-fastapi.md) |

---

## Summary

A REST API exposes **resources** (such as `users` and `transactions`) over **HTTP**, using standard **methods** and **status codes**, with **JSON** bodies for structured data. The cashback platform’s backend is a REST API: clients send requests, FastAPI processes them, and responses follow predictable patterns that frontends, mobile apps, and integration tests can rely on.

---

## Definition

**REST** (Representational State Transfer) is an architectural style for networked APIs. Clients interact with **resources** identified by URLs. The server is typically **stateless**: each request contains enough information (later, a JWT) for the server to process it without remembering prior requests.

Key terms:

| Term | Meaning |
|------|---------|
| **Resource** | A domain object exposed via URL (e.g. `/users/me`) |
| **Representation** | How a resource is serialized (usually JSON) |
| **Endpoint** | URL + HTTP method combination (e.g. `GET /health`) |
| **Stateless** | Server does not store client session between requests |
| **Idempotent** | Repeating the same request has the same effect (`GET`, `PUT`, `DELETE`) |

---

## Why it matters in this project

Every feature in the Cashback & Rewards Platform flows through REST:

- **Week 1:** Register, login, profile (`/auth/*`, `/users/me`)
- **Month 1:** Submit and list transactions
- **Month 2:** Wallet balance, redemption, async reward processing triggers
- **Month 3:** Admin analytics and fraud review APIs

Angular’s `HttpClient`, Postman, pytest, and future mobile clients all speak REST. Consistent URL design, status codes, and JSON shapes reduce integration bugs and make the API self-documenting via OpenAPI (`/docs`).

---

## Core concepts

### HTTP methods

| Method | Purpose | Idempotent | Week 1 example |
|--------|---------|------------|----------------|
| `GET` | Read a resource | Yes | `GET /users/me` |
| `POST` | Create or trigger action | No | `POST /auth/register` |
| `PUT` | Replace entire resource | Yes | *(later)* update full profile |
| `PATCH` | Partial update | No | *(later)* change display name |
| `DELETE` | Remove resource | Yes | *(later)* admin delete user |

Use **nouns in paths**, not verbs:

- Preferred: `POST /auth/login`, `GET /transactions`
- Avoid: `POST /doLogin`, `GET /getAllTransactions`

### HTTP status codes

| Code | Name | When to use |
|------|------|-------------|
| `200` | OK | Successful read or login |
| `201` | Created | User registered, resource created |
| `400` | Bad Request | Business rule failed (duplicate email) |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Authenticated but insufficient role |
| `404` | Not Found | Resource does not exist |
| `422` | Unprocessable Entity | Validation failed (invalid email format) |
| `500` | Internal Server Error | Unexpected server failure |

**401 vs 403:** `401` = “who are you?” (no/invalid token). `403` = “I know who you are, but you cannot do this” (wrong role).

### Request and response structure

REST APIs commonly use **JSON** (`Content-Type: application/json`).

**Headers** carry metadata:

```http
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Body** carries the payload (for `POST`, `PUT`, `PATCH`).

### Resource design for the cashback platform

| Resource | Base path | Week 1 scope |
|----------|-----------|--------------|
| Health | `/health` | Yes |
| Auth | `/auth/register`, `/auth/login`, `/auth/refresh` | Yes |
| Users | `/users/me` | Yes |
| Transactions | `/transactions` | Month 1 |
| Wallets | `/wallets` | Month 2 |
| Admin | `/admin/*` | Month 3 |

### Stateless authentication (preview)

Week 1 uses **JWT**: the client stores tokens and sends `Authorization: Bearer <token>` on each protected request. The server validates the token without a server-side session store. Details in [05-jwt-authentication.md](./05-jwt-authentication.md).

---

## Examples (cashback platform)

### Example 1 — Health check

Simplest endpoint; confirms the API process is running.

**Request**

```http
GET /health HTTP/1.1
Host: localhost:8000
```

**Response** — `200 OK`

```json
{
  "status": "ok"
}
```

---

### Example 2 — Register user

**Request** — `POST /auth/register`

```json
{
  "email": "alice@example.com",
  "password": "SecurePass123!",
  "full_name": "Alice Smith"
}
```

**Response** — `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "alice@example.com",
  "full_name": "Alice Smith",
  "role": "user"
}
```

The response never includes `password` or `hashed_password`.

---

### Example 3 — Login

**Request** — `POST /auth/login`

```json
{
  "email": "alice@example.com",
  "password": "SecurePass123!"
}
```

**Response** — `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### Example 4 — Protected profile

**Request** — `GET /users/me`

```http
GET /users/me HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response** — `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "alice@example.com",
  "full_name": "Alice Smith",
  "role": "user"
}
```

**Without token** — `401 Unauthorized`

```json
{
  "detail": "Not authenticated"
}
```

---

### Example 5 — Error responses

**Duplicate registration** — `400 Bad Request`

```json
{
  "detail": "Email already registered"
}
```

**Invalid credentials** — `401 Unauthorized`

```json
{
  "detail": "Invalid email or password"
}
```

**Validation error** — `422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error"
    }
  ]
}
```

FastAPI returns `422` automatically when Pydantic validation fails.

---

### Example 6 — End-to-end auth flow

```text
1. POST /auth/register     → 201  (user created)
2. POST /auth/login        → 200  (tokens issued)
3. GET  /users/me          → 200  (with Bearer access_token)
4. GET  /users/me          → 401  (without Authorization header)
```

This sequence is the Week 1 acceptance test. Run it in Swagger UI (`/docs`), Postman, or pytest.

---

## Common pitfalls

| Pitfall | Why it is a problem | Better practice |
|---------|---------------------|-----------------|
| Verbs in URLs (`/getUser`) | Breaks REST conventions; harder to document | Noun paths: `/users/me` |
| Returning passwords in JSON | Security breach | Return only safe fields; hash server-side |
| `200` for everything | Clients cannot handle errors | Use correct status codes |
| Inconsistent error shape | Frontend needs custom parsers per endpoint | Standardize on `{ "detail": "..." }` |
| Putting sensitive data in query strings | URLs are logged | Use headers (Bearer) or POST body |

---

## Study checkpoints

Answer these before moving to [FastAPI](./02-fastapi.md):

1. What is the difference between a **resource** and an **endpoint**?
2. When should you return `401` vs `403`?
3. Why is `POST /auth/register` **not** idempotent?
4. What does `422` mean in a FastAPI application?
5. Write the JSON body for a login request and list the headers needed for `GET /users/me`.
6. Why should error responses use consistent JSON structure?

---

## Related topics

| Topic | Relationship |
|-------|--------------|
| [02-fastapi.md](./02-fastapi.md) | Implements REST routes in Python |
| [05-jwt-authentication.md](./05-jwt-authentication.md) | Bearer token pattern for protected routes |
| [09-pytest.md](./09-pytest.md) | Automated verification of REST contracts |

---

## Further reading

- [MDN — HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [MDN — HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Tutorial — HTTP methods](https://restfulapi.net/http-methods/)
