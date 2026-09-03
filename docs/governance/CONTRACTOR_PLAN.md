# Contractor Plan

## Package P1: secure n8n workflow backup

Scope: sanitizer, scanner, backup/push script, sanitized workflow files, documentation, and daily timer.

Excluded: credential export, database backup, execution history, modifying live workflows, importing workflows, and changing n8n containers.

Risk: `high` because source workflows contain secrets and the destination is public.

Rollback: disable/remove the timer and service, then revert the Git commit.
