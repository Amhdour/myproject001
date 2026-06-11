# Demo Attack Inventory

## Purpose
Inventory repository demo attacks relevant to RAG security.

## Commands or search methods used
- `rg -n -i "demo_attack|cross_tenant|prompt_injection|unauthorized|retrieval" backend demo_attacks docs .github`
- Direct inspection of security demo attack files and tests.

## Files found
- `backend/onyx/security_layer/demo_attacks/retrieval_unauthorized_doc_attempt.json`
- `backend/onyx/security_layer/demo_attacks/prompt_injection_tool_call.md`
- `backend/onyx/security_layer/demo_attacks/README.md`
- `backend/tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py`
- `backend/tests/security/demo_attacks/test_missing_tenant_retrieval_attack.py`
- `backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py`

## Relevant code paths found
- Cross-tenant retrieval demo attack test expects a DENY decision.
- Prompt-injection retrieved-content demo attack test expects ALLOW and records a limitation.
- Unauthorized retrieval JSON describes requesting tenant and document tenant mismatch with expected deny/audit/finding.

## Findings
- Demo attack evidence exists for cross-tenant retrieval and retrieved-content prompt-injection limitation.
- The requested cross-tenant test passed locally with system Python.
- The requested prompt-injection limitation test passed locally with system Python.

## Gaps
- No demo attack was found/executed for all requested categories: stale permission retrieval, deleted document retrieval in live RAG, citation leakage in live answer, source confusion, or data exfiltration attempt.
- JSON/markdown demo artifacts are not proof of live enforcement unless paired with executable tests or runtime evidence.

## Claim boundary
Demo attacks were inventoried and two tests were executed locally. Full demo attack coverage is not proven.
