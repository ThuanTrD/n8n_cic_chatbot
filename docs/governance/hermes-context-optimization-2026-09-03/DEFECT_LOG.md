# Defect Log

1. Initial RAG assertion expected one `LIMIT 8`, but the query contains two deliberate stages. The build stopped before import. Both were reviewed and intentionally reduced to 5.
2. Initial validator assertion expected one 1200-token request, but the node contains primary and retry requests. The build stopped before import. Both were intentionally reduced to 500.
3. Publishing the prior version while main n8n was running updated version state but did not restore webhook rows. The workflow was recovered using an offline one-off publish followed by n8n startup. Final GET/POST registrations and Facebook challenge passed.

No secret was committed or printed.
