# Contractor Plan

Package P1: implement and test a standard-library Python serial proxy plus hardened systemd unit.

Package P2: update exactly six reachable Hermes draft HTTP nodes to use the gateway, preserving production version and all credentials/connections.

Risk: `high` due concurrency, authentication forwarding, public webhook continuity, and production-adjacent workflow import.

Rollback: disable the service and publish the prior workflow version. Raw workflow backups remain permission 600 outside Git.
