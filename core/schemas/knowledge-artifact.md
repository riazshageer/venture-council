# Employee and playbook schema

Every employee and playbook begins with YAML frontmatter:

```yaml
---
id: unique-lowercase-id
owner: employee-id # playbooks only
status: candidate | active | deprecated
version: 1.0.0
reviewed: YYYY-MM-DD
review_interval_days: 90
source_ids: [SOURCE-ID]
---
```

Employees must put `Duties and skills` first, then working method, collaboration as needed, and boundaries. Playbooks must contain decision-changing guidance rather than a copied tutorial.

Promotion requires a unique ID, valid owner, existing sources, index entry, no broken local links, a realistic scenario check, and documented overlap analysis. Material changes increment the version and reviewed date.
