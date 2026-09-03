# Definition of Done

| ID | Requirement | Evidence |
|---|---|---|
| R1 | Export every workflow separately | Export count equals manifest count and observed source count |
| R2 | Exclude secrets and credential material | Scanner passes; raw export is absent from repo |
| R3 | Preserve useful workflow structure | Every JSON document parses and retains nodes/connections |
| R4 | Push current sanitized snapshot | Remote `main` resolves to the local commit |
| R5 | Refresh daily | Enabled timer shows the next 23:50 Asia/Ho_Chi_Minh run |
| R6 | Fail safely | Synthetic-secret scanner test is rejected |
