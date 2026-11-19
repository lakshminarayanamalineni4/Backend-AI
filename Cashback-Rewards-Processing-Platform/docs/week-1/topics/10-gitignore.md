# Topic 10 — `.gitignore` Patterns

| | |
|---|---|
| **Phase** | Week 1 |
| **Status** | Outline |
| **Prerequisites** | Basic Git familiarity |
| **Next topic** | Back to [topic index](./README.md) |

---

## Summary

`.gitignore` tells Git which files and folders to leave out of version control. In this project, it keeps generated Python caches, local virtual environments, test cache files, and secret environment files out of the repository.

---

## Definition

A `.gitignore` file contains **patterns**. Git compares those patterns against files in the repository and skips any match.

Important rule: a `.gitignore` file only applies from the folder where it lives downward. A root-level `.gitignore` can ignore files anywhere in the repo, but a nested `.gitignore` can only affect its own folder and child folders.

---

## Why it matters in this project

The Cashback & Rewards Processing Platform will use a Python backend, local virtual environments, cache folders, and secret values. Ignoring the right files prevents:

- committing secrets by accident
- committing machine-specific environment folders
- polluting the repo with generated cache files
- confusing collaborators with local-only artifacts

This keeps the backend clean, reproducible, and safe to share.

---

## Current `.gitignore` lines

| Line | Pattern | Meaning |
|------|---------|---------|
| 1 | `.venv/` | Ignore the local Python virtual environment folder |
| 2 | `.env` | Ignore the real environment file that may contain secrets |
| 3 | `__pycache__/` | Ignore Python bytecode cache folders |
| 4 | `*.pyc` | Ignore compiled Python bytecode files |
| 5 | `.pytest_cache/` | Ignore cache created by `pytest` |

---

## Core concepts

### Pattern vs path

`.gitignore` entries are usually **patterns**, not full paths.

- `.venv/` matches a folder named `.venv`
- `.env` matches a file named `.env`
- `*.pyc` matches any file ending in `.pyc`

Use a full path only when you want to target one exact location.

### Root-level vs nested `.gitignore`

- A root-level [`.gitignore`](../../../.gitignore) applies across the repository.
- A nested file like [backend/.gitignore](../../../backend/.gitignore) only applies inside [backend/](../../../backend).

That is why a nested `.gitignore` cannot ignore a file in the repository root.

### Trailing slash

The trailing slash means “folder only.”

- `__pycache__/` ignores a directory
- `.venv/` ignores a directory
- `.env` ignores a file, so no slash is needed

---

## Examples (cashback platform)

### Example 1 — Local virtual environment

When you create [backend/.venv](../../../backend/.venv), Git should not track it. The environment is local to your machine and can be recreated at any time.

### Example 2 — Secret environment file

The real [backend/.env](../../../backend/.env) file should stay untracked because it can contain database credentials, JWT secrets, and token settings.

### Example 3 — Generated caches

Python automatically creates `__pycache__/` folders and `*.pyc` files. `pytest` also creates its own cache folder. None of those are source-of-truth project files.

---

## Common pitfalls

- Putting `.env` in git by mistake.
- Forgetting that a nested `.gitignore` cannot ignore root files.
- Using a folder rule without the trailing slash when you only mean a directory.
- Trying to ignore already-tracked files without removing them from Git first.

---

## Study checkpoints

- You can explain why `.venv/` and `.env` belong in `.gitignore`.
- You can tell the difference between a root-level and nested `.gitignore`.
- You can read a pattern like `*.pyc` and know exactly what it matches.

---

## Related topics

- [08-environment-config.md](./08-environment-config.md)
- [02-fastapi.md](./02-fastapi.md)
- [09-pytest.md](./09-pytest.md)
- [Week 1 checklist](../checklist.md)