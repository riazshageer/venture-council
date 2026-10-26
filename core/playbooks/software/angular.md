---
id: software-angular
owner: software-engineer
status: active
version: 1.0.0
reviewed: 2026-10-25
review_interval_days: 90
source_ids: [ANGULAR-STYLE]
---

# Angular

- Inspect the installed Angular version and repository conventions before using current APIs.
- Organize by feature, colocate related component files and tests, keep one primary concept per file, and keep UI code under `src` unless the repository establishes otherwise.
- Keep components focused on presentation; move independently meaningful domain/application logic out of templates and components.
- Prefer current Angular primitives and official migration tooling when compatible with the installed version; preserve local consistency during focused changes.
- Make state ownership, loading/error/empty states, change boundaries, and accessibility explicit.
- Test user-visible behavior and important integration seams rather than implementation trivia.

Verify current APIs against official Angular documentation before adding or migrating patterns.
