# Step 09 — Retrieval ACL Audit Event Persistence Summary

## Status

Focused portfolio technical-proof slice for redacted Retrieval ACL audit-event persistence is implemented with an in-memory sink only.

Production readiness remains `NO-GO`. Enterprise readiness remains `NO-GO`. Staging validation is not claimed.

## What changed

- Added a `RetrievalACLAuditEvent` dataclass with a fixed `retrieval_acl.decision` event type and `retrieval-acl-enforcement-v1` control ID.
- Added `build_retrieval_acl_audit_event(decision)` to convert Retrieval ACL decisions into reviewer-safe audit events.
- Added in-memory sink helpers to record, read, and clear audit events in focused tests.
- Added tests proving allowed and denied decision conversion, redaction, sink behavior, demo attack denial auditing, and NO-GO readiness boundaries.
- Added an audit-event persistence runbook documenting test execution, redaction requirements, safe claims, forbidden claims, and rollback.

## What tests prove

The focused tests prove that:

- an allowed enforce-mode Retrieval ACL decision can produce an audit event;
- a denied enforce-mode Retrieval ACL decision can produce an audit event;
- serialized audit events do not include demo chunk text, user prompts, raw document bodies, secrets, credentials, or a demo email value;
- the in-memory sink records events and returns immutable snapshots;
- the in-memory sink clear helper removes recorded events;
- the demo attack with caller tenant `tenant-a` and chunk tenant `tenant-b` is denied in enforce mode and produces a redacted `retrieval_acl.decision` audit event;
- production and enterprise readiness fields remain `NO-GO`.

## What is not claimed

This step does not claim:

- production readiness;
- enterprise readiness;
- staging validation;
- compliance certification;
- database persistence;
- durable audit logging;
- full Onyx-wide authorization coverage;
- full Onyx-wide audit coverage;
- storage of chunk text, user prompts, raw document content, secrets, credentials, or PII.

## Remaining blockers

- Replace the proof-only in-memory sink with a reviewed durable audit persistence design before any production-oriented claim.
- Define retention, query, export, alerting, access-control, and operational monitoring requirements for any durable audit log.
- Validate end-to-end behavior through appropriate deployment and staging processes before any staging-oriented claim.
- Continue proving tenant metadata coverage across real retrieval paths.
- Obtain external review before changing readiness boundaries.

## Updated readiness percentages

These percentages are reviewer-facing portfolio estimates only, not production readiness claims.

- Production-style portfolio coverage: about `99%` as a reviewer artifact only.
- Retrieval ACL audit-event persistence proof: focused in-memory proof complete.
- Production readiness: `NO-GO / 0%`.
- Enterprise production-candidate readiness: `NO-GO / 7–9%`.
- Staging validation: not claimed / `0%`.
- Durable audit persistence readiness: `NO-GO / 0%`.
