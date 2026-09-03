# Idea Comparison

1. Edit Webhook node paths or hard-code callback URLs in nodes. Rejected because the registered path is already correct and n8n derives displayed URLs from global configuration.
2. Update `N8N_WEBHOOK_URL` and `N8N_EDITOR_BASE_URL` in the persistent Compose environment. Selected because it fixes generated URLs globally and is reversible.

The selected change is the smallest configuration-level fix.
