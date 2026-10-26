---
id: software-semantic-html
owner: software-engineer
status: active
version: 1.0.0
reviewed: 2026-10-25
review_interval_days: 120
source_ids: [MDN-HTML, W3C-WCAG]
---

# Semantic HTML

- Choose elements for meaning and native behavior, not appearance: headings, landmarks, lists, links, buttons, labels, tables, details, and dialogs where appropriate.
- Preserve a logical document outline and DOM order. CSS visual rearrangement must not create a confusing reading or focus order.
- Use links for navigation and buttons for actions. Use native controls before recreating them with ARIA.
- Associate labels, instructions, errors, descriptions, and validation status programmatically.
- Add ARIA only to fill semantic gaps; incorrect ARIA can make an interface worse.
- Ensure keyboard operation, visible focus, meaningful names, language metadata, alternative text decisions, and robust progressive enhancement.

Conformance checks support—not replace—manual keyboard, screen-reader, zoom/reflow, and user testing.
