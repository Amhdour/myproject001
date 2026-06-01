# Telemetry Sample

## Oracle VPS verification

- Host: `rag-agent-security-staging-v2`
- Path: `~/step63x-verify/myproject001`
- Branch: `step-63x-runtime-retrieval-acl-proof`
- Commit SHA: `1eb6f5391dde968e7d6c0a033cf077122a8a3a44`
- Status: `ORACLE_STEP63X_DEMO_ATTACK_PASS`

## Command run

```bash
PYTHONPATH=. python demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py
```

## Observed telemetry evidence from command output

```text
telemetry=retrieval_acl_decision_total
```

## Expected metric shape

```json
{
  "metric_name": "retrieval_acl_decision_total",
  "mode": "enforce",
  "decision": "deny",
  "enforcement_result": "blocked",
  "denied_chunk_count": 1
}
```

## Purpose

This metric supports reviewer inspection of the bounded retrieval ACL decision path. It is an in-memory test/demo metric and not a production monitoring backend.

## Result

`PASS_FOR_DEMO_ATTACK_OUTPUT`

## Limitations

- This is in-memory demo telemetry evidence, not production monitoring.
- It does not prove Prometheus, OpenTelemetry, SIEM, alerting, retention, dashboards, or SLO integration.
- Focused pytest remains blocked by repo-wide `backend/tests/conftest.py` dependency loading for `fastapi_users` in the minimal Oracle verification venv.
- Production readiness, enterprise readiness, full Onyx-wide enforcement, full staging GO, external validation, and compliance certification are not claimed.
