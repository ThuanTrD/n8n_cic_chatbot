# Scenario Matrix

| Scenario | Status | Evidence |
|---|---|---|
| Empty folder configuration | passed | deterministic fail-closed harness |
| Unsupported type and duplicate Drive ID | passed | allowlist/dedupe harness |
| File size over 50 MB | passed | rejection harness |
| Target graph and references | passed | 36-node topology validation |
| All Code nodes compile | passed | 41/41 across ingest and chatbot |
| Metadata supported/unsupported | passed | hallucinated issuer/status rejected |
| Chunk size/count/page/article lineage | passed | deterministic chunk harness |
| Migration and repeat execution | passed | two runs in rollback transaction |
| Persistent schema/RLS/policies | passed | five tables, forced RLS, five service-role policies |
| First write and unchanged hash | passed | real PostgreSQL transaction |
| Changed source creates new version | passed | real PostgreSQL transaction |
| Concurrent same/different hash | passed | busy reservation guard |
| Pending metadata isolation | passed | current document unchanged before finalize |
| Partial embedding | passed | new version remains non-current |
| Failure containment | passed | statuses failed and embeddings non-retrievable |
| Tenant lineage enforcement | passed | composite FK rejection |
| Chatbot legal retrieval | passed | real SQL select through new corpus |
| Imported state equals reviewed artifact | passed | exact parameters/topology/credential IDs |
| Target and chatbot remain inactive | passed | imported metadata |
| Post-test database contains no synthetic rows | passed | all five tables count zero |
| Actual Drive download/Gemini OCR/embedding | not_applicable | legal folder and source documents not yet supplied; no external model calls authorized for synthetic data |
| Live customer/Telegram send | not_applicable | no channel node in target and workflows inactive |
| Sanitized Git backup | passed | 13 workflows sanitized; security check passed with 263 redactions |
