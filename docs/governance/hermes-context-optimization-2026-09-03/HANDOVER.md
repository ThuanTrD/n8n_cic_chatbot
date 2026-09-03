# Handover

Current draft: `bbbb2dc8-c5cf-46f5-820c-47cb9d32eeca` (optimized Hermes).

Current production: `05ae075c-4756-43b5-997a-05e727f40b2d` (original upper flow).

Resume only after the Hermes endpoint is healthy and alias `cms-intellicad` is verified to map to the intended Qwen3-VL 30B model. Confirm no running executions, stop main n8n, publish the optimized version with the one-off Compose command, then start n8n and verify health, registrations, and Facebook challenge.

Rollback backups:

- `/opt/n8n/backups/JivRSTL8gODfi5sc-draft-before-context-20260903T031713Z.json`
- `/opt/n8n/backups/JivRSTL8gODfi5sc-published-before-context-20260903T031713Z.json`
