# Defect Log

1. The first build expected seven context nodes, but input-only scope correctly contains six; the seventh node from the earlier Hermes task was an output-token change. Assertion stopped before import. DoD and build assertion were corrected to six.
2. The first registration assertion ran immediately when Docker health became healthy, before webhook rows appeared. An independent check seconds later confirmed both rows and HTTP 200. No rollback was required.

No secret was exposed or committed.
