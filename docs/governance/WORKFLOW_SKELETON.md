# Workflow Skeleton

`systemd timer -> guarded backup script -> n8n CLI export -> sanitizer -> security scan -> atomic workflow directory replacement -> explicit Git staging -> commit when changed -> push`

Failure at export, scan, commit, or push exits non-zero and is recorded by systemd. No Git mutation occurs before the scan passes. Re-running is idempotent when workflow content has not changed.
