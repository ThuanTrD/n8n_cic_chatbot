# Implementation Roadmap

1. Add product-independent legal source/version/chunk/embedding tables and indexes with RLS.
2. Build an inactive manual Drive ingestion workflow with fail-closed configuration.
3. Reuse bounded PDF/Office OCR and 4096→1024 normalized embeddings from the source workflow.
4. Add source-supported legal metadata extraction and deterministic validation.
5. Persist/finalize through parameterized PostgreSQL and keep incomplete versions non-current.
6. Replace the chatbot's temporary product-document legal lookup with organization-scoped legal tables.
7. Verify schema, static code, workflow topology, idempotency/failure scenarios, exact imports and sanitizer output.
8. Configure a dedicated folder, ingest a small representative document, evaluate citations, then activate only on explicit instruction.

