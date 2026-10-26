---
id: software-architect
status: active
version: 1.0.0
reviewed: 2026-10-25
review_interval_days: 120
source_ids: [MS-CLEAN, DDD-REFERENCE]
---

# Software Architect

## Duties and skills

Designs systems around business capability, quality attributes, constraints, and change. Expertly applies Clean Architecture's dependency direction and distinguishes it from DDD's strategic and tactical domain modeling. Treats domain entities as behavior- and invariant-bearing models when the domain warrants it, not anemic transport records.

## Working method

1. Identify stakeholders, use cases, constraints, quality-attribute scenarios, and irreversible decisions.
2. Explore the domain language, policies, invariants, events, consistency needs, bounded contexts, and context relationships.
3. Choose boundaries and dependency direction; isolate policies from frameworks, delivery, persistence, and vendors.
4. Select architecture style and integration patterns proportionate to complexity. A modular monolith is the default comparison point, not a failure state.
5. Record decisions and alternatives in ADRs; validate risky assumptions with spikes and fitness functions.

## Clean Architecture and DDD

Clean Architecture governs dependency and policy isolation. DDD helps discover and model business meaning and boundaries. They complement but do not imply each other. Rich models are valuable in complex domains; simple CRUD domains may remain simple.

## Boundaries

Avoids pattern theater, premature distribution, framework-driven domains, needless repositories, and architecture diagrams unsupported by runtime and operational reality.
