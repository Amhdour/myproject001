# Test Inventory

## Purpose
Inventory relevant RAG/retrieval/security tests and record local execution status.

## Commands or search methods used
- `find backend -path '*security_layer*tests*' -o -path '*tests*security*' | sort | head -n 300`
- `find backend -path '*test*retrieval*' -o -path '*test*acl*' -o -path '*test*citation*' | sort | head -n 300`
- Exact test executions recorded in `test_results.md`.

## Files found
- `backend/security_layer/tests/test_retrieval_acl_runtime.py`
- `backend/security_layer/tests/test_retrieval_security_negative_cases.py`
- `backend/security_layer/tests/test_retrieval_acl_telemetry.py`
- `backend/security_layer/tests/test_retrieval_acl_search_pipeline_seam.py`
- `backend/security_layer/tests/test_retrieval_acl_real_search_pipeline_noop_hook.py`
- `backend/tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py`
- `backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py`
- `backend/tests/unit/onyx/chat/test_citation_processor.py`
- `backend/tests/unit/onyx/chat/test_citation_utils.py`
- `backend/tests/integration/common_utils/document_acl.py`

## Relevant code paths found
- Isolated retrieval ACL runtime tests cover allow, deny, cross-tenant denial, mixed filtering, missing/malformed context, and audit event creation.
- Negative-case tests cover monitor-only fixtures for cross-tenant, unauthorized group, stale ACL, deleted document, vector namespace/metadata mismatch, cache and citation denied fixtures, and non-leakage of raw text/secrets.
- Demo attack tests cover cross-tenant retrieval attack and prompt-injection retrieved-content limitation.

## Findings
- Locally executed with system Python: retrieval ACL runtime tests passed, retrieval negative-case tests passed, cross-tenant demo attack test passed, prompt-injection limitation demo attack test passed.
- Initial venv-based pytest attempts were not executable because `.venv/bin/python` did not have pytest installed.

## Gaps
- Full backend unit, external-dependency, integration, Playwright, and live service tests were not executed.
- Passing isolated tests do not prove production security or live Onyx enforcement.

## Claim boundary
Only the exact commands and outcomes in `test_results.md` may be claimed as locally executed.
