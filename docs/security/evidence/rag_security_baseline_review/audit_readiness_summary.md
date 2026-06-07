# Audit Readiness Summary

## Purpose
Summarize current audit-readiness evidence for RAG security.

## Commands or search methods used
- Consolidated from all evidence files and local test execution.

## Files found
- `docs/security/rag_security_baseline_review.md`
- All files under `docs/security/evidence/rag_security_baseline_review/`

## Relevant code paths found
- Ingestion/indexing: `backend/onyx/indexing/indexing_pipeline.py`, `backend/onyx/document_index/vespa/indexing_utils.py`.
- Retrieval: `backend/onyx/context/search/pipeline.py`, `backend/onyx/context/search/retrieval/search_runner.py`.
- ACL/security: `backend/onyx/access/*`, `backend/onyx/security_layer/retrieval_guard/*`, `backend/security_layer/tests/*`.
- Prompt/citation: `backend/onyx/tools/tool_implementations/*`, `backend/onyx/chat/citation_*`.

## Findings
- Review completeness is moderate because major RAG/security paths were mapped.
- Evidence completeness is limited because only repository/local test evidence was captured.
- Test coverage confidence is limited to isolated/security tests executed locally.
- Demo attack confidence is limited to found and executed demo attack tests; coverage is not comprehensive.
- CI gate confidence is low-to-moderate because workflow definitions exist, but pass status is not confirmed.
- Staging and production/security-audit readiness are low because no staging/deployment/external audit evidence was found.

## Gaps
See `security_gap_register.md` and `production_readiness_limitations.md`.

## Claim boundary
Audit-readiness estimates are conservative and based only on this repository and local commands.
