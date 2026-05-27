# Retrieval Path Patching Design (Step 17A)

## purpose
Define a design-only plan to patch live retrieval execution paths with retrieval ACL security hooks in a controlled rollout sequence without changing runtime behavior in this step.

## scope
- Documentation/design/test-planning only.
- No production wiring or enforcement activation.

## status
planned/design

## owner
AI Trust & Security Readiness Engineer

## non-claim statement
This document does not claim production readiness, control effectiveness, or live enforcement. No runtime retrieval path is patched in Step 17A.

## relationship to isolated retrieval ACL controls
Uses isolated controls in `backend/security_layer/retrieval/` as the intended security decision primitives for future integration.

## relationship to runtime wrappers
Runtime wrapper design (`docs/security/runtime_context_wrappers.md`) is treated as a composition layer around these patch points for decision capture, mode selection, and fail-closed behavior.

## relationship to safe denial behavior
All deny outcomes map to safe-denial categories and response constraints in `docs/security/safe_denial_behavior.md`.

## relationship to patch-point mapping
Patch candidates map to retrieval/security patch points in `docs/security/patch_points.md`.

## live retrieval path inventory
See `docs/security/evidence/retrieval_path_patching_design/retrieval_path_inventory.md` for route/service/query-stage inventory and candidate hook locations.

