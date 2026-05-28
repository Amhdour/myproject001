# Shadow-Deny Simulation Harness (Isolated)

This module provides isolated simulation-only helpers for shadow-deny decisions.

- No runtime activation.
- No enforce mode.
- No live blocking or live filtering.
- No production writes (only in-memory simulation records).
- Supported families: retrieval, vector, cache, tool, MCP, artifact, ingestion, safe-denial, audit-metric.

Test command:
`PYTHONPATH=. python -m pytest backend/security_layer/tests -q`

Non-claim: this harness does not claim production readiness or enforcement activation.
