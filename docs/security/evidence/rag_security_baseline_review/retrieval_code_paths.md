# Retrieval Code Paths

## Purpose
Document confirmed retrieval code paths and seam points relevant to RAG security.

## Commands or search methods used
- `rg -n "def search_pipeline|def search_chunks|hybrid_retrieval|keyword_retrieval|id_based_retrieval|apply_retrieval_acl_guard|apply_retrieval_acl_real_path_enforcement_hook" backend/onyx backend/security_layer`
- Direct inspection of retrieval pipeline, Vespa retrieval, and security-layer retrieval tests.

## Files found
- `backend/onyx/context/search/pipeline.py`
- `backend/onyx/context/search/retrieval/search_runner.py`
- `backend/onyx/document_index/vespa/chunk_retrieval.py`
- `backend/onyx/document_index/vespa/shared_utils/vespa_request_builders.py`
- `backend/onyx/context/search/preprocessing/access_filters.py`
- `backend/security_layer/tests/test_retrieval_acl_search_pipeline_seam.py`
- `backend/security_layer/tests/test_retrieval_acl_runtime.py`

## Relevant code paths found
- `search_pipeline(...)` builds `IndexFilters` and calls `search_chunks(...)`.
- `_embed_and_hybrid_search(...)` computes a query embedding and calls `document_index.hybrid_retrieval(...)`.
- `_keyword_search(...)` calls `document_index.keyword_retrieval(...)`.
- `search_chunks(...)` combines federated and indexed retrieval results, then applies runtime/ACL guard code before returning chunks.
- Vespa visit/id-based retrieval code applies tenant and ACL checks when filters contain those values.

## Findings
- The normal indexed retrieval path is ACL-aware through `IndexFilters.access_control_list` and Vespa filter construction.
- The search runner also includes post-retrieval guard calls for retrieved chunks.
- There is a separate `inference_sections_from_ids` helper that sets `IndexFilters(access_control_list=None)` with a comment saying doc IDs were validated beforehand; this review did not trace all callers to prove that invariant globally.

## Gaps
- No live Vespa query was executed.
- No full integration test was executed to prove live retrieval behavior.
- Some retrieval security tests are isolated helper tests rather than full Onyx deployment tests.

## Claim boundary
Code exists for ACL-aware retrieval and post-retrieval guard seams. Production behavior is not proven without live integration/staging evidence.
