# Step 11 — Retrieval ACL Audit + Telemetry Combined Proof Summary

## Status

Focused portfolio technical-proof slice for combined Retrieval ACL audit events and telemetry counters is implemented in memory only.

Production readiness remains `NO-GO`. Enterprise readiness remains `NO-GO`. Staging validation is not claimed.

## What changed

- Added `observe_retrieval_acl_decision(decision)` to build a redacted audit event, record it in the in-memory audit sink, increment aggregate telemetry counters, and return the audit event.
- Updated enforce mode to call the combined observability helper instead of calling telemetry counters directly.
- Preserved `off` and `shadow` behavior: no audit events and no telemetry counter increments.
- Added combined tests for allowed, denied, fail-closed, off, shadow, demo attack redaction, no-go readiness boundaries, and chunk-content exclusion.
- Added evidence and runbook documentation for the combined proof.

## What tests prove

- Enforce allowed decisions record one redacted `allowed` audit event and increment `allowed_count`.
- Enforce cross-tenant denied decisions record one redacted `denied` audit event and increment `denied_count`.
- Enforce missing-metadata fail-closed decisions record one redacted denied audit event and increment `fail_closed_count`.
- `off` mode records no audit events and increments no counters.
- `shadow` mode records no audit events and increments no counters.
- The demo attack denial records a redacted denial event, increments `denied_count`, and excludes chunk content, prompt text, raw document content, secrets, credentials, and the raw document identifier from serialized observability state.
- Readiness markers remain `NO-GO` and no positive production or enterprise readiness marker is introduced.

## What is not claimed

- Production readiness is not claimed.
- Enterprise readiness is not claimed.
- Staging validation is not claimed.
- Compliance certification is not claimed.
- Database persistence is not added or claimed.
- Prometheus, OpenTelemetry, SIEM integration, dashboarding, alerting, and durable monitoring are not added or claimed.
- Storage of chunk text, user prompts, raw document content, secrets, credentials, or PII is not added or claimed.
- Complete Onyx-wide authorization coverage is not claimed.

## Remaining blockers

- Replace process-local in-memory observability with a reviewed durable audit and telemetry architecture before any production-oriented claim.
- Define retention, export, access control, alerting, monitoring, and incident-response requirements before operational use.
- Complete staging deployment review before any staging-oriented claim.
- Continue proving tenant metadata coverage across all relevant real retrieval paths.
- Obtain security and architecture review before changing `NO-GO` readiness boundaries.

## Updated readiness percentages

These percentages are reviewer-facing portfolio estimates only, not production readiness claims.

- Production-style portfolio coverage: about `current separated readiness matrix` as a reviewer artifact only.
- Combined Retrieval ACL audit + telemetry proof: focused in-memory proof complete.
- Production readiness: `NO-GO / 0%`.
- Enterprise production-candidate readiness: `NO-GO / 8–10%`.
- Staging validation: not claimed / `0%`.
- Durable telemetry readiness: `NO-GO / 0%`.
- Durable audit persistence readiness: `NO-GO / 0%`.
