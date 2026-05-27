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

## Step 17C Additions
- `integration_flags.py` adds isolated retrieval integration mode/config helpers (disabled, monitor_only, shadow_deny, enforce).
- `context_builder.py` adds isolated context/candidate builders from safe metadata only.
- `integration_hook.py` adds isolated evaluation hook helpers for monitor, shadow deny, and enforce behavior.
- No live retrieval handlers/search/vector/rerank/context/prompt/cache paths are patched in this step.

## Test command
`PYTHONPATH=. python -m pytest backend/security_layer/tests -q`

## Non-claim
These helpers are isolated and test-focused only; this step does not enable production runtime enforcement.
