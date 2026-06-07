# Step 10 — Retrieval ACL Telemetry Counters Proof

## Scope

This step adds focused in-memory telemetry counters for Retrieval ACL Enforcement v1 decisions. The counters are incremented only from the enforce-mode decision loop and are intended as a reviewer-facing technical proof.

This step does not add production readiness, enterprise readiness, staging validation, OpenTelemetry, Prometheus, SIEM integration, dashboarding, durable monitoring, database persistence, or complete Onyx-wide authorization coverage.

## Files created

- `backend/security_layer/retrieval_acl/telemetry_counters.py`
- `backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py`
- `docs/security/evidence/step_10_retrieval_acl_telemetry_counters.md`
- `docs/security/evidence/step_10_retrieval_acl_telemetry_counters_summary.md`
- `docs/security/runbooks/retrieval_acl_telemetry_counters_runbook.md`

## Files modified

- `backend/security_layer/retrieval_acl/enforce_hook.py`

## Telemetry schema

`RetrievalACLTelemetrySnapshot` stores aggregate counters only:

| Field | Purpose |
| --- | --- |
| `allowed_count` | Number of enforce-mode decisions where a same-tenant chunk was allowed. |
| `denied_count` | Number of enforce-mode non-fail-closed denials, including cross-tenant denials. |
| `fail_closed_count` | Number of enforce-mode denials caused by missing Retrieval ACL metadata. |
| `storage_scope` | Constant `in_memory_only` boundary marker. |
| `production_readiness` | Constant `NO-GO` boundary marker. |
| `enterprise_readiness` | Constant `NO-GO` boundary marker. |

The counter module stores no chunk text, prompt text, raw document content, secrets, credentials, or PII. It receives only `allowed` and `reason` values from the enforce-mode hook.

## Test commands and results

Run from the repository root:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/telemetry_counters.py backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/retrieval_acl/metadata_adapter.py
ruff check backend/security_layer/retrieval_acl/telemetry_counters.py backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py
python scripts/portfolio/check_claim_boundary.py
git diff --check
```

Current local results are recorded in the Step 10 summary: all required commands passed in this branch.

## Demo attack counter proof

The focused test `test_demo_attack_denial_increments_denied_count_without_chunk_content` uses this scenario:

- caller tenant: `tenant-a`;
- chunk tenant: `tenant-b`;
- mode: `enforce` via `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`;
- expected Retrieval ACL decision: denied;
- expected counter effect: `denied_count` increments by `1`;
- expected redaction boundary: the demo chunk text, raw tenant value, and raw document identifier are absent from the serialized telemetry snapshot.

## Safe claims

- Enforce-mode Retrieval ACL decisions can increment in-memory aggregate counters.
- Allowed same-tenant enforce decisions can increment `allowed_count`.
- Cross-tenant enforce denials can increment `denied_count`.
- Missing-metadata enforce denials can increment `fail_closed_count`.
- Off and shadow modes do not increment these counters.
- The focused counters can be cleared and read in tests.
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
- full Onyx-wide authorization coverage;
- storage of chunk text, prompt text, raw document content, secrets, credentials, or PII.

## Known limitations

- Counters are in-memory only and process-local.
- Counters are lost when the Python process exits or the clear helper is called.
- No retention, export, alerting, query API, authentication boundary, dashboard, or operational monitoring is added.
- This proof does not validate staging behavior.
- This proof does not prove complete tenant metadata availability for every real retrieval chunk.
- Counter updates are intentionally minimal and are not a substitute for reviewed production telemetry architecture.

## Updated readiness percentages

These percentages are reviewer-facing portfolio estimates only, not production readiness claims.

- Production-style portfolio coverage: about `current separated readiness matrix` as a reviewer artifact only.
- Retrieval ACL telemetry counter proof: focused in-memory proof complete.
- Production readiness: `NO-GO / 0%`.
- Enterprise production-candidate readiness: `NO-GO / 8–10%`.
- Staging validation: not claimed / `0%`.
- Durable telemetry readiness: `NO-GO / 0%`.