## patch candidate catalog
| ID | target area | candidate file/path | candidate function/class/route if known | existing behavior summary | planned security hook | planned retrieval ACL control | required context fields | safe denial behavior | monitor-only behavior | shadow-deny behavior | enforce-mode behavior | mapped risks | mapped requirements | mapped patch points | planned tests | rollback note | confidence | implementation status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RPC-001 | query received | backend/onyx/server/query_and_chat | chat/search entry routes | Query is accepted and forwarded into retrieval stack. | Add pre-retrieval decision wrapper invocation. | `build_retrieval_acl_context` + `evaluate_query_scope` | request_id,user_id,tenant_id,query_text,mode | generic denial envelope | decision/audit only | log would-deny + continue | block when deny | R-RPATCH-001/002/007 | SR-RET-001,SR-AUDIT-001 | PP-RET-01,PP-AUDIT-01 | RPT-001,RPT-004,RPT-005 | feature-flag bypass path | medium | planned |
| RPC-002 | subject context extraction | backend/onyx/server/auth and retrieval adapter layers | request principal helpers | Subject identity is derived from auth/session context. | Add required subject extraction contract. | `validate_subject_context` | user_id,roles,groups,authn_state | deny missing subject | audit missing-subject | shadow-deny telemetry | hard deny | R-RPATCH-007/006 | SR-RET-001,SR-ADMIN-001 | PP-RET-01 | RPT-002 | disable hook via rollout flag | medium | planned |
| RPC-003 | tenant context extraction | backend/onyx/server/multitenant + retrieval adapters | tenant resolution helpers | Tenant is currently resolved for retrieval calls. | Add required tenant-bound context check. | `validate_tenant_context` | tenant_id,tenant_scope | deny missing tenant | record only | shadow-deny drift logs | hard deny | R-RPATCH-007/006 | SR-RET-001,SR-VEC-001 | PP-RET-01,PP-VEC-01 | RPT-003 | rollback to monitor-only | medium | planned |
| RPC-004 | retrieval scope resolution | backend/onyx/chat and search orchestration | retrieval plan builder | Scope constructed from query/config. | ACL scope narrowing hook before backend search. | `resolve_allowed_scope` | tenant_id,subject_id,source_filters | generic scoped deny | log delta scope | log dropped scopes | enforce narrowed/deny | R-RPATCH-001/002 | SR-RET-001 | PP-RET-02 | RPT-006,RPT-010 | disable scope narrowing flag | low | planned |
| RPC-005 | candidate source resolution | backend/onyx/connectors/retrieval source selectors | source resolver functions | Sources selected by query constraints and ranking config. | Filter source set by ACL decision. | `filter_allowed_sources` | source_id,tenant_id,subject_perms | hide source identifiers | report dropped source count | emit would-drop list | remove unauthorized sources | R-RPATCH-001/002 | SR-RET-001 | PP-RET-02 | RPT-010,RPT-012 | revert source filter hook | low | planned |
| RPC-006 | vector namespace check | backend/onyx/document_index / vespa query adapters | vector query builder | Namespace constraints may come from caller/config. | Assert namespace belongs to resolved tenant scope. | `check_namespace_access` | tenant_id,namespace | deny with safe reason | record mismatch | shadow-deny mismatch | block query | R-RPATCH-001/006 | SR-VEC-001,SR-RET-001 | PP-VEC-01 | RPT-008 | feature flag off | medium | planned |
| RPC-007 | vector metadata check | backend/onyx/document_index metadata filter stage | metadata filter assembly | Metadata filters currently reflect retrieval options. | Append/validate ACL metadata predicates. | `check_vector_metadata_acl` | acl_tags,doc_owner,tenant_id | generic deny | audit only | log would-deny hits | exclude mismatched candidates | R-RPATCH-001/002 | SR-VEC-001 | PP-VEC-02 | RPT-009 | remove acl predicate injection | medium | planned |
| RPC-008 | document ACL check | backend/onyx/retrieval post-vector candidate gate | doc candidate filter | Candidate docs pass to rerank/context. | Evaluate doc-level ACL before downstream stages. | `authorize_document` | doc_id,tenant_id,subject_id,acl_version | no doc leakage | count denied docs | mark shadow-denied docs | remove/deny | R-RPATCH-001/008 | SR-RET-001 | PP-RET-02 | RPT-006,RPT-011 | fallback to pre-hook behavior | medium | planned |
| RPC-009 | chunk ACL check | backend/onyx/retrieval chunk expansion stage | chunk collector | Chunks from docs prepared for rerank/context. | Chunk-level ACL gate post expansion. | `authorize_chunk` | chunk_id,doc_id,tenant_id,subject_id | no chunk identifiers leaked | log denied chunk count | log would-deny chunks | exclude unauthorized chunks | R-RPATCH-001/008 | SR-RET-001,SR-CACHE-001 | PP-RET-02,PP-CACHE-01 | RPT-007,RPT-013 | disable chunk gate flag | medium | planned |
| RPC-010 | hybrid search filtering | backend/onyx/search hybrid fusion pipeline | lexical+vector merge stage | Hybrid merge currently rank-orders raw candidates. | Filter unauthorized before/after fusion. | `filter_hybrid_candidates` | candidate_ids,acl_decisions | sanitized denial | report filtered totals | report shadow filtered | enforce filtered output | R-RPATCH-001/002 | SR-RET-001,SR-VEC-001 | PP-RET-02,PP-VEC-02 | RPT-010 | bypass hybrid acl filter flag | low | planned |
| RPC-011 | rerank candidate filtering | backend/onyx/chat/reranking pipeline | rerank input builder | Reranker can receive all upstream candidates. | Enforce ACL-filtered rerank input/output. | `filter_rerank_candidates` | candidate_ids,acl_map | no denied candidate echo | telemetry only | shadow-deny reintro detection | block reintroduced unauthorized | R-RPATCH-001/004 | SR-RET-001 | PP-RET-02 | RPT-011 | rollback rerank guard | medium | planned |
| RPC-012 | citation filtering | backend/onyx/chat/citations | citation builder | Citations formed from selected context. | Remove unauthorized references pre-response. | `filter_citations_acl` | citation_doc_id,citation_chunk_id | generic source-hidden response | record suppressed citations | shadow suppress counts | enforce removal | R-RPATCH-002 | SR-RET-001,SR-PROMPT-001 | PP-RET-02,PP-PROMPT-02 | RPT-012 | disable citation filter | medium | planned |
| RPC-013 | context chunk authorization | backend/onyx/chat/context assembly | context pack builder | Context may include all selected chunks. | ACL filter before packing model context. | `filter_context_chunks_acl` | chunk_ids,subject_id,tenant_id | deny without disclosure | monitor dropped chunks | shadow-deny dropped chunks | enforce exclusion | R-RPATCH-002 | SR-RET-001,SR-PROMPT-001 | PP-RET-02,PP-PROMPT-01 | RPT-013 | revert context gate | medium | planned |
| RPC-014 | prompt context authorization | backend/onyx/chat/prompt construction | prompt context renderer | Prompt sees assembled context as-is. | Final ACL assertion before prompt render. | `authorize_prompt_context` | prompt_chunks,acl_labels | no denied text leakage | prompt decision log | shadow-deny markers | block/render sanitized | R-RPATCH-002 | SR-PROMPT-001,SR-RET-001 | PP-PROMPT-01/02 | RPT-014,RPT-019 | disable prompt assertion | low | planned |
| RPC-015 | cache read authorization | backend/onyx/cache retrieval response cache | cache get path | Cache may return prior retrieval artifacts. | ACL validate cached payload before return. | `authorize_cache_read` | cache_key,tenant_id,subject_id,acl_version | cache miss-style safe deny | monitor cache bypass risk | shadow would-deny cache reads | deny/evict unauthorized cache | R-RPATCH-008/006 | SR-CACHE-001,SR-RET-001 | PP-CACHE-01,PP-RET-02 | RPT-015 | disable ACL cache check | medium | planned |
| RPC-016 | audit event write | backend/onyx/security/audit emission callsites | audit helpers | Retrieval decisions may not be fully audited. | Mandatory audit on decision path. | `write_retrieval_audit_event` | decision_id,mode,result,reason | redact sensitive fields | emit decision events | emit deny drift events | required audit on allow/deny | R-RPATCH-003 | SR-AUDIT-001,SR-EVIDENCE-001 | PP-AUDIT-01 | RPT-016 | fallback to existing audit format | high | planned |
| RPC-017 | finding/metric emission | backend/onyx/security telemetry/finding paths | finding+metric emitters | Retrieval security deviations may be under-reported. | Emit findings/metrics for deny/drift/misconfig. | `record_retrieval_finding` + `emit_retrieval_metric` | requirement_id,risk_id,mode,decision | no sensitive content | metrics only | shadow drift finding | enforce deny finding/metric | R-RPATCH-004/005/006 | SR-EVIDENCE-001,SR-AUDIT-001 | PP-EVIDENCE-01,PP-AUDIT-02 | RPT-017,RPT-018 | disable new signals via flag | high | planned |

