# Cache Security (Isolated Minimal Controls)

This module contains **isolated** cache security helper controls only.

- No live cache integration.
- No real cache backend calls.
- No production cache or DB writes.
- No enforcement mode enablement.

Supported checks: tenant/subject/ACL/provenance context checks, cache-key contract validation, cache metadata/TTL checks, stale/deleted/drift/poisoning/prompt-injection markers, and in-memory audit/finding/metric emission.

Test command:

`PYTHONPATH=. python -m pytest backend/security_layer/tests -q`

Non-claim: this isolated module does **not** claim live runtime protection until explicitly integrated.
