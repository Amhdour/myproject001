# Step 28X Fixture Coverage

Implemented synthetic fixtures:

- cross-tenant retrieval marker fixture
- stale ACL marker fixture
- deleted document marker fixture
- vector namespace/ACL mismatch marker fixture
- cache tenant/ACL collision marker fixture
- unauthorized/high-risk tool marker fixture
- MCP unknown server/confused-deputy/credential-boundary marker fixture
- artifact sensitive/document/prompt-injection marker fixture
- monitor-only no-block/no-filter marker fixture
- shadow-deny no-block marker fixture
- enforce gate block marker fixture
- safe denial non-leakage marker fixture

All fixtures use safe placeholders and assert no real data, raw prompts, raw documents, raw chunks, or raw secrets.
