# Preliminary Definition of Done

Success: five concurrent test requests produce upstream max concurrency 1; queue health is observable; only the six intended draft nodes change URL/timeout; global n8n concurrency remains 4; production and webhook registrations remain unchanged; sanitized Git backup passes.

Failure: more than one upstream request runs concurrently, credentials or bodies are logged, unrelated workflow nodes change, or production registration fails.

Forbidden: modifying the workstation, publishing against a 502 upstream, binding the gateway publicly, or committing raw credentials.
