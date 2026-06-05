# Retrieval ACL Telemetry Counters Runbook

## Scope

Use this runbook to reproduce the Step 10 Retrieval ACL telemetry counters proof.

This runbook covers only process-local in-memory counters for focused tests. It does not cover production readiness, enterprise readiness, staging validation, OpenTelemetry, Prometheus, SIEM integration, dashboarding, durable monitoring, database persistence, or full Onyx-wide authorization coverage.

## How to run tests

From the repository root, run:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/telemetry_counters.py backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/retrieval_acl/metadata_adapter.py
ruff check backend/security_layer/retrieval_acl/telemetry_counters.py backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py
python scripts/portfolio/check_claim_boundary.py
git diff --check
```

If Python dependencies are missing, activate the project virtual environment first:

```bash
source .venv/bin/activate
```

## Expected counter fields

A `RetrievalACLTelemetrySnapshot` should include only:

- `allowed_count`: aggregate count of allowed enforce-mode decisions;
- `denied_count`: aggregate count of denied enforce-mode decisions that are not missing-metadata fail-closed decisions;
- `fail_closed_count`: aggregate count of enforce-mode missing-metadata decisions;
- `storage_scope`: `in_memory_only`;
- `production_readiness`: `NO-GO`;
- `enterprise_readiness`: `NO-GO`.

## Operating rules

- Only enforce mode increments counters.
- Off mode must not increment counters.
- Shadow mode must not increment counters.
- Missing metadata decisions increment `fail_closed_count`.
- Cross-tenant denials increment `denied_count`.
- Allowed same-tenant decisions increment `allowed_count`.
- The snapshot must not include chunk text, prompt text, raw document content, secrets, credentials, or PII.

## Demo attack proof

Run `test_demo_attack_denial_increments_denied_count_without_chunk_content` in `backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py`. The test uses a caller from `tenant-a` and a chunk from `tenant-b`. In enforce mode, the denial increments `denied_count` and the serialized snapshot omits the demo chunk body, raw tenant value, and raw document identifier.

## Safe claims

- Retrieval ACL enforce-mode decisions can update aggregate in-memory counters.
- Off and shadow modes leave the counters unchanged.
- The clear helper resets all three counters.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.
- Staging validation is not claimed.

## Forbidden claims

Do not claim:

- production readiness;
- enterprise readiness;
- staging validation;
- OpenTelemetry support;
- Prometheus support;
- SIEM integration;
- dashboarding;
- durable monitoring;
- database persistence;
- compliance certification;
- storage of chunk text, prompt text, raw document content, secrets, credentials, or PII.

## Rollback note

This proof slice is isolated to the telemetry counter module, one enforce-hook import/call site, focused tests, and documentation. To roll back, remove `backend/security_layer/retrieval_acl/telemetry_counters.py`, remove `backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py`, remove the Step 10 evidence and runbook files, and remove the telemetry counter import and enforce-mode call from `backend/security_layer/retrieval_acl/enforce_hook.py`. No database migration or durable storage rollback is required because this step adds no database persistence.
