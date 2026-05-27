# Vector Security Layer (Isolated)

This package provides **isolated vector DB security helper controls** only.

- No live vector DB integration.
- No real vector DB/search/index/cache calls.
- No production DB/vector/cache writes.
- No application-path wiring.

Supported checks include:
- context, namespace, metadata, ACL snapshot, provenance validation
- deleted/stale candidate filtering
- prompt-injection and poisoning marker flagging
- safe denial mapping + in-memory audit/finding/metric emission

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests -q
```

## Non-claim

This module does **not** claim production enforcement. Enforcement remains inactive.
