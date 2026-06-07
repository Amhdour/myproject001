# Step 09 — Retrieval ACL Audit Event Persistence Proof

## Scope

This step adds a focused portfolio technical-proof slice for converting Retrieval ACL Enforcement v1 decisions into reviewer-safe audit events and storing those events in a minimal in-memory sink for tests.

This step does not add database persistence, production readiness, enterprise readiness, staging validation, compliance certification, or full Onyx-wide authorization coverage.

## Files created

- `backend/security_layer/retrieval_acl/audit_events.py`
- `backend/security_layer/tests/test_retrieval_acl_audit_events.py`
- `docs/security/evidence/step_09_retrieval_acl_audit_event_persistence.md`
- `docs/security/evidence/step_09_retrieval_acl_audit_event_persistence_summary.md`
- `docs/security/runbooks/retrieval_acl_audit_event_persistence_runbook.md`

## Audit event schema

`RetrievalACLAuditEvent` records only redacted decision metadata:

| Field | Purpose |
| --- | --- |
| `event_type` | Constant `retrieval_acl.decision`. |
| `control_id` | Constant `retrieval-acl-enforcement-v1`. |
| `policy_version` | Retrieval ACL policy version from the decision. |
| `mode` | Retrieval ACL mode that produced the decision. |
| `decision` | `allowed` or `denied`. |
| `reason` | Reviewer-safe reason code such as `allowed` or `tenant_mismatch`. |
| `user_tenant_id` | Caller tenant boundary used by the decision. |
| `chunk_tenant_id` | Retrieved chunk tenant boundary used by the decision. |
| `document_ref` | Redacted document reference only. |
| `production_readiness` | Must remain `NO-GO`. |
| `enterprise_readiness` | Must remain `NO-GO`. |

## Redaction rules

Audit events must never include:

- chunk text;
- user prompts;
- raw document bodies;
- raw document content;
- secrets;
- credentials;
- PII.

The event builder accepts an existing `RetrievalACLDecision`, which already carries only redacted decision metadata. The in-memory sink stores only `RetrievalACLAuditEvent` objects, not chunk objects or prompt objects.

## Test command

Focused Step 09 command:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_audit_events.py -q
```

Regression commands for the surrounding Retrieval ACL proof slice:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/audit_events.py backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/retrieval_acl/metadata_adapter.py
ruff check backend/security_layer/retrieval_acl/audit_events.py backend/security_layer/tests/test_retrieval_acl_audit_events.py
python scripts/portfolio/check_claim_boundary.py
git diff --check
```

## Demo attack audit event proof

The focused test `test_demo_attack_denial_produces_redacted_audit_event` uses this scenario:

- caller tenant: `tenant-a`;
- chunk tenant: `tenant-b`;
- mode: `enforce` via `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`;
- expected Retrieval ACL decision: denied;
- expected audit event type: `retrieval_acl.decision`;
- expected readiness fields: `production_readiness=NO-GO` and `enterprise_readiness=NO-GO`;
- expected redaction boundary: the demo chunk text is absent from the serialized audit event.

## Safe claims

- Enforce-mode Retrieval ACL decisions can be converted into redacted audit events.
- Denied cross-tenant decisions can produce reviewer-safe audit events.
- The focused in-memory sink can record, return, and clear audit events during tests.
- Off, shadow, and enforce behavior remains owned by the existing enforcement hook; enforce mode remains behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.
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
- durable audit storage;
- full Onyx-wide authorization coverage;
- full Onyx-wide audit coverage;
- storage of chunk text, user prompts, raw document bodies, secrets, credentials, or PII.

## Known limitations

- Persistence is in-memory only and is intended for focused tests.
- Events are not persisted to PostgreSQL, Redis, object storage, or any durable audit log.
- Events are lost when the Python process exits or the sink is cleared.
- No retention, export, alerting, query API, authentication boundary, or operational monitoring is added.
- This step does not prove complete tenant metadata availability for every real retrieval chunk.

## Status

- Step status: focused technical proof implemented locally.
- Production readiness: `NO-GO / 0%`.
- Enterprise readiness: `NO-GO` as a portfolio-review estimate only.
- Staging validation: not claimed / `0%`.
- Audit persistence durability: in-memory only / not durable.
