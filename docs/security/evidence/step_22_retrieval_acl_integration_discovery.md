# Step 22 Retrieval ACL Integration-Point Discovery

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T16:25:00Z |
| Branch name | `step-22-retrieval-acl-integration-discovery` |
| Base branch | `main` |
| Starting commit SHA | `9ed7cb7040b0f639e715fe9c5db3e608fb904a76` |
| Step 21 dependency | `RETRIEVAL_ACL_RUNTIME_HELPER_PROVEN_BY_CI` pending merge of PR #150 |

## Objective

Step 22 discovers candidate integration points where the isolated Step 21 Retrieval ACL runtime helper could later be wired into real Onyx retrieval/search paths.

This step is discovery-only. It does not wire the helper into live request paths and does not claim production retrieval security.

## Files inspected

```text
backend/onyx/context/search/models.py
backend/onyx/context/search/pipeline.py
backend/onyx/tools/tool_implementations/search/search_tool.py
```

## Existing ACL-related structures discovered

### Search filters carry ACL and tenant fields

`backend/onyx/context/search/models.py` defines `IndexFilters` with:

```text
access_control_list: list[str] | None
tenant_id: str | None = None
```

This means the existing search pipeline already has a filter-level ACL/tenant concept before chunks are retrieved.

### Search requests can bypass ACL

`ChunkSearchRequest` includes:

```text
bypass_acl: bool = False
```

This is important because any future runtime helper integration must preserve legitimate system bypass behavior while preventing accidental user-path bypasses.

### Retrieved chunks expose document IDs

`InferenceChunk` includes:

```text
document_id: str
```

This is a useful candidate mapping field for post-retrieval runtime filtering, but `InferenceChunk` does not directly include full `RetrievalDocumentACL` metadata required by the isolated Step 21 helper.

## Candidate integration point A — filter construction before retrieval

### File

```text
backend/onyx/context/search/pipeline.py
```

### Function

```text
_build_index_filters(...)
```

### Why it matters

This function builds `IndexFilters`, including `access_control_list` and `tenant_id`, before search execution.

It already:

- validates requested document-set access when a database session is available;
- calls `build_access_filters_for_user(user, db_session)` when ACLs are not bypassed;
- sets tenant ID with `get_current_tenant_id()` when multi-tenant mode is enabled.

### Security role

This is the pre-retrieval filter gate. It is probably the existing first-line ACL boundary.

### Step 22 recommendation

Do not replace this path with the Step 21 helper. Instead, treat it as the upstream source of truth for filter construction and later prove that user paths do not bypass it accidentally.

## Candidate integration point B — immediately after `search_chunks(...)`

### File

```text
backend/onyx/context/search/pipeline.py
```

### Function

```text
search_pipeline(...)
```

### Exact point

After:

```text
retrieved_chunks = search_chunks(...)
```

and before:

```text
fetch_ee_implementation_or_noop("onyx.external_permissions.post_query_censoring", ...)
```

### Why it matters

This is the first point where real retrieved `InferenceChunk` objects exist after vector/search retrieval and before the search pipeline returns chunks to callers.

### Security role

This is the strongest candidate for a future post-retrieval runtime ACL guard because it can fail closed or filter retrieved results before downstream LLM selection, UI conversion, or prompt construction.

### Current blocker

The Step 21 helper expects isolated `RetrievalResultChunk` objects with explicit `RetrievalDocumentACL` metadata. Real `InferenceChunk` objects include `document_id` and tenant/search metadata but do not obviously include full document ACL metadata in the inspected file.

A future integration step needs an adapter that can map `InferenceChunk` plus existing ACL/tenant context into the Step 21 helper model, or a new helper path designed for `InferenceChunk` directly.

## Candidate integration point C — enterprise post-query censoring hook

### File

```text
backend/onyx/context/search/pipeline.py
```

### Existing hook

