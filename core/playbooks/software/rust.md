---
id: software-rust
owner: software-engineer
status: active
version: 1.0.0
reviewed: 2026-10-25
review_interval_days: 90
source_ids: [RUST-GUIDE]
---

# Rust

- Model invalid states out where practical with enums, newtypes, ownership, and visibility.
- Prefer borrowing over cloning by reflex, but optimize clarity before speculative micro-optimization.
- Use `Result` and meaningful error types at library/domain boundaries; reserve panics for violated invariants or unrecoverable initialization conditions.
- Keep unsafe code exceptional, isolated, documented with invariants, and covered by focused tests/tooling.
- Make concurrency ownership and cancellation explicit; avoid holding locks across await points.
- Follow `rustfmt`, Clippy, API documentation, semver, and repository MSRV policy.
- Test examples, edge cases, serialization boundaries, and property/invariant behavior where valuable.

Check the repository toolchain and official Rust/API guidance before adopting newly stabilized language features.
