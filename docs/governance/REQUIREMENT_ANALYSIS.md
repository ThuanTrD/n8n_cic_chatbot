# Requirement Analysis

## Objective

Version the current n8n workflows in GitHub now and refresh the snapshot daily before the end of the day.

## Actors and permissions

- n8n Docker container: source of workflow definitions.
- VM user `ADMIN`: may run Docker and push through a repository deploy key.
- GitHub public repository: destination; it must receive sanitized content only.

## Inputs and outputs

Input is the output of `n8n export:workflow --backup`. Output is one deterministic JSON file per workflow plus operational scripts and documentation.

## Constraints

- Never commit credentials, encryption keys, database files, execution data, binary data, environment files, or literal auth tokens.
- Preserve n8n expressions and workflow topology.
- Abort before Git staging when the security scan fails.
- Limit this automation to `/home/ADMIN/n8n_cic_chatbot`.
- Schedule assumption: 23:50 daily in `Asia/Ho_Chi_Minh`.

## Side effects and rollback

Successful runs may create a Git commit and push `main`. Disable the systemd timer to stop automation; revert a Git commit to roll back repository content.
