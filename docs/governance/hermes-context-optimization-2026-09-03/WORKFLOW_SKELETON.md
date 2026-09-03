# Workflow Skeleton

`verify baseline/no running execution -> secure raw backups -> generate optimized draft with exact assertions -> validate structural invariants -> CLI import -> republish prior versionId -> verify current/active version split -> verify webhook registration -> sanitized backup -> Git push`

Any failed post-import check triggers republish of the prior version and preservation of raw backups for recovery.
