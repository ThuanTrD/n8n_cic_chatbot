# Workflow Skeleton

`verify baseline -> secure draft/published backups -> exact asserted context edits -> enable Webhook4/disable Webhook -> structural comparison -> stop n8n -> one-off import </dev/null -> read new versionId -> one-off publish new version </dev/null -> start n8n -> verify health/registration/challenge -> sanitized Git push`

Rollback publishes version 05ae075c-4756-43b5-997a-05e727f40b2d offline.
