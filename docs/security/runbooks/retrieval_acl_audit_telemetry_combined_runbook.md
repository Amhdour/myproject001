# Retrieval ACL Audit + Telemetry Combined Proof Runbook

## Scope

This runbook covers the focused in-memory proof that enforce-mode Retrieval ACL decisions can create both redacted audit events and aggregate telemetry counter updates.

This runbook is not a production, enterprise, staging, compliance, SIEM, OpenTelemetry, Prometheus, database-persistence, or durable-monitoring runbook.

## How to run tests

Run from the repository root:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_decision_observability.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_audit_events.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/decision_observability.py backend/security_layer/retrieval_acl/audit_events.py backend/security_layer/retrieval_acl/telemetry_counters.py backend/security_layer/retrieval_acl/enforce_hook.py
ruff check backend/security_layer/retrieval_acl/decision_observability.py backend/security_layer/tests/test_retrieval_acl_decision_observability.py
python scripts/portfolio/check_claim_boundary.py
git diff --check
```

## Expected audit event behavior

- `off` mode: no audit event is recorded.
- `shadow` mode: no audit event is recorded.
- `enforce` allowed decision: one redacted audit event is recorded with `decision="allowed"` and `reason="allowed"`.
- `enforce` cross-tenant denial: one redacted audit event is recorded with `decision="denied"` and `reason="tenant_mismatch"`.
- `enforce` missing-metadata fail-closed denial: one redacted audit event is recorded with `decision="denied"` and `reason="missing_acl_metadata"`.

## Expected telemetry counter behavior

- `off` mode: `allowed_count`, `denied_count`, and `fail_closed_count` remain unchanged.
- `shadow` mode: `allowed_count`, `denied_count`, and `fail_closed_count` remain unchanged.
- `enforce` allowed decision: `allowed_count` increments.
- `enforce` cross-tenant denial: `denied_count` increments.
- `enforce` missing-metadata fail-closed denial: `fail_closed_count` increments.

## Demo attack

Use the combined observability test `test_demo_attack_records_redacted_denial_event_and_denied_counter` as the focused demo attack proof:

- caller tenant: `tenant-a`;
- retrieved chunk tenant: `tenant-b`;
- mode: `enforce` with `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`;
- expected retrieval result: no returned chunks;
- expected audit result: one redacted denied event with `reason="tenant_mismatch"`;
- expected telemetry result: `denied_count == 1`, `allowed_count == 0`, and `fail_closed_count == 0`.

## Redaction requirements

Combined observability state must not store:

- chunk text;
- user prompts;
- raw document content;
- raw document bodies;
- raw document identifiers;
- secrets;
- credentials;
- PII.

Audit events store redacted decision metadata only. Telemetry snapshots store aggregate counters only.

## Safe claims

- Enforce-mode Retrieval ACL decisions can create redacted in-memory audit events.
- Enforce-mode Retrieval ACL decisions can update aggregate in-memory telemetry counters.
- Allowed, denied, and fail-closed enforce decisions are covered by focused tests.
- `off` and `shadow` modes do not record audit events or increment telemetry counters.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.
- Staging validation is not claimed.

## Forbidden claims

Do not claim:

- production readiness;
- enterprise readiness;
- staging validation;
- compliance certification;
- database persistence;
- Prometheus support;
- OpenTelemetry support;
- SIEM integration;
- dashboarding;
- alerting;
- durable monitoring;
- complete Onyx-wide authorization coverage;
- storage of chunk text, user prompts, raw document content, secrets, credentials, or PII.

## Rollback note

Rollback for this proof slice is to remove the enforce-mode call to `observe_retrieval_acl_decision`, remove `decision_observability.py`, and remove the combined proof tests and documentation. This returns enforce mode to the prior direct telemetry-counter proof behavior and removes the combined audit-event recording path.
