# Topic 11 — `.env.example` Template

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Outline |
| **Prerequisites** | [08-environment-config.md](./08-environment-config.md) |
| **Next topic** | Back to [topic index](./README.md) |

---

## Summary

`.env.example` is the safe template version of your environment file. It documents which variables the application expects without storing real secrets.

---

## Definition

A `.env.example` file is a commit-safe sample configuration file. New contributors copy it to `.env` and replace the placeholder values with their own local settings.

Unlike `.env`, the example file should contain no secrets, passwords, or machine-specific credentials.

---

## Why it matters in this project

The Cashback & Rewards Processing Platform needs a consistent way to describe backend settings such as:

- database connection string
- JWT signing secret
- JWT algorithm
- access token expiry
- refresh token expiry

Keeping those names in `.env.example` means every developer knows what the app needs before running it.

---

## Current `.env.example` lines

| Line | Value | Meaning |
|------|-------|---------|
| 1 | `DATABASE_URL=postgresql://cashback:cashback@localhost:5432/cashback` | Example PostgreSQL connection string for local development |
| 2 | `JWT_SECRET=change-me-in-production-use-a-long-random-string` | Placeholder signing secret for JWTs |
| 3 | `JWT_ALGORITHM=HS256` | JWT signing algorithm expected by the app |
| 4 | `ACCESS_TOKEN_EXPIRE_MINUTES=30` | Example access token lifetime |
| 5 | `REFRESH_TOKEN_EXPIRE_DAYS=7` | Example refresh token lifetime |

---

## Core concepts

### Template vs real file

- `.env.example` is committed to git
- `.env` is ignored by git
- `.env.example` documents the contract
- `.env` holds your real local values

### Placeholder values

The sample values should be realistic enough to guide setup, but never real enough to be reused in production.

### Variable naming

The names in `.env.example` should match the names your settings layer reads later. If the app expects `REFRESH_TOKEN_EXPIRE_DAYS`, the template must use that exact key.

---

## Examples (cashback platform)

### Example 1 — New developer setup

A new contributor copies `.env.example` to `.env`, fills in a local database URL, and uses a generated JWT secret for their machine.

### Example 2 — Deployment checklist

The same variable names appear in local development, CI, and production. Only the actual values change.

### Example 3 — Settings validation

When the app starts later, it can fail fast if a required key is missing instead of failing deep inside a request.

---

## Common pitfalls

- Committing `.env` instead of `.env.example`.
- Leaving the sample file empty or incomplete.
- Using placeholder names that do not match the application settings.
- Putting real secrets into the example file.

---

## Study checkpoints

- You can explain why `.env.example` is committed but `.env` is not.
- You can describe how a teammate uses the file to create their own local config.
- You can read the sample values and tell which ones are safe placeholders.

---

## Related topics

- [08-environment-config.md](./08-environment-config.md)
- [10-gitignore.md](./10-gitignore.md)
- [Week 1 checklist](../checklist.md)