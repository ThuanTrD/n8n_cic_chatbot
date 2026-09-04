# Workflow Skeleton

Manual trigger → validate organization/folder configuration → list trusted Drive folder → allowlist/dedupe/sort → sequential file loop → reserve/check source hash → skip unchanged or download → bounded PDF/Office batches → Gemini OCR → merge/normalize → bounded legal metadata extraction → deterministic metadata validation → create/reuse immutable version → semantic legal chunking with page/article lineage → sequential embedding → upsert embedding → validate counts → atomically switch current version → summary → next file.

Failure branches mark the ingestion/version failed where an ID exists and continue to the next file. No delete/cancellation branch is included. The workflow is inactive and manual.

