# Handover

## Operate

Run manually with `/home/ADMIN/n8n_cic_chatbot/scripts/backup_and_push.sh`. Inspect automation with `systemctl status n8n-git-backup.timer` and `journalctl -u n8n-git-backup.service`.

## Rollback

Run `sudo systemctl disable --now n8n-git-backup.timer` to stop daily updates. Revert the relevant Git commit to roll back repository content. Removing the timer does not affect live n8n workflows.

## Limitation

This public repository is a sanitized workflow source snapshot, not a full disaster-recovery backup. A private encrypted backup target is required for credential and runtime recovery.
