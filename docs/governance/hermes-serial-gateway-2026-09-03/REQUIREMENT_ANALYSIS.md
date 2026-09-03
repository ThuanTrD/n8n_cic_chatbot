# Requirement Analysis

Objective: protect the workstation without modifying it and without throttling unrelated n8n workflows.

A VM-side HTTP gateway will serialize only Hermes-branch chat-completion calls with concurrency 1, queue at most 20 requests, reject oversized request bodies, redact request content from logs, and forward existing authorization headers to the unchanged upstream.

Six reachable Hermes-branch HTTP nodes will use the Docker host gateway and a 600-second client timeout. Production remains on the existing version until the Hermes upstream is healthy.