```text
fetch_ee_implementation_or_noop(
    "onyx.external_permissions.post_query_censoring",
    "_post_query_chunk_censoring",
    retrieved_chunks,
)(chunks=retrieved_chunks, user=user)
```

### Why it matters

This existing post-query hook already represents a post-retrieval censoring boundary for connector-specific field/object permissions.

### Security role

It is a good architectural reference point for runtime post-retrieval filtering, but it appears to depend on enterprise extension behavior and should not be assumed available in the open-source runtime.

### Step 22 recommendation

Use this hook as architectural evidence that post-query censoring is a recognized design point. Do not claim the Step 21 helper is integrated there.

## Candidate integration point D — search tool query fanout and recombination

### File

```text
backend/onyx/tools/tool_implementations/search/search_tool.py
```

### Relevant flow

`SearchTool.run(...)`:

- prefetches ACL filters with `build_access_filters_for_user(self.user, db_session)` unless `bypass_acl` is enabled;
- runs multiple search queries in parallel via `_run_search_for_query(...)`;
- recombines returned chunks with weighted reciprocal rank fusion;
- converts chunks into sections;
- emits selected documents and later builds LLM-facing context.

### Why it matters

This is a high-risk downstream surface: if unauthorized chunks survive earlier retrieval/filtering, they can be recombined, selected, emitted, expanded, and added to LLM-facing context.

### Security role

This is not the first choice for Step 21 helper integration because it is later in the flow and has more complex LLM/UI behavior. However, it is a critical proof target for future end-to-end tests.

### Step 22 recommendation

Future integration tests should prove unauthorized chunks cannot reach:

- weighted RRF recombination;
- `merge_individual_chunks(...)`;
- `convert_inference_sections_to_search_docs(...)`;
- `select_sections_for_expansion(...)`;
- `convert_inference_sections_to_llm_string(...)`.

## Candidate integration ranking

| Rank | Candidate | File/function | Reason |
| --- | --- | --- | --- |
| 1 | Post-`search_chunks` runtime guard | `backend/onyx/context/search/pipeline.py::search_pipeline` | First post-retrieval point before chunks return to callers. |
| 2 | Filter construction hardening/proof | `backend/onyx/context/search/pipeline.py::_build_index_filters` | Existing pre-retrieval ACL and tenant filter boundary. |
| 3 | Existing post-query censoring hook | `fetch_ee_implementation_or_noop(...post_query_censoring...)` | Existing architectural post-retrieval censoring pattern. |
| 4 | Search tool downstream proof | `backend/onyx/tools/tool_implementations/search/search_tool.py::run` | Needed to prove unauthorized chunks cannot reach UI/LLM context. |

## Non-goals for Step 22

Step 22 does not:

- modify runtime code;
- wire Step 21 helper into Onyx retrieval;
- change search behavior;
- claim live enforcement;
- claim production retrieval security;
- claim enterprise readiness;
- claim full tenant isolation.

## Safe claims

- Step 22 identifies candidate retrieval ACL integration points.
- The strongest candidate is a post-`search_chunks` guard in `search_pipeline`.
- The existing pipeline already has pre-retrieval ACL/tenant filters and a post-query censoring pattern.
- Further implementation requires an adapter from real `InferenceChunk`/ACL context to the Step 21 helper model or a dedicated `InferenceChunk` runtime guard.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim Step 21 is wired into live Onyx retrieval.
- Do not claim production retrieval security.
- Do not claim complete RAG authorization.
- Do not claim enterprise readiness.
- Do not claim live tenant isolation.
- Do not claim full backend test success.

## Recommended Step 23

Step 23 should build an isolated adapter proof for real Onyx-like `InferenceChunk` objects:

```text
InferenceChunk + requester/search ACL context -> RetrievalResultChunk-compatible authorization decision
```

This should still be isolated test proof first. Only after that should a later step consider wiring into `search_pipeline` behind a safe flag or shadow-mode wrapper.
