# Audit Log Sample

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

## Observed audit evidence from command output

```text
audit_event=retrieval_authorization_failed
```

## Expected audit event shape

```json
{
  "event_type": "step_39x_runtime_retrieval_authorization",
  "request_id": "step-63x-cross-tenant-demo-attack",
  "mode": "enforce",
  "action": "retrieve",
  "resource_type": "chunk",
  "tenant_id": "tenant-a",
  "subject_id": "user-a",
  "decision": "deny",
  "reason_code": "retrieval_authorization_failed",
  "enforcement_result": "blocked"
}
```

## Redaction note

The sample intentionally excludes retrieved content and unauthorized document content.

## Result

`PASS_FOR_DEMO_ATTACK_OUTPUT`

## Limitations

- This is redacted demo-output evidence, not a production audit sink.
- It does not prove audit retention, tamper-evidence, centralized logging, or SIEM integration.
- Focused pytest remains blocked by repo-wide `backend/tests/conftest.py` dependency loading for `fastapi_users` in the minimal Oracle verification venv.
- Production readiness, enterprise readiness, full Onyx-wide enforcement, full staging GO, external validation, and compliance certification are not claimed.
