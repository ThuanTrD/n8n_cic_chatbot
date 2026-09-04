# Requirement Analysis

## Objective
Bring the verified production behaviors of the CMS IntelliCAD chatbot into the CIC general chatbot while preserving multi-product, organization-wide RAG behavior.

## Scope
- Conversation continuity with five customer turns and persistent lead profile.
- Vietnamese/English semantic routing, product selection, PRICE versus QUOTE, DEMO, lead, feedback and handoff.
- Evidence-only product facts and current prices.
- Deterministic contact and invalid-phone handling.
- Human/bot reply discrimination and bounded handoff polling.
- URL-safe Messenger formatting.
- Serialized local-model gateway and bounded context/output.

## Constraints
- Do not hardcode product 1369, CMS IntelliCAD prompts, or its installer URL.
- No schema migration.
- No real Facebook, Telegram or customer side effect during tests.
- Target remains inactive unless explicitly requested.
- Raw workflow exports and decrypted credentials must not be committed.

## Risk
high: production webhook, personal data, external messages, concurrency, multi-product evidence and persistent actions.
