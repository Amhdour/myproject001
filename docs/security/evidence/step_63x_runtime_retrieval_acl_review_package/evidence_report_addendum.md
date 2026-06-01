# Evidence Report Addendum — Step 63X

## Category

`runtime_retrieval_acl_review_package`

## Evidence path

`docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/`

## Included evidence artifacts

- `README.md`
- `control_summary.md`
- `demo_attack_results.md`
- `ci_gate_results.md`
- `staging_retest_results.md`
- `audit_log_sample.md`
- `telemetry_sample.md`
- `claim_boundary.md`
- `known_limitations.md`
- `reviewer_questions.md`

## Code/test artifacts

- `backend/security_layer/runtime_enforcement/telemetry.py`
- `backend/security_layer/runtime_enforcement/retrieval_adapter.py`
- `backend/tests/security_layer/test_runtime_retrieval_acl_step_63x.py`
- `demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py`
- `.github/workflows/runtime-retrieval-acl-security.yml`

## Current status

`BOUNDED_RUNTIME_RETRIEVAL_ACL_PROOF_READY_FOR_PR_REVIEW`

## Oracle VPS verification evidence

### Verified checkout

- Host: `rag-agent-security-staging-v2`
- Branch: `step-63x-runtime-retrieval-acl-proof`
- Commit SHA: `1eb6f5391dde968e7d6c0a033cf077122a8a3a44`
- Environment: `.venv-step63x`

### Demo attack result

`ORACLE_STEP63X_DEMO_ATTACK_PASS`

Observed output:

```text
PASS: unauthorized cross-tenant retrieval was blocked.
decision=deny reason=retrieval_authorization_failed denied_chunk_count=1
audit_event=retrieval_authorization_failed telemetry=retrieval_acl_decision_total
```

### No-pytest function-level verifier result

`ORACLE_STEP63X_NO_PYTEST_FUNCTION_VERIFIER_PASS`

Observed output:

```text
PASS: test_disabled_mode_preserves_existing_retrieval_behavior
PASS: test_monitor_only_records_cross_tenant_violation_without_blocking
PASS: test_enforce_mode_blocks_cross_tenant_chunk_and_allows_same_tenant_chunk
PASS: test_enforce_mode_allows_authorized_same_tenant_subject_scoped_chunk
PASS: test_enforce_mode_blocks_wrong_subject_even_when_tenant_matches
PASS: Step 63X no-pytest function-level verification completed.
```

## Remaining blockers / pending evidence

- Focused pytest remains blocked by repo-wide `backend/tests/conftest.py` dependency loading for `fastapi_users` in the minimal Oracle verification venv.
- GitHub Actions result is pending until the workflow runs on the PR.
- Oracle/Coolify full staging retest is not claimed from this function-level verification.
- External reviewer response is pending.

## Non-claim statement

This addendum does not claim production readiness, enterprise production-candidate readiness, full Onyx-wide enforcement, external validation, compliance certification, CI success, or full staging GO.
