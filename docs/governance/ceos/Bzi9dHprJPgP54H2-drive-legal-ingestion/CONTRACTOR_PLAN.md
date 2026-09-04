# Contractor Plan

## WP-01 Schema
Additive legal corpus migration, indexes and RLS. No existing table changes. Rollback before ingestion: drop new tables in dependency order; after ingestion prefer forward-fix/export-first.

## WP-02 Ingestion workflow
Build target from bounded source mechanics with new PostgreSQL persistence and no external notification. Rollback: restore empty target export.

## WP-03 Retrieval integration
Change only the legal CTE/evidence path of `GmiCVh7CyLs4zMMm`. Rollback: restore its pre-change export/version.

## WP-04 Verification and operations
Compile, SQL prepare, migration transaction rehearsal, disposable-row integration, diff review, exact imported-state comparison, sanitizer and Git push.

