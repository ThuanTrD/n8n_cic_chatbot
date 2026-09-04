# Integration Report

- PostgreSQL contract: PREPARE passed for context retrieval, CIC evidence retrieval and lead persistence.
- Model boundary: six HTTP model nodes still target 172.18.0.1:18645; gateway service active.
- Persistence: existing tables and idempotency keys reused; no migration.
- External effects: Facebook and Telegram nodes were not executed in tests.
- Import: exported n8n state matches reviewed parameters exactly after final re-import.
