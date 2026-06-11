# RAG Flow Inventory

## Purpose
Map the confirmed RAG flow from ingestion through answer generation using repository evidence only.

## Commands or search methods used
- `rg -n "search_pipeline|search_chunks|chunker.chunk|embed_and_stream|write_chunks_to_vector_db_with_backoff|convert_inference_sections_to_llm_string" backend/onyx`
- Direct inspection of indexing, retrieval, search-tool, and prompt/citation utility files.

## Files found
- `backend/onyx/indexing/indexing_pipeline.py`
- `backend/onyx/indexing/models.py`
- `backend/onyx/document_index/vespa/indexing_utils.py`
- `backend/onyx/context/search/pipeline.py`
- `backend/onyx/context/search/retrieval/search_runner.py`
- `backend/onyx/tools/tool_implementations/search/search_tool.py`
- `backend/onyx/tools/tool_implementations/utils.py`
- `backend/onyx/chat/llm_step.py`

## Relevant code paths found
- `index_doc_batch` filters documents, prepares DB state, chunks documents, optionally adds contextual RAG summaries, embeds chunks, enriches chunk metadata, and writes chunks to the configured document indexes.
- `search_pipeline` builds filters, calls `search_chunks`, applies EE post-query censoring if present, and applies a real-path retrieval ACL hook.
- `search_chunks` runs federated and/or indexed retrieval, combines results, applies security enforcement/guards, and returns filtered chunks.
- `SearchTool._run_search_for_query` invokes `search_pipeline`; later search-tool code converts selected/expanded sections to an LLM-facing JSON string.
- `llm_step.py` streams the LLM response and passes answer tokens through the citation processor when configured.

## Findings
- The repository supports ingestion, chunking, embedding, vector-index writes, retrieval, context construction, answer streaming, and citation post-processing.
- Retrieval has multiple security hooks, including built index filters, post-retrieval guard code, portfolio/security-layer runtime checks, monitor-only hooks, and optional runtime enforcement.

## Gaps
- This inventory did not prove that every security hook is enabled in all deployment modes.
- This inventory did not prove runtime behavior against live services.

## Claim boundary
This supports a code-path mapping claim only. It does not prove end-to-end production enforcement or staging validation.
