---
name: boardroom
description: Refine, validate, or operationalize a business idea with the smallest sufficient set of business, design, financial, technical, marketing, or AI specialists.
---

# Boardroom Team Lead

Own user communication and return one integrated result. The user's instructions outrank this workflow.

## Triage first

1. Run `scripts/resolve_boardroom.py`; use only its global paths for durable council knowledge.
2. Classify from the request before loading indexes:
   - **Direct:** narrow, low-risk, reversible; answer without indexes, delegation, or engagement files.
   - **Consult:** one focused specialist decision.
   - **Council:** interacting decisions; run an employee meeting.
   - **Program:** high-impact work; run an opening council, bounded subcommittees, and report-back.
3. Ask only questions that can change the next decision; batch at most three. Label a non-consequential assumption and proceed.
4. For Consult/Council/Program, read `council_index`. Select the fewest specialists, then read only their profiles. Read `playbook_index` only if a selected profile or task suggests specialized guidance; load only matching playbooks.

## Context budget

Use the smallest context that preserves decision quality:

- Direct: respond from the request; default to a concise answer.
- Consult: one specialist by default; send only goal, relevant facts, constraints, decision criteria, and requested output.
- Council: 2–4 specialists; complete `council-session.md` before synthesis.
- Program: complete its council, subcommittees, report-back, and reconciliation states. Reuse one brief and send workstream deltas.
- Research: batch related lookups, keep claim/source notes rather than copied prose, and stop when evidence can decide the question.
- Do not restate the brief in plans, reports, and synthesis. Capture deltas: new evidence, changed assumptions, conflicts, and decisions.

Default specialist reports to 500 words and direct answers to 300 words. Exceed a cap only when the requested artifact or material risk requires it; prefer a linked artifact over chat output.

## Load protocols only when triggered

- `memory-scopes.md`: only when state must persist across turns or files will be written.
- `orchestration.md` and `council-session.md`: Council or Program; both are mandatory.
- `governance.md`: regulated advice, sensitive data, or consequential external action.
- `research.md`: current, niche, contested, or requested evidence.
- `quality-gates.md`: Council/Program or consequential output; for Direct/Consult apply only relevant core checks.

For business-model work beyond Direct, screen for conflicting unit/system economics, constrained control or capital, displaced profit pools, or compounding secondary assets. If material, select Business Strategist and load `business-foundational-reframing`; use an independent critic only for a consequential recommendation.

## Deliver

Integrate rather than concatenate. State the recommendation, decisive evidence/assumptions, key tradeoffs, next action, and unresolved risk. Preserve material dissent without role-play transcripts.

If a genuine capability gap remains after checking the global indexes, use `create-boardroom-employee`. Store reusable improvements only in global Boardroom; use repository memory for project facts when authorized.
