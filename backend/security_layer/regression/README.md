# Regression + Demo Attack Bundle

This package is an isolated regression and synthetic demo-attack bundle for the
security layer. It is intended to consolidate high-value regression scenarios,
local synthetic fixtures, and sanitized evidence summaries for partner demos.

Boundaries:

- Synthetic fixtures only; no real tenant, customer, user, document, credential,
  prompt, chunk, or secret data.
- No live application calls.
- No network calls.
- No production database, cache, vector, tool, MCP, artifact, ingestion, or
  deployment writes.
- No enforce-mode runtime activation.
- No shadow-deny runtime activation.
- No live blocking or live filtering.
- No change to application behavior.

Run the isolated tests with:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_regression_demo_models.py backend/security_layer/tests/test_regression_demo_fixtures.py backend/security_layer/tests/test_regression_demo_scenarios.py backend/security_layer/tests/test_regression_demo_runner.py backend/security_layer/tests/test_regression_demo_non_leakage.py -q
```

Non-claim statement: this bundle is not production readiness, not live
enforcement, and not staging attack execution. Real demo attack execution against
staging is a later step.
