# Retrieval Path Inventory (Design)

- Query entrypoint candidates: API chat/search routes, retrieval orchestration boundaries.
- Subject/tenant context candidates: auth principal extractors and tenant-resolution helpers.
- Search pipeline candidates: scope resolution, source resolution, vector query assembly, metadata filters.
- Ranking/context candidates: hybrid merge, rerank input/output, citation assembly, context assembly, prompt construction.
- Cache candidate: retrieval cache read path requiring ACL revalidation before payload return.
- Audit/evidence candidates: decision audit emitter, finding record writer, security metric emitter.

This inventory is design-only and requires implementation-time code-point confirmation.
