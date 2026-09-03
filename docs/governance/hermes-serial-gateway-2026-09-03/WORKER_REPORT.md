# Worker Report

Implemented a Python standard-library serial gateway on 172.18.0.1:18644 with concurrency 1, maximum queue 20, queue timeout 480 seconds, upstream timeout 300 seconds, body limit 2 MiB, restricted paths/headers, and payload-free logging.

Installed and enabled `hermes-serial-gateway.service`. Updated exactly six reachable Hermes draft chat-completion nodes to use the gateway with 600-second n8n timeouts.

Draft version: `e9501437-4b9d-4850-b1b9-e403d638bf76`. Published production remains `05ae075c-4756-43b5-997a-05e727f40b2d`.
