# Defect Log

## D-01 — Generated JavaScript escapes
Initial generator converted JavaScript newline/regex escapes. Converted embedded Code-node bodies to raw strings; 41/41 nodes compile. Status: `accepted`.

## D-02 — Product-specific credential display name
The shared Postgres credential ID carried an IntelliCAD display label. The reviewed artifact uses a generic label; n8n normalizes it to the stored credential name on import. Comparison now verifies credential type and ID. No product data coupling exists. Status: `accepted`.

## D-03 — Concurrent version claims
Initial reservation distinguished only identical hashes. Added document-wide active-run blocking, explicit claim ownership and a 12-hour stale recovery window. Same- and changed-hash concurrency scenarios pass. Status: `accepted`.

## D-04 — Pending metadata publication
Initial version preparation could update the document metadata before embeddings completed. Metadata now remains in the version and is copied to the public document only in the atomic complete-finalization path. Status: `accepted`.
