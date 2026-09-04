# Requirement Analysis

## Objective
Extend the CIC general chatbot with legal-document and certificate lookup while preserving its multi-product behavior.

## Rules
- Legal claims must come only from supplied, active, current document versions.
- Legal answers require source provenance and must distinguish document lookup from professional legal advice.
- Missing, stale, conflicting, or scope-ambiguous evidence causes abstention or staff escalation.
- Retrieved document text is untrusted data, never executable instruction.
- Legal lookup is organization-wide and must not silently select a product.
- Context and outputs remain bounded for the workstation model.

## Inputs and outputs
- Input: customer question plus supplied legal documents/certificates stored in the existing document corpus.
- Output: concise answer with document title/number and version/effective/page/section metadata when present.

## Constraints
- No schema migration in this slice.
- No document content is invented or ingested before the user supplies it.
- No real Facebook/Telegram message is sent during verification.
- Target remains inactive.
- No raw workflow or secret enters Git.

## Risk
`high`: legal/compliance, production webhook, external publication, personal data and model inference.

