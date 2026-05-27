# Runtime Wrapper Skeletons (Isolated)

This directory contains **minimal isolated wrapper skeletons** for runtime authorization checks.

## Scope
- Isolated-only implementation under `backend/security_layer/runtime/`.
- Not wired into production/runtime request paths.
- No active production enforcement.

## Test-only helpers
- `audit.py`, `findings.py`, and `metrics.py` are in-memory helpers for tests.
- They do not write to production logs, databases, or telemetry pipelines.

## Modes
- `enforce`: deny/approval decisions are enforced.
- `monitor_only`: deny decisions are observed but not blocked.
- `shadow_deny`: deny decisions are recorded as shadow denies without blocking.

## Limitations
- No integration with Onyx request handlers, routers, middleware, retrieval/tool/MCP/artifact/sandbox/model paths.
- No production readiness claim.

## Test command
`PYTHONPATH=. python -m pytest backend/security_layer/tests -q`

## Non-claim statement
This module provides scaffolding only and does not claim runtime security enforcement in application paths.
