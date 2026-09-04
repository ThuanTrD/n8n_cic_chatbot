# Definition of Done

- DOD-01: Target remains multi-product and organization-scoped.
- DOD-02: Five customer turns and associated replies are bounded and deduplicated.
- DOD-03: Stored name, phone, email, company and need are merged every turn.
- DOD-04: Invalid phone attempts are acknowledged; valid correction is accepted.
- DOD-05: PRICE and QUOTE remain distinct; unsupported prices are removed.
- DOD-06: Missing product/contact requests ask only for missing data.
- DOD-07: Complete action payloads persist idempotently before confirmation.
- DOD-08: Bot replies are never recorded as human replies.
- DOD-09: URLs remain byte-for-byte intact through formatting.
- DOD-10: Model calls use the serialized gateway with bounded history/output.
- DOD-11: Static and offline branch fixtures pass; no real external send is used.
- DOD-12: Sanitized backup passes security checks and is pushed to Git.
- DOD-13: Target remains inactive until explicit activation.
