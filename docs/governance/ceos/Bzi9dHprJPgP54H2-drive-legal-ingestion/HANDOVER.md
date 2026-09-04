# Handover

## Delivered
- `Bzi9dHprJPgP54H2`: inactive legal Drive ingestion workflow.
- Dedicated `legal_*` Supabase corpus for all CIC products.
- General chatbot retrieval integration.

## Required operator action
Set `CIC_LEGAL_DRIVE_FOLDER_ID` on the n8n container/service, restart n8n if needed, place a small authoritative PDF in that folder, manually execute the workflow and review the generated document number, issuer, dates, page/article citations and chunk count. Do not activate scheduling before this pilot passes.

## Retention
Removing a Drive file does not delete legal records. Superseded versions remain for audit and become non-current only after a complete replacement succeeds.

## Rollback
Workflow: restore the pre-change exports/versions. Schema: before real ingestion, the reviewed down migration may drop only the five empty `legal_*` tables; after ingestion, export data and use a forward-fix unless destructive rollback is explicitly approved.

