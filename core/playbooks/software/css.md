---
id: software-css
owner: software-engineer
status: active
version: 1.0.0
reviewed: 2026-10-25
review_interval_days: 120
source_ids: [CUBE, BEM]
---

# CSS: CUBE with BEM-compatible blocks

- Use the cascade and intrinsic layout as strengths. Start with global foundations and design tokens.
- Apply CUBE layers: Composition for layout flow, Utility for single-purpose rules, Block for component identity, Exception for explicit contextual/state variation.
- Use BEM-style names inside Blocks when they improve readable component structure; avoid deep selector nesting and specificity contests.
- Prefer logical properties, fluid sizing, container/media queries where supported, and content-driven breakpoints.
- Represent state semantically with attributes or explicit exception markers; keep JavaScript hooks separate where useful.
- Test zoom, reflow, forced colors, reduced motion, long/translated content, and keyboard focus.

Do not convert every rule into a utility or every element into a BEM class. Choose the smallest layer that expresses the responsibility.
