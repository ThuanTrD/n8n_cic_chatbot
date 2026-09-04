# Idea Comparison

## Option A — Reuse product document tables
Lowest initial work, but requires a fake product, leaks legal authority into product scope and violates the all-products requirement. Rejected.

## Option B — Dedicated legal corpus with n8n ingestion
Adds four organization-scoped tables, reuses validated Drive/OCR/embedding mechanics, and cleanly separates authoritative source/version/derived data. Selected.

## Option C — External ingestion service and queue
Best long-term durability and file scanning, but requires a new service/deployment boundary. Deferred; the schema and state model remain compatible with this migration later.

