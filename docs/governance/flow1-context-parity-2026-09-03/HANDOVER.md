# Handover

Current draft and production version: `56ed3429-95a9-4fea-8013-1cde8a437c9a`.

Production uses flow 1 through Webhook4. Both flows now share the same input-context caps. Flow 2 retains the serial Hermes gateway but remains disabled at its Webhook.

Rollback: offline publish `05ae075c-4756-43b5-997a-05e727f40b2d`, or restore the permission-600 backups with stamp `20260903T040052Z` under `/opt/n8n/backups`.
