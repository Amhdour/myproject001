# Context Builder Summary

`context_builder.py` provides isolated builders for:
- subject and tenant context
- `RetrievalACLContext` construction
- safe metadata candidate construction

Safety behavior:
- rejects `document_text`, `chunk_text`, `source_secret` and other sensitive/raw content keys
- handles missing subject and tenant safely via nullable fields
- builds `RetrievalCandidate` objects compatible with existing isolated retrieval controls
- does not perform live search/vector/cache calls
