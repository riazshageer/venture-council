# Engagement schema

An engagement lives at `.boardroom/engagements/<slug>/`. Use lowercase hyphenated slugs. Copy the files from `core/templates/engagement/`; do not create empty folders.

Required files:

- `brief.md`: current scope and success definition.
- `open-questions.md`: unresolved questions and their impact.
- `assumptions.md`: explicit assumptions and approval state.
- `plan.md`: execution shape, specialists, workstreams, and stopping criteria.
- `decisions.md`: append-only decision records.
- `retrospective.md`: engagement-specific learning and candidate durable learning.

Create `research/`, `reports/`, or `deliverables/` only when the engagement needs them. Use ISO `YYYY-MM-DD` dates and stable IDs (`A-001`, `D-001`, `Q-001`). Never store secrets.

## Status values

Engagement: `discovery`, `planned`, `active`, `waiting`, `complete`, `cancelled`.

Assumption: `proposed`, `approved`, `rejected`, `validated`, `invalidated`.

Decision: `proposed`, `decided`, `superseded`, `revisit`.
