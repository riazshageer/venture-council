---
name: create-boardroom-employee
description: Research, validate, and add or improve a Boardroom specialist or specialist playbook when the existing council has a demonstrated capability gap.
---

# Grow the Boardroom council

Run the `scripts/resolve_boardroom.py` bundled with this skill first. Use only its returned absolute paths. They identify Boardroom's writable global knowledge store, independent of the current repository. If it is not initialized, stop and provide the install command; never create an employee or playbook in the client repository.

Use this only after the resolved global council and playbook indexes show a genuine gap or an existing profile requires a material new capability.

1. Define the missing decisions, outputs, boundaries, and why current specialists cannot cover them.
2. Prefer a playbook for domain-, platform-, jurisdiction-, or technology-specific expertise owned by an existing employee. Create a new employee only for a distinct professional accountability.
3. Research authoritative primary sources and current official documentation. Record provenance in the resolved global `sources.md`; do not copy source prose into the profile.
4. Create the artifact with `status: candidate`, an owner, version, reviewed date, review interval, triggers, outputs, boundaries, and source IDs.
5. Validate links, metadata, overlap, safety boundaries, and a realistic scenario. A candidate may serve the current engagement but must be labeled provisional.
6. Promote to `active` and update the relevant global index only after validation. Validate the global core, append an audit record to the resolved `audit_log`, record the promotion in the repository-local engagement decision log when one exists, and tell the user that global Boardroom knowledge changed.

Never claim credentials, licensure, lived experience, or guaranteed results. Do not create a specialist merely to add a persona; create decision-relevant capability. Never copy client-confidential or repository-specific information into global Boardroom knowledge.
