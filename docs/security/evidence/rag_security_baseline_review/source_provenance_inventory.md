# Source Provenance Inventory

## Purpose
Inventory source identity and provenance fields preserved through retrieval and citation flows.

## Commands or search methods used
- `rg -n -i "citation|source|provenance|document_id|connector_id|source_type|tenant_id" backend docs .github`
- Direct inspection of indexing models, Vespa hit conversion, search models, and retrieval guard provenance.

## Files found
- `backend/onyx/indexing/models.py`
- `backend/onyx/document_index/vespa/indexing_utils.py`
- `backend/onyx/document_index/vespa/chunk_retrieval.py`
- `backend/onyx/context/search/models.py`
- `backend/onyx/security_layer/retrieval_guard/provenance.py`
- `backend/onyx/security_layer/retrieval_guard/models.py`
- `backend/onyx/tools/tool_implementations/utils.py`

## Relevant code paths found
- Vespa document fields include `DOCUMENT_ID`, `CHUNK_ID`, `SOURCE_TYPE`, `SOURCE_LINKS`, `SEMANTIC_IDENTIFIER`, `METADATA`, owners, ACL, document sets, and tenant ID when multi-tenant.
- `_vespa_hit_to_inference_chunk` maps Vespa fields into `InferenceChunk` with document ID, chunk ID, source type, title, semantic identifier, owners, metadata, links, summary, context, and timestamps.
- `build_provenance` emits document ID, chunk ID, tenant ID, connector ID from metadata, source type, ACL state, permission source, user ID, session ID, decision, and reason.

## Findings
- Source/document/chunk identity is represented in both retrieved chunk models and LLM-facing/citation mapping flows.
- Retrieval guard provenance exists for post-retrieval decisions.

## Gaps
- Connector ID is obtained from chunk metadata in retrieval guard provenance; this review did not prove every retrieved chunk contains connector metadata.
- Tenant ID is represented in filters and security guard metadata, but this review did not prove every legacy/indexed chunk includes tenant metadata in all modes.

## Claim boundary
Provenance structures exist; complete provenance coverage for all sources is not proven.
