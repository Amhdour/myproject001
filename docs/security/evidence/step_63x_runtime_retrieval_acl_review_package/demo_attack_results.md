# Demo Attack Results

## Demo attack

`demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py`

## Scenario

- Acting subject: `user-a`
- Acting tenant: `tenant-a`
- Authorized candidate: `tenant-a-roadmap`
- Unauthorized candidate: `tenant-b-secret-plan`

## Expected result

The unauthorized `tenant-b-secret-plan` chunk must be removed from the allowed chunk set in enforce mode.

## Oracle VPS verification

- Host: `rag-agent-security-staging-v2`
- Path: `~/step63x-verify/myproject001`
- Branch: `step-63x-runtime-retrieval-acl-proof`
- Commit SHA: `1eb6f5391dde968e7d6c0a033cf077122a8a3a44`
- Environment: `.venv-step63x`
- Status: `ORACLE_STEP63X_DEMO_ATTACK_PASS`

## Command run

```bash
PYTHONPATH=. python demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py
```

## Actual output

```text
PASS: unauthorized cross-tenant retrieval was blocked.
decision=deny reason=retrieval_authorization_failed denied_chunk_count=1
audit_event=retrieval_authorization_failed telemetry=retrieval_acl_decision_total
```

## Result

`PASS`

## Limitations

- Focused Step 63X demo proof only.
- Focused pytest remains blocked by repo-wide `backend/tests/conftest.py` dependency loading for `fastapi_users` in the minimal Oracle verification venv.
- GitHub Actions success is not claimed from this evidence.
- Full Oracle/Coolify staging GO is not claimed from this evidence.
- Production readiness is not claimed.
- Enterprise readiness is not claimed.
- Full Onyx-wide enforcement is not claimed.
- External validation is not claimed.
- Compliance certification is not claimed.
