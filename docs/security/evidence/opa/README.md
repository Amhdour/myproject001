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
- `resource_chunk_id`
- `resource_tenant_id`
- `correlation_id`
- `fallback_used`

## Trace linkage

OpenTelemetry instrumentation for this same enforcement path is documented in `docs/security/evidence/opentelemetry/`. The decision span `security.opa.retrieval_acl.decision` carries the same correlation, subject, resource, policy, decision, reason, fallback, and enforcement metadata needed to link traces back to OPA decision evidence without exporting raw chunk text.

## Evidence documents

- [CI validation results](ci_validation_results.md) records the observed GitHub Actions result for the OPA policy validation workflow.
- [Reproduction commands](reproduction_commands.md) lists local commands for reproducing OPA CLI validation.
- [Limitations](limitations.md) documents known scope boundaries and environment limitations.
