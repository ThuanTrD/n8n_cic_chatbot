# Idea Comparison

1. Direct SQLite mutation could preserve the active version but bypasses n8n services and risks history/index inconsistency. Rejected.
2. Supported CLI import followed immediately by publish of the known previous production version. Selected because it creates workflow history and explicitly restores the production version.
3. Publish optimized Hermes immediately. Rejected while the Hermes endpoint returns 502.
