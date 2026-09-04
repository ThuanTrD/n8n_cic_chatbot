# Workflow Skeleton

Customer message → language normalization → bounded RAG retrieval → semantic router (`LEGAL_LOOKUP`) → deterministic legal evidence policy → Qwen answer → legal fact-check → citation/status guard → existing response channel.

Controlled failures:
- no legal evidence → request exact document or staff verification;
- missing effective/version metadata → answer only what the document says and mark current effect unverified;
- conflicting evidence → abstain and escalate;
- model/verifier failure → deterministic evidence-safe response.

