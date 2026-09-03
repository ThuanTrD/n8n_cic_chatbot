# Handover

Current webhook URL: `https://hydrogen-valium-liabilities-sit.trycloudflare.com/webhook/intellicad`.

Rollback:

```bash
sudo cp --preserve=mode,ownership,timestamps \
  /opt/n8n/.env.backup-webhook-domain-20260903T015911Z /opt/n8n/.env
sudo docker compose --project-directory /opt/n8n \
  -f /opt/n8n/compose.yaml up -d --no-deps --force-recreate n8n
```

The hostname is a Cloudflare quick-tunnel hostname. If that tunnel is recreated, Cloudflare may issue another hostname and the two environment values must be updated again. A named Cloudflare Tunnel with a stable custom hostname is the durable solution.
