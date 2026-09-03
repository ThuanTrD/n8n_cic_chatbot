# Workflow Skeleton

`verify baseline -> back up .env -> patch two URL values -> recreate n8n only -> wait for health -> verify environment -> verify workflow registration -> test editor/webhook paths -> export sanitized snapshot -> push Git`

Any failed post-change mandatory check triggers rollback from the environment backup.
