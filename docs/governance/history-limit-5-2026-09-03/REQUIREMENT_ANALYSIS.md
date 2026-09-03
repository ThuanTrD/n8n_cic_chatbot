# Requirement Analysis

Objective: reduce conversation history from 8 to 5 messages in both flow 1 and flow 2.

Scope is exactly two history-query nodes and one `LIMIT 8 -> LIMIT 5` replacement per node. RAG limits, message caps, router/validator context, prompts, models, output budgets, credentials, connections, webhook flags, gateway, and workstation are excluded.
