# Requirement Analysis

Objective: reduce Qwen3-VL 30B workstation load caused by oversized context in the Hermes branch.

Bounded changes:

- conversation history limit 15 to 8;
- RAG limits 10/8 to 5;
- semantic-router retained text 7000 to 4000 characters and output 1200 to 400 tokens;
- validator retained text 4000 to 2000 characters and output 1200 to 500 tokens;
- individual normalized message cap 8000 to 4000 characters;
- Hermes output 1800 to 900 tokens.

Model alias `cms-intellicad`, credentials, prompts, routing policy, and published production version remain unchanged. Publishing Hermes is excluded while its endpoint returns 502.
