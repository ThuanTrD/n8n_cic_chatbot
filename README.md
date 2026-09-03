# n8n CIC Chatbot workflow snapshots

This public repository stores sanitized, reviewable n8n workflow definitions exported from the `n8n` Docker container on `instance-20260811-042007`.

## Security boundary

The repository intentionally excludes credentials, encryption keys, runtime databases, execution history, binary data, and literal authorization values. Credential references are replaced with placeholders. The files preserve workflow topology and expressions, but credentials must be recreated and remapped before import.

## Manual backup

```bash
cd /home/ADMIN/n8n_cic_chatbot
./scripts/backup_and_push.sh
```

The script exports all workflows, sanitizes them in a temporary directory, validates the result, replaces `workflows/`, commits only approved paths when content changes, and pushes `main`.

## Schedule

The VM systemd timer `n8n-git-backup.timer` runs daily at 23:50 in `Asia/Ho_Chi_Minh`. Inspect it with:

```bash
systemctl status n8n-git-backup.timer
journalctl -u n8n-git-backup.service
```

## Restore boundary

Import workflow JSON through n8n and then recreate/remap credentials. This repository is not a full n8n disaster-recovery backup.
