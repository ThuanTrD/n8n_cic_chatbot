# Idea Comparison

1. Set n8n global concurrency to 1. Reliable but delays all three active workflows. Rejected.
2. Add a database lock inside the workflow. Requires schema/lease recovery and can leak locks across error branches. Rejected.
3. Add a VM-side serial gateway used only by the Hermes branch. Selected because it isolates impact, is observable, testable, and reversible without workstation changes.
