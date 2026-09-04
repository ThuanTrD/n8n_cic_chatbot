# Defect Log

## D-01 — Software license false positive

- Observed: initial read-only probe classified eight IntelliCAD FAQ/system-requirement chunks as legal evidence.
- Cause: classifier inspected chunk content and accepted generic `license`.
- Repair: classification now requires legal/certificate/contract signals in document title or controlled document metadata; generic `license` was removed.
- Regression: the same probe returns zero legal documents.
- Status: `accepted`.
