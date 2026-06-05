# Retrieval ACL Audit Event Persistence Runbook

## Scope

Use this runbook to reproduce the Step 09 Retrieval ACL audit-event persistence proof.

This runbook covers only redacted audit-event construction and a minimal in-memory audit sink for focused tests. It does not cover database persistence, durable audit logging, production readiness, enterprise readiness, staging validation, compliance certification, or full Onyx-wide authorization coverage.

## How to run tests

From the repository root, run:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_audit_events.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/audit_events.py backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/retrieval_acl/metadata_adapter.py
ruff check backend/security_layer/retrieval_acl/audit_events.py backend/security_layer/tests/test_retrieval_acl_audit_events.py
python scripts/portfolio/check_claim_boundary.py
git diff --check
```

If Python dependencies are missing, activate the project virtual environment first:

```bash
source .venv/bin/activate
```

## Expected event fields

A `RetrievalACLAuditEvent` should include only:

- `event_type`: `retrieval_acl.decision`;
- `control_id`: `retrieval-acl-enforcement-v1`;
- `policy_version`;
- `mode`;
- `decision`: `allowed` or `denied`;
- `reason`;
- `user_tenant_id`;
- `chunk_tenant_id`;
- `document_ref`: redacted document reference only;
- `production_readiness`: `NO-GO`;
- `enterprise_readiness`: `NO-GO`.

## Redaction requirements

Audit events must not store or serialize:

- chunk text;
- user prompts;
- raw document bodies;
- raw document content;
- secrets;
- credentials;
- PII.

The proof-only in-memory sink must store audit event objects only. Do not store source chunks, prompt objects, document bodies, connector credentials, or user profile details in the sink.

## Safe claims

- Retrieval ACL decisions can be converted into redacted reviewer-safe audit events.
- Denied enforce-mode demo attack decisions can produce `retrieval_acl.decision` audit events.
- The in-memory sink can record, return, and clear events for focused tests.
- Enforce behavior remains gated behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.
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
- storage of chunk text, user prompts, raw document content, secrets, credentials, or PII.

## Rollback note

This proof slice is isolated to the audit-event module, focused tests, and documentation. To roll back, remove `backend/security_layer/retrieval_acl/audit_events.py`, remove `backend/security_layer/tests/test_retrieval_acl_audit_events.py`, and remove the Step 09 evidence and runbook files. No database migration or durable storage rollback is required because this step adds no database persistence.
