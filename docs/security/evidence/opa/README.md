# OPA Retrieval ACL Evidence

This evidence bundle documents a small Open Policy Agent (OPA) policy-as-code decision layer for **Retrieval ACL only**. The policy decides whether a retrieved document chunk may enter final RAG context for the action `rag.context.include`.

## Scope

- Runtime adapter code: `backend/onyx/security_layer/opa/`
- Rego policy: `backend/onyx/security_layer/policy/opa/retrieval_acl.rego`
- Rego tests: `backend/onyx/security_layer/policy/opa/tests/retrieval_acl_test.rego`
- Demo attack: `scripts/security/demo_attacks/opa/retrieval_acl_policy_bypass_demo.py`

This bundle does not claim production readiness and does not integrate OPA across every tool or security surface.

## Security invariant

A retrieved chunk must not enter final RAG context unless the acting user is authorized for the chunk/document tenant, user/group permissions, and the source is not deleted or stale.

## Decision evidence fields

OPA Retrieval ACL decision evidence uses:

- `event_type = "security.opa.retrieval_acl.decision"`
- `decision`
- `reason`
- `policy_package`
- `policy_version`
- `subject_user_id`
- `subject_tenant_id`
- `resource_document_id`
- `resource_tenant_id`
- `correlation_id`
- `fallback_used`
