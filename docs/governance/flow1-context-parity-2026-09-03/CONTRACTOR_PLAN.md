# Contractor Plan

Package P1 creates a combined workflow version from the current draft, changing only asserted flow-1 context values and two webhook flags.

Package P2 publishes the new version offline, validates production behavior, and records a sanitized Git snapshot.

Risk: `high` due production publication and webhook continuity.

Rollback: offline publish 05ae075c-4756-43b5-997a-05e727f40b2d and restart n8n.
