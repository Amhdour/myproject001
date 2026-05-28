# Integration Plan Summary

Step 27X added an isolated `backend/security_layer/monitor_only/` package and required docs for a limited monitor-only integration bundle.

## Scope

- Models and candidate inventory.
- Disabled-by-default monitor-only flags.
- Shared audit/finding/metric sink helper.
- Cache dry-run adapter helper.

## Out of Scope

- Broad live hooks.
- Enforce mode activation.
- Shadow-deny runtime activation.
- Live blocking/filtering.
- Production-readiness claims.
