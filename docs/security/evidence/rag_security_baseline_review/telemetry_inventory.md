# Telemetry Inventory

## Purpose
Inventory telemetry/metrics evidence for RAG retrieval security.

## Commands or search methods used
- `rg -n -i "telemetry|metric|counter|trace|retrieval_acl|denied" backend docs .github`
- Direct inspection of security-layer telemetry tests and runtime metrics references.

## Files found
- `backend/security_layer/tests/test_retrieval_acl_telemetry.py`
- `backend/security_layer/tests/test_retrieval_acl_telemetry_counters.py`
- `backend/security_layer/tests/test_runtime_audit_findings_metrics.py`
- `backend/tests/security/test_security_metrics.py`
- `.github/workflows/retrieval-acl-telemetry-tests.yml`
- `backend/onyx/tracing/flows.py`

## Relevant code paths found
- Retrieval ACL telemetry tests exist in the isolated `backend/security_layer/tests` suite.
- Project instructions require LLM/embedding/rerank/image/voice/intent calls to use tagged generation spans.
- Security-readiness workflows include security metrics tests under `backend/tests/security`.

## Findings
- There is evidence of isolated telemetry/metrics tests for retrieval ACL controls.
- There is tracing infrastructure guidance for LLM and embedding calls.

## Gaps
- This review did not prove production metrics export, dashboards, alerting, or metric cardinality controls.
- This review did not prove metrics for every requested category: cross-tenant attempts, prompt injection attempts, stale permission hits, deleted document retrieval attempts, citation mismatch, policy decision latency, or demo attack results in production.

## Claim boundary
Telemetry tests and tracing conventions exist; production telemetry completeness is not proven.
