# Integration Report

- PostgreSQL 17.6/pgvector migration: applied, SHA-256 `df65f0c724de6c9f5090a12e57c332ce54f3551f0029b9bc732cec9b291751a0`.
- Persistent schema: five empty tables, 23 indexes, forced RLS and five service-role policies.
- Transactional integration: write, changed version, idempotent skip, concurrency, partial/failure containment, tenant FK and chatbot retrieval passed; synthetic rows rolled back.
- Target import: version `8f6a9ef6-1878-4149-ae94-3ad412157a31`, 36 nodes, 35 connection sources, inactive.
- General chatbot import: version `27903867-df41-4f3d-bd54-cb24b24ce9e6`, 84 nodes, 74 connection sources, inactive.
- External Drive/Gemini/embedding calls: intentionally not executed because the legal folder/documents are not configured.

