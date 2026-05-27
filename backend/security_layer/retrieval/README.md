# Retrieval ACL (Isolated Minimal Controls)

This module provides isolated retrieval ACL helper controls for Step 16B.

## Scope
- Isolated retrieval ACL checks only.
- No live retrieval integration.
- No real search / vector DB / rerank / context assembly / prompt construction calls.
- No production DB / vector store / cache writes.

## Supported checks
- tenant + subject context presence
- retrieval scope validation
- document ACL and chunk ACL validation
- cross-tenant denial
- vector namespace and vector metadata validation
- stale ACL snapshot denial
- deleted document denial
- unauthorized candidate filtering
- isolated audit/finding/metric emission

## Test command
`PYTHONPATH=. python -m pytest backend/security_layer/tests -q`

## Non-claim
This implementation does **not** claim production runtime enforcement and remains intentionally unwired.
