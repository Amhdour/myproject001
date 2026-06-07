# Step 11 — Retrieval ACL Audit + Telemetry Combined Proof

## Scope

This step adds a focused, in-memory portfolio technical proof that each `enforce`-mode Retrieval ACL decision can produce both a redacted audit event and an aggregate telemetry counter update.

The proof covers allowed, denied, and fail-closed decisions. It preserves `off`, `shadow`, and `enforce` behavior: `off` and `shadow` modes do not record audit events or increment telemetry counters, while `enforce` mode remains gated behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.

This step does not add production readiness, enterprise readiness, staging validation, database persistence, Prometheus, OpenTelemetry, SIEM integration, compliance certification, or durable monitoring.

## Files created

- `backend/security_layer/retrieval_acl/decision_observability.py`
- `backend/security_layer/tests/test_retrieval_acl_decision_observability.py`
- `docs/security/evidence/step_11_retrieval_acl_audit_telemetry_combined_proof.md`
- `docs/security/evidence/step_11_retrieval_acl_audit_telemetry_combined_proof_summary.md`
- `docs/security/runbooks/retrieval_acl_audit_telemetry_combined_runbook.md`

## Files modified

- `backend/security_layer/retrieval_acl/enforce_hook.py`
- `backend/security_layer/retrieval_acl/audit_events.py`
- `backend/security_layer/tests/test_retrieval_acl_audit_events.py`

## Combined observability flow

1. `apply_retrieval_acl_enforcement_hook(...)` resolves the mode from configuration or `ONYX_SECURITY_RETRIEVAL_ACL_MODE`.
2. In `off` or `shadow` mode, the hook evaluates decisions for proof visibility but returns the original chunks and does not call the combined observability helper.
3. In `enforce` mode, each chunk is evaluated into a `RetrievalACLDecision`.
4. Each enforce-mode decision is passed to `observe_retrieval_acl_decision(decision)`.
5. `observe_retrieval_acl_decision` builds a redacted `RetrievalACLAuditEvent` from the decision.
6. The audit event is recorded in the in-memory audit sink.
7. The telemetry counters are incremented using only `decision.allowed` and `decision.reason`.
8. The helper returns the audit event for focused proof use.

## Audit event schema

`RetrievalACLAuditEvent` contains redacted decision metadata only:

| Field | Purpose |
| --- | --- |
| `event_type` | Constant Retrieval ACL event type. |
| `control_id` | Constant control identifier for Retrieval ACL Enforcement v1. |
| `policy_version` | Retrieval ACL policy version from the decision. |
| `mode` | Runtime mode, expected to be `enforce` for recorded events in this proof. |
| `decision` | `allowed` or `denied`. |
| `reason` | Coarse decision reason such as `allowed`, `tenant_mismatch`, or `missing_acl_metadata`. |
| `user_tenant_id` | Tenant boundary value used for the decision. |
| `chunk_tenant_id` | Tenant boundary value extracted from chunk metadata, or `missing` for fail-closed decisions. |
| `document_ref` | Redacted document reference, never the raw document body. |
| `production_readiness` | Constant `NO-GO` boundary marker. |
| `enterprise_readiness` | Constant `NO-GO` boundary marker. |

The audit event schema must not include chunk text, user prompts, raw document content, secrets, credentials, or PII.

## Telemetry counter schema

`RetrievalACLTelemetrySnapshot` stores aggregate counters only:

| Field | Purpose |
| --- | --- |
| `allowed_count` | Number of enforce-mode decisions where a same-tenant chunk was allowed. |
| `denied_count` | Number of enforce-mode non-fail-closed denials, including cross-tenant denials. |
| `fail_closed_count` | Number of enforce-mode denials caused by missing Retrieval ACL metadata. |
| `storage_scope` | Constant `in_memory_only` boundary marker. |
| `production_readiness` | Constant `NO-GO` boundary marker. |
| `enterprise_readiness` | Constant `NO-GO` boundary marker. |

Telemetry updates receive only `allowed` and `reason`. The telemetry snapshot must not include chunk text, user prompts, raw document content, raw document identifiers, secrets, credentials, or PII.

## Demo attack proof

The combined observability demo attack uses caller tenant `tenant-a` against a retrieved chunk tagged as `tenant-b` with sensitive chunk content and prompt bait. In `enforce` mode:

- the returned chunks list is empty;
- the Retrieval ACL decision reason is `tenant_mismatch`;
- one redacted denied audit event is recorded;
- `denied_count` increments by `1`;
- `allowed_count` and `fail_closed_count` remain `0`;
- the serialized audit and telemetry proof state excludes chunk content, prompt text, raw document content, credentials, secrets, and the raw document identifier.

## Test commands and results

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

Current local results for this branch:

- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_decision_observability.py -q` — passed, `8 passed`.
- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_audit_events.py -q` — passed, `7 passed`.
- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py -q` — passed, `8 passed`.
- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q` — passed, `17 passed`.
- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q` — passed, `7 passed`.
- `PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/decision_observability.py backend/security_layer/retrieval_acl/audit_events.py backend/security_layer/retrieval_acl/telemetry_counters.py backend/security_layer/retrieval_acl/enforce_hook.py` — passed.
- `ruff check backend/security_layer/retrieval_acl/decision_observability.py backend/security_layer/tests/test_retrieval_acl_decision_observability.py` — passed, `All checks passed!`.
- `python scripts/portfolio/check_claim_boundary.py` — passed, no unsafe positive readiness claims found.
- `git diff --check` — passed.

## Safe claims

- Enforce-mode Retrieval ACL decisions can record redacted in-memory audit events.
- Enforce-mode Retrieval ACL decisions can increment aggregate in-memory telemetry counters.
- Allowed same-tenant decisions can record an `allowed` audit event and increment `allowed_count`.
- Cross-tenant denials can record a redacted `denied` audit event and increment `denied_count`.
- Missing-metadata fail-closed denials can record a redacted denied audit event and increment `fail_closed_count`.
- `off` and `shadow` modes do not record audit events or increment counters.
- Chunk text, user prompts, raw document content, secrets, credentials, and PII are not stored by this proof slice.
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
- durable monitoring;
- alerting;
- complete Onyx-wide authorization coverage;
- storage of chunk text, user prompts, raw document content, secrets, credentials, or PII.

## Known limitations

- Audit events and counters are in-memory only and process-local.
- Observability state is cleared on process restart or by the test clear helpers.
- No database schema, migration, retention policy, export path, dashboard, alerting, authz boundary, or operational monitoring is added.
- No Prometheus, OpenTelemetry, SIEM, or compliance integration is added.
- This proof does not validate staging behavior.
- This proof does not prove complete tenant metadata availability for every real retrieval chunk.
- External review is required before changing readiness boundaries.

## Updated readiness percentages

These percentages are reviewer-facing portfolio estimates only, not production readiness claims.

- Production-style portfolio coverage: about `current separated readiness matrix` as a reviewer artifact only.
- Combined Retrieval ACL audit + telemetry proof: focused in-memory proof complete.
- Production readiness: `NO-GO / 0%`.
- Enterprise production-candidate readiness: `NO-GO / 8–10%`.
- Staging validation: not claimed / `0%`.
- Durable telemetry readiness: `NO-GO / 0%`.
- Durable audit persistence readiness: `NO-GO / 0%`.
