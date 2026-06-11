# Audit Logging Inventory

## Purpose
Inventory audit/logging evidence for security-relevant RAG retrieval decisions.

## Commands or search methods used
- `rg -n -i "audit|logging|correlation|decision_id|retrieval_result" backend docs .github`
- Direct inspection of retrieval guard audit code and security-layer tests.

## Files found
- `backend/onyx/security_layer/retrieval_guard/guard.py`
- `backend/onyx/security_layer/audit/models.py`
- `backend/onyx/security_layer/audit/service.py`
- `backend/security_layer/tests/test_retrieval_acl_audit_events.py`
- `backend/security_layer/tests/test_retrieval_acl_decision_observability.py`
- `backend/security_layer/tests/test_retrieval_security_negative_cases.py`

## Relevant code paths found
- `apply_retrieval_acl_guard` records `retrieval_result_allowed`, `retrieval_result_observed_risky`, or `retrieval_result_denied` audit events.
- The guard includes tenant ID, user ID, session ID, decision ID, resource type/id, action, risk level, document ID, chunk ID, ACL state, and reason.
- The guard creates security decisions with evidence including a generated correlation ID.

## Findings
- Audit event code exists for post-retrieval guard decisions.
- Isolated security-layer tests cover audit-event behavior.

## Gaps
- This review did not prove durable production storage, retention, SIEM export, or correlation across the entire request lifecycle.
- This review did not prove audit events fire for all retrieval paths or all deployment modes.
- No live denied retrieval audit log was produced from a running Onyx deployment.

## Claim boundary
Audit-event code exists and isolated tests exist; production audit logging completeness is not proven.
