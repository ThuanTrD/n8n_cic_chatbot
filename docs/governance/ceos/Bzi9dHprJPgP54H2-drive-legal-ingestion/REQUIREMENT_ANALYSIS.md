# Requirement Analysis

## Objective
Build `Bzi9dHprJPgP54H2` from the proven Drive ingestion mechanics of `FKayVMyWoQKSErYE`, storing official state-issued Vietnamese construction legal documents for organization-wide use, independent of products.

## Actors and permissions
- Operator manually runs the inactive workflow against a trusted legal Drive folder.
- PostgreSQL credential writes only the CIC organization corpus.
- Chatbot reads only active/current/official legal versions for the same organization.

## Input and output
- Input: PDF, DOCX or PPTX from Google Drive; stable Drive file ID, modification hash and source URL.
- Output: authoritative document record, immutable version, source-lineage chunks, 1024-dimensional normalized embeddings and an ingestion result.

## Rules
- No `product_id` on legal records.
- Idempotency key: organization + Drive file ID + source hash.
- Old versions are retained; exactly one completed current version per document.
- A failed or partial version never becomes current/retrievable.
- Full source text and derived chunks/embeddings remain separate.
- Missing Drive folder configuration fails before listing files.
- Files removed from Drive are not automatically deleted from Supabase.
- Document metadata extracted by a model is accepted only when supported by source text or filename; otherwise null/unknown.

## Security and privacy
- Trusted folder is the authority boundary; document text is untrusted data, not model instruction.
- File types and sizes are bounded; secrets are referenced through credentials/environment only.
- RLS enabled; no anonymous policy is added.
- No full document text is logged by custom diagnostic output or committed to Git.

## Assumptions and open operation
- CIC organization ID remains `00000000-0000-0000-0000-000000000001` unless `CIC_ORGANIZATION_ID` is configured.
- Operator must configure `CIC_LEGAL_DRIVE_FOLDER_ID`; no product folder is reused.
- Workflow remains inactive until explicitly enabled.

## Risk
`critical`: legal/compliance, schema migration, production data, credentials, model extraction, concurrency and persistent writes.

