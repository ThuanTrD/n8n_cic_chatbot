# IntelliCAD production QA  2026-09-03

Workflow: `JivRSTL8gODfi5sc` (`CMS IntelliCAD - Facebook Chatbot`)

## Changes

- Remapped all PostgreSQL nodes from the deleted credential to the valid project credential.
- Routed the semantic router, answer model, and verifier through a VM-side bounded Qwen gateway.
- Set Qwen inference concurrency to 1 with a maximum waiting queue of 20.
- Kept conversation history at five messages and added deterministic answer safety guards.
- Removed an orphan direct-Qwen test node and all temporary evaluation routing.

## Validation

- Initial scenario suite: 16 of 16 webhook executions completed successfully.
- Targeted regression suite: 9 of 9 executions completed successfully.
- Final focused regression suite: 4 of 4 executions completed successfully.
- Production Qwen gateway smoke execution: `15316`, successful with three serialized model calls.
- Saturated-history token probe: `15337`, successful with exactly five history messages.
- Five-user test: all five webhooks returned HTTP 200 in 1.962.36 seconds.
- Five-user executions `15329``15333`: 5 of 5 successful.
- Gateway observation: maximum active inference 1, maximum waiting 4, exactly 15 completed model calls.
- Hidden node errors: none in final regression, smoke, or load-test executions.

## Token observations

| Condition | Router input | Agent input | Verifier input | Total input | Total output |
| --- | ---: | ---: | ---: | ---: | ---: |
| No history | 918 | 5,612 | 1,607 | 8,137 | 905 |
| Five-message history | 1,712 | 6,516 | 2,362 | 10,590 | 1,019 |

History growth is bounded at five messages. The measured saturated-history input was about 30% above the empty-history case and did not grow without limit.

## Safety and cleanup

- Test requests used isolated customer and message identifiers.
- Outbound Meta sends were suppressed during evaluation; the temporary adapter was removed afterward.
- No credentials, raw execution payloads, customer content, or authorization headers are stored here.
- Production webhook paths and Meta URLs were restored and the n8n health check passed.
