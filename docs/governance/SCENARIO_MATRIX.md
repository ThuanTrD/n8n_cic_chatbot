# Scenario Matrix

| Scenario | Expected | Status |
|---|---|---|
| Clean workflow | Accepted | passed |
| Literal Bearer token | Rejected by check-only gate | passed |
| Live 11-workflow export | All represented in manifest | passed |
| Sanitized live output | No scanner findings | passed |
| No content change | No commit | passed |
| Changed repository content | Commit and SSH push | passed |
| Forbidden tracked paths | None present | passed |
| Daily timer | Enabled with next run near 23:50 local | passed |
