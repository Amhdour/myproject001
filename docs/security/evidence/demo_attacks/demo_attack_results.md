# Demo Attack Results

Generated from deterministic pytest demo attack cases.

## cross-tenant retrieval attempt
- Threat: tenant isolation bypass via retrieved chunk metadata
- Expected blocked behavior: deny
- Actual decision: deny
- Evidence: `backend/tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py`
- Limitation: service-level demo plus retrieval hook patch; not a live deployed route test

## missing-tenant retrieval attempt
- Threat: retrieval without tenant context
- Expected blocked behavior: deny
- Actual decision: deny
- Evidence: `backend/tests/security/demo_attacks/test_missing_tenant_retrieval_attack.py`
- Limitation: service-level demo; live API deployment not exercised

## high-risk tool execution without approval
- Threat: unsafe autonomous tool action
- Expected blocked behavior: approval_required
- Actual decision: approval_required
- Evidence: `backend/tests/security/demo_attacks/test_high_risk_tool_without_approval.py`
- Limitation: generic tool policy path; not wired to every production tool executor

## prompt injection in retrieved content
- Threat: malicious retrieved text attempts instruction override
- Expected blocked behavior: not implemented
- Actual decision: allow
- Evidence: `backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py`
- Limitation: content scanning for prompt injection is documented as not yet implemented by this MVP

## unsafe sandbox action
- Threat: critical sandbox command execution
- Expected blocked behavior: approval_required
- Actual decision: approval_required
- Evidence: `backend/tests/security/demo_attacks/test_unsafe_artifact_or_sandbox_action.py`
- Limitation: policy decision tested; not wired to every sandbox launch path
