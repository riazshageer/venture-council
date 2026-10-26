---
id: software-nestjs
owner: software-engineer
status: active
version: 1.0.0
reviewed: 2026-10-25
review_interval_days: 90
source_ids: [NEST-DOCS]
---

# NestJS

- Organize modules around coherent capabilities; avoid a global dumping-ground module.
- Keep controllers as delivery adapters, application services focused on use cases, and domain policy free of Nest decorators when Clean Architecture boundaries are required.
- Use dependency injection deliberately; tokens/interfaces at boundaries should not become ceremonial wrappers.
- Validate external input, map transport contracts explicitly, centralize cross-cutting behavior through appropriate pipes, guards, interceptors, filters, or middleware.
- Make authentication, authorization, transactions, idempotency, errors, configuration, observability, and shutdown behavior explicit.
- Test domain/application behavior cheaply and use integration/e2e tests for framework wiring and external boundaries.

Verify decorators, package integrations, and lifecycle behavior against documentation for the installed NestJS version.
