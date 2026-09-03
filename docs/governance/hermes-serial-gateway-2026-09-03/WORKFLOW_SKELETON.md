# Workflow Skeleton

`Hermes HTTP node -> internal gateway 172.18.0.1:18644 -> bounded queue -> semaphore(1) -> unchanged Cloudflare upstream -> response`

The gateway accepts only GET health/models and POST chat-completions paths, caps bodies, forwards a restricted header allowlist, and never logs payloads or authorization values.

Rollback: republish the prior workflow version and disable/remove the gateway service.
