# Engagement schema

An engagement lives at `.boardroom/engagements/<slug>/`. Use lowercase hyphenated slugs. Copy the files from `core/templates/engagement/`; do not create empty folders.

Create an engagement only when state must survive the current turn. Start with `brief.md`; add `decisions.md`, questions, assumptions, plan, retrospective, `research/`, `reports/`, or `deliverables/` only when each carries unique state that will be read again. Do not duplicate the brief across files.

Use ISO `YYYY-MM-DD` dates and stable IDs (`A-001`, `D-001`, `Q-001`). Never store secrets.

## Status values

Engagement: `discovery`, `planned`, `active`, `waiting`, `complete`, `cancelled`.

Assumption: `proposed`, `approved`, `rejected`, `validated`, `invalidated`.

Decision: `proposed`, `decided`, `superseded`, `revisit`.
