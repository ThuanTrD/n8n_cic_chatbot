# Scenario Matrix

| Scenario | Status | Evidence |
|---|---|---|
| Vietnamese legal intent | passed | deterministic router harness |
| English legal intent | passed | deterministic router harness |
| Legal query without product selection | passed | empty product assertion |
| Supplied certificate evidence | passed | policy harness |
| Source title/number citation | passed | deterministic verifier guard |
| Unknown effective date | passed | explicit current-effect caveat |
| No legal evidence | passed | abstention plus staff-followup flag |
| Prompt injection inside document | passed | agent treats document as data |
| PostgreSQL contract | passed | PREPARE against production-equivalent Supabase |
| PostgreSQL read path | passed | one-row bounded SELECT probe |
| False positive from software license FAQ | passed | repaired classifier returns zero legal evidence |
| Existing PRICE/product selection | passed | regression harness |
| Context/token bounds | passed | 6 answer chunks, 5 verifier chunks, 900/500 token caps |
| Imported parameters equal reviewed artifact | passed | exact comparison |
| Workflow remains inactive | passed | imported export metadata |
| No live Facebook/Telegram sends | passed | workflow not executed |

Actual legal-document answer quality is deferred until the user supplies authoritative documents under `LEGAL_DOCUMENT_CONTRACT.md`; it is outside this readiness slice.
