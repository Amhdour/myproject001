# Citation Integrity Inventory

## Purpose
Inventory evidence for citation-source mapping and gaps around unauthorized citation leakage.

## Commands or search methods used
- `rg -n -i "citation|source|provenance" backend docs .github`
- Direct inspection of citation processor, citation utilities, search tool, and citation unit tests.

## Files found
- `backend/onyx/chat/citation_processor.py`
- `backend/onyx/chat/citation_utils.py`
- `backend/onyx/tools/tool_implementations/search/search_tool.py`
- `backend/onyx/tools/tool_implementations/utils.py`
- `backend/tests/unit/onyx/chat/test_citation_processor.py`
- `backend/tests/unit/onyx/chat/test_citation_utils.py`
- `backend/security_layer/tests/test_retrieval_security_negative_cases.py`

## Relevant code paths found
- `convert_inference_sections_to_llm_string` assigns citation IDs per document ID and returns a citation mapping.
- `SearchDocsResponse` includes search docs and citation mapping.
- `DynamicCitationProcessor` maps streamed citation markers to `SearchDoc` objects and emits citation events in hyperlink mode.
- `collapse_citations` re-numbers citations while preserving/merging mappings by document ID.

## Findings
- Citation mapping is tied to SearchDoc/document IDs generated from selected retrieved sections.
- Isolated tests exist for citation processor/utilities and security fixtures include a denied citation fixture.

## Gaps
- This review did not find or execute a full integration test proving unauthorized citations cannot leak after retrieval filtering in a live RAG answer.
- Citation code maps citations; it is not by itself a permission enforcement mechanism.

## Claim boundary
Citation mapping exists; full citation integrity and unauthorized citation leakage prevention are not proven.
