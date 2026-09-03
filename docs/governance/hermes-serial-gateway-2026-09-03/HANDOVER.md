# Handover

Service operations:

```bash
systemctl status hermes-serial-gateway.service
curl http://172.18.0.1:18644/health
journalctl -u hermes-serial-gateway.service
```

Current draft: `e9501437-4b9d-4850-b1b9-e403d638bf76`.

Current production: `05ae075c-4756-43b5-997a-05e727f40b2d`.

Resume only after the upstream returns success and `cms-intellicad` maps to the intended Qwen3-VL 30B model. Publish the current draft offline, start n8n separately, then verify registrations and Facebook challenge.

Rollback backup stamp: `20260903T034200Z` under `/opt/n8n/backups`. Disable the gateway with `sudo systemctl disable --now hermes-serial-gateway.service` if reverting.
