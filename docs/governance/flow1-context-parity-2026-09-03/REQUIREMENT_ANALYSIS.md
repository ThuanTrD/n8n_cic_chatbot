# Requirement Analysis

Objective: make flow 1 use the same input-context limits as optimized flow 2 while keeping flow 1 in production.

Changes are limited to:

- history 15 to 8;
- RAG limits 8/8/10 to 5/5/5;
- normalized customer/admin message caps 8000 to 4000 characters;
- semantic-router context 7000 to 4000 characters;
- validator context 4000 to 2000 characters;
- enable Webhook4 and disable Webhook so the new published version remains flow 1.

Excluded: model, output-token budgets, prompts, credentials, connections, global concurrency, Hermes gateway settings, and workstation configuration.
