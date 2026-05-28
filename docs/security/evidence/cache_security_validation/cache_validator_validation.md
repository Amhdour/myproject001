# Cache validator validation
- Missing tenant/subject/ACL/provenance paths deny safely.
- Invalid cache key and invalid cache metadata paths deny safely.
- Stale ACL/deleted-or-stale/drift/poisoning/injection markers validated as flaggable.
- Decision reason redaction validated for query/prompt/document/chunk terms.
