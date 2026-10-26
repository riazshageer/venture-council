# Memory scopes

Boardroom has two non-interchangeable memory scopes.

## Global Boardroom knowledge

The global Boardroom home is resolved by the active skill's `scripts/resolve_boardroom.py`. Its `core/` contains council employees, playbooks, protocols, schemas, templates, and source provenance shared across every repository.

Only reusable, non-confidential, validated professional capability belongs there. New employees, new playbooks, and improvements to existing ones must be written there through the candidate/validation/promotion workflow. Never write these artifacts into the current repository, even if it has a `core/`, `skills/`, or `.boardroom/` directory.

## Repository-local memory

The current repository owns facts and state about its engagement: brief, goals, constraints, assumptions, decisions, research, reports, deliverables, and retrospective.

Before creating `.boardroom/engagements/<slug>/`, inspect repository instructions and existing memory conventions. Use an existing repository memory system when all are true:

- its instructions or structure make the intended location and format clear;
- the information is relevant to that repository rather than reusable Boardroom capability;
- writing is within the user's requested scope;
- the content contains no unnecessary secrets or personal data.

If the repository memory system is ambiguous, keep Boardroom state under `.boardroom/engagements/<slug>/` rather than guessing. Do not duplicate the same state across both systems. Link to an authoritative project artifact when useful.

## Learning from an engagement

An engagement can produce both kinds of learning. Split them:

- “This product targets accountants in Trinidad” is repository-local.
- “A validated method for evaluating payment rails by country” may become a global playbook after removing client details, sourcing, testing, and promotion.

Promotion copies only the generalized capability, never the client data that revealed the opportunity.
