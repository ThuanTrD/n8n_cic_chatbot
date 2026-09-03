# Contractor Plan

Package: persistent n8n webhook domain correction.

Risk: `high` due production restart and public webhook contract.

Files in persistent runtime scope: `/opt/n8n/.env` only. Repository scope: task evidence and the automatically sanitized workflow snapshot.

Rollback: restore the timestamped `.env` backup, run Docker Compose recreation for `n8n`, and repeat health/registration checks.
