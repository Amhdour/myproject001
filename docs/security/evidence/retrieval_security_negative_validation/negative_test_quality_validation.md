# Step 18E Negative Test Quality Validation

- Explicit negative tests in `test_retrieval_security_negative_cases.py`: 13.
- Covered required negative cases:
  - cross-tenant document
  - cross-tenant chunk
  - unauthorized group
  - unauthorized role
  - stale ACL
  - deleted document
  - vector namespace mismatch
  - vector metadata mismatch
  - cache cross-tenant fixture
  - citation denied fixture
  - rerank denied fixture
  - non-leakage (raw text/secrets/token/API key patterns)
- Added/strengthened in Step 18E:
  - monitor-only candidate count + identity + order preservation for mixed negative cases.
- No future-mode test enables enforce or shadow-deny.
- No live retrieval behavior changed.
