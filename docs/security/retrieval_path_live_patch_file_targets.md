# Retrieval Path Live Patch File Targets (Step 17D)

Candidate inventory for future monitor-only integration patches. No files listed below are modified in Step 17D.

| target ID | target area | candidate file/path | candidate function/class/route if known | confidence level | proposed future patch type | allowed mode for first patch | rollback note | evidence required | unknowns |
|---|---|---|---|---|---|---|---|---|---|
| LPT-001 | query entrypoint | `backend/onyx/server/query_and_chat/query_backend_models.py` | query request model orchestration points | medium | monitor-only hook call insertion | monitor-only only | remove/bypass hook call | request-to-hook invocation evidence | exact runtime entry function may differ |
| LPT-002 | subject context extraction | `backend/onyx/server/query_and_chat/` | auth subject extraction helpers | low | context builder adapter | monitor-only only | fallback to existing subject parsing | subject field completeness matrix | source-of-truth identity mapping uncertain |
| LPT-003 | tenant context extraction | `backend/onyx/server/` | tenant/workspace context resolvers | low | context builder adapter | monitor-only only | bypass tenant enrichment | tenant resolution evidence | multi-tenant path variance |
| LPT-004 | retrieval scope resolution | `backend/onyx/server/query_and_chat/` | retrieval scope derivation helpers | medium | non-blocking scope capture | monitor-only only | disable scope capture | scope decision logs | scope merge order not fully confirmed |
| LPT-005 | candidate source resolution | `backend/onyx/context/search/` | candidate source selection helpers | low | monitor-only candidate audit tap | monitor-only only | remove audit tap | candidate coverage sample | exact module/function unresolved |
| LPT-006 | vector query/namespace metadata path | `backend/onyx/document_index/` | vector query call sites | low | namespace metadata observation hook | monitor-only only | disable metadata capture | namespace metadata traces | backend variants may exist |
| LPT-007 | document ACL filtering | `backend/onyx/context/search/` | doc candidate filtering utilities | low | shadow comparator insertion (non-blocking) | monitor-only only | remove comparator | monitor vs baseline diff report | exact filter stage uncertain |
| LPT-008 | chunk ACL filtering | `backend/onyx/context/search/` | chunk pruning/filter utilities | low | shadow comparator insertion (non-blocking) | monitor-only only | remove comparator | chunk-level diff samples | chunk pipeline fan-out unknown |
| LPT-009 | hybrid search filtering | `backend/onyx/context/search/` | lexical/vector merge + filter logic | low | monitor-only decision annotation | monitor-only only | remove annotation | hybrid path decision logs | merge-phase hook point uncertain |
| LPT-010 | rerank filtering | `backend/onyx/context/search/` | rerank post-processing boundaries | low | non-blocking post-rerank evaluation | monitor-only only | disable evaluation | rerank comparison report | rerank stage variant paths |
| LPT-011 | citation filtering | `backend/onyx/chat/` | citation selection/serialization paths | low | monitor-only citation policy check | monitor-only only | bypass check | citation non-leakage samples | multiple citation assemblers possible |
| LPT-012 | context assembly filtering | `backend/onyx/context/` | context assembly pipeline functions | low | monitor-only context filtering simulation | monitor-only only | bypass simulation | context payload comparison | exact context builder path uncertain |
| LPT-013 | prompt context filtering | `backend/onyx/chat/` | prompt construction helpers | low | monitor-only prompt context audit | monitor-only only | disable prompt audit | prompt redaction comparison | prompt templates vary by flow |
| LPT-014 | cache read path | `backend/onyx/` | retrieval/cache read helpers | low | monitor-only cache observation | monitor-only only | remove observation hook | cache-hit behavior comparison | cache layer topology uncertain |
| LPT-015 | audit/finding/metric path | `backend/onyx/` | telemetry emitters / metric counters | medium | monitor-only telemetry emission wiring | monitor-only only | disable emission path | structured event samples | sink ownership and schemas vary |
\n\n## Step 17E Update (2026-05-27)\n- Added first live retrieval monitor-only hook at  after existing retrieval guard result handling.\n- Mode is disabled by default (), and monitor_only is the only live-enabled behavior for this step.\n- Enforce mode remains NO-GO and is not wired into live retrieval path.\n- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.\n

## Step 17E Update (2026-05-27)
- Added first live retrieval monitor-only hook at `backend/onyx/context/search/retrieval/search_runner.py` after existing retrieval guard result handling.
- Mode is disabled by default (`default_retrieval_integration_config`), and monitor_only is the only live-enabled behavior for this step.
- Enforce mode remains NO-GO and is not wired into live retrieval path.
- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.