## rollout plans
### monitor-only rollout plan
Enable decision hooks in observe mode; never block. Require complete audit + metric output and drift baselines.

### shadow-deny rollout plan
Compute deny decisions and record would-block outcomes while continuing responses. Compare shadow-deny and monitor-only deltas.

### enforce-mode rollout plan
Progressively enable blocking by tenant/cohort once shadow-deny drift and false-positive thresholds are approved.

## fail-closed rollout expectations
Missing required subject/tenant/context in enforce mode blocks retrieval safely and emits audit/finding/metric evidence.

## safe-denial rollout expectations
Denial responses remain generic and do not disclose denied doc/source/chunk identifiers.

## backwards compatibility expectations
Monitor-only and shadow-deny modes preserve user-visible retrieval behavior; enforce mode only changes unauthorized access outcomes.

## feature flag/config expectations
Separate flags for: hook activation, mode selection, per-stage enforcement, audit strictness, and rollback fallback.

## test strategy
Use `docs/security/retrieval_path_patching_test_plan.md` for planned test IDs, mappings, expected evidence, and rollback verification.

## evidence requirements
Store prerequisite checks, inventory, candidate map, test summary, traceability summary, and remote limitation notes under `docs/security/evidence/retrieval_path_patching_design/`.

## rollback expectations
Rollback path requires per-stage feature-flag disablement, enforce→shadow→monitor rollback order, and validation that baseline behavior is restored.

## known limitations
- Candidate file/function mappings are best-effort and require implementation-time verification.
- No runtime patching or enforcement is included in this step.
- Remote/main sync validation may remain blocked by environment constraints.
