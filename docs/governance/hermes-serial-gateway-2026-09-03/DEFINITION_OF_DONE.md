# Definition of Done

| ID | Requirement | Evidence |
|---|---|---|
| G1 | Hermes-only concurrency equals 1 | Five-request real local integration test |
| G2 | Queue is bounded to 20 | Configuration and rejection test |
| G3 | Gateway is Docker-internal only | Listener bound to 172.18.0.1 |
| G4 | Six draft AI calls use gateway | Exact export comparison |
| G5 | Global n8n concurrency remains 4 | Container environment |
| G6 | Production version/registration preserved | Database and webhook challenge |
| G7 | No secret in logs/Git | Log review and sanitizer |
