# Idea Comparison

## Raw Docker volume backup

Highest fidelity, but it includes the encrypted credential store, encryption coupling, runtime state, and possible personal data. It is unsuitable for a public Git repository.

## Sanitized CLI workflow export

Preserves workflow structure and expressions, creates reviewable diffs, is reversible, and can be security-gated. Literal sensitive parameters and credential identifiers are replaced. This option is selected.

A fully restorable secret-bearing backup requires a private encrypted backup target and is outside this repository's scope.
