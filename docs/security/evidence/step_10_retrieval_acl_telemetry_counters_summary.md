# Step 10 — Retrieval ACL Telemetry Counters Summary

## Status

Focused portfolio technical-proof slice for Retrieval ACL telemetry counters is implemented with in-memory counters only.

Production readiness remains `NO-GO`. Enterprise readiness remains `NO-GO`. Staging validation is not claimed.

## What changed

- Added a `RetrievalACLTelemetrySnapshot` dataclass with aggregate `allowed_count`, `denied_count`, and `fail_closed_count` values.
- Added helpers to record, read, and clear process-local Retrieval ACL telemetry counters.
- Updated the enforce-mode decision loop to record telemetry counter updates only in enforce mode.
- Added tests proving enforce-only counter behavior, allowed/cross-tenant/fail-closed increments, clear behavior, demo attack redaction, and NO-GO boundaries.
- Added a telemetry counter runbook documenting test execution, safe claims, forbidden claims, and rollback.

## Test commands and results

- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py -q` — passed, `8 passed`.
- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q` — passed, `17 passed`.
- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q` — passed, `7 passed`.
- `PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/telemetry_counters.py backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/retrieval_acl/metadata_adapter.py` — passed.
- `ruff check backend/security_layer/retrieval_acl/telemetry_counters.py backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py` — passed, `All checks passed!`.
- `python scripts/portfolio/check_claim_boundary.py` — passed, no unsafe positive readiness claims found.
- `git diff --check` — passed.

## Demo attack counter proof

The focused demo attack test uses caller tenant `tenant-a` against a retrieved chunk tagged as `tenant-b`. In enforce mode, the decision is denied and `denied_count` increments by `1`. The serialized snapshot contains aggregate counters and boundary markers only; it does not contain demo chunk content, the raw tenant value, or the raw document identifier.

## Safe claims

- Enforce-mode Retrieval ACL decisions can update aggregate in-memory counters.
- Off and shadow modes do not update these counters.
- Missing metadata increments `fail_closed_count`.
- Cross-tenant denial increments `denied_count`.
- Allowed same-tenant decision increments `allowed_count`.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.
- Staging validation is not claimed.

## Forbidden claims

This step does not claim:

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

## Remaining blockers and known limitations

- Replace process-local counters with a reviewed telemetry architecture before any production-oriented claim.
- Define retention, export, alerting, access-control, and operational requirements before any operational telemetry claim.
- Validate behavior through appropriate deployment review before any staging-oriented claim.
- Continue proving tenant metadata coverage across real retrieval paths.
- Obtain external review before changing readiness boundaries.

## Updated readiness percentages

These percentages are reviewer-facing portfolio estimates only, not production readiness claims.

- Production-style portfolio coverage: about `99%` as a reviewer artifact only.
- Retrieval ACL telemetry counters proof: focused in-memory proof complete.
- Production readiness: `NO-GO / 0%`.
- Enterprise production-candidate readiness: `NO-GO / 8–10%`.
- Staging validation: not claimed / `0%`.
- Durable telemetry readiness: `NO-GO / 0%`.
