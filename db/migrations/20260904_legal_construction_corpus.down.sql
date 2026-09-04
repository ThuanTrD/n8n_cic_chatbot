-- Destructive rollback. Use only before legal data is ingested, or after an explicit export/approval.
DROP TABLE IF EXISTS public.legal_ingestion_runs;
DROP TABLE IF EXISTS public.legal_chunk_embeddings;
DROP TABLE IF EXISTS public.legal_document_chunks;
DROP TABLE IF EXISTS public.legal_document_versions;
DROP TABLE IF EXISTS public.legal_documents;
DROP FUNCTION IF EXISTS public.legal_touch_updated_at();
