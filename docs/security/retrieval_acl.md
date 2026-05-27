# Retrieval ACL Design (Step 16A)

## Purpose
Define the planned retrieval access-control model for query-to-context assembly security gating, without changing runtime behavior.

## Scope
Design, traceability, and test-planning artifacts for retrieval ACL controls across query auth, document/chunk filtering, vector metadata constraints, rerank filtering, citation filtering, context assembly boundaries, prompt context boundaries, and ACL-aware cache behavior.

## Status
planned/design

## Owner
AI Trust & Security Readiness Engineer

## Non-Claim Statement
This document is design-only. It does **not** claim live enforcement, production integration, control effectiveness, or production readiness.

## Relationship to Existing Step Artifacts
- **Policy engine:** Planned checks consume policy decisions from `backend/security_layer/policies` via future integration.
- **Runtime wrappers:** Planned stage orchestration maps to future wrappers under `backend/security_layer/runtime`.
- **Safe denial behavior:** All deny branches map to safe-denial taxonomy and no-leak response standards.
- **Secure ingestion:** Retrieval ACL relies on trusted ingestion metadata/ACL snapshots from secure-ingestion controls.

## Retrieval Threat Model
Primary threats: cross-tenant leakage, ACL bypass at doc/chunk/vector/rerank/citation layers, stale permission artifacts, deleted-document resurfacing, and cache-based authorization bypass.

## Retrieval Trust Boundaries
1. Caller/session boundary.
2. Tenant/workspace boundary.
3. Query orchestration boundary.
4. Vector search backend boundary.
5. Reranker boundary.
6. Citation/context/prompt assembly boundary.
7. Cache boundary.
8. Audit/metrics/findings boundary.

## Retrieval Entrypoints
Planned coverage for backend retrieval entrypoints that process user query requests and produce candidate/context/citation outputs (without modifying live handlers in this step).

## Authorization Models
- **Query authorization model:** Query must carry valid subject + tenant context before retrieval scope resolution.
- **Document-level ACL model:** Candidate documents require allow decision against tenant/workspace + subject principal set.
- **Chunk-level ACL model:** Chunks must inherit and satisfy effective ACL, not only parent-doc allow.
- **Tenant/workspace boundary model:** Hard deny on boundary mismatch.
- **User/group/role permission model:** Effective principal set includes user ID, resolved groups, and roles.
- **Connector permission propagation model:** Connector entitlement snapshots propagate into doc/chunk ACL evidence.
- **ACL snapshot model:** Retrieval checks use versioned snapshot metadata.
- **Stale ACL handling:** Stale/unknown snapshot state yields deny + finding.
- **Deleted document handling:** Deleted/tombstoned content always filtered/denied.
- **Vector metadata authorization model:** Metadata filters must match tenant/workspace/principal constraints.
- **Namespace isolation model:** Vector namespace mismatch is denied.
- **Hybrid search authorization model:** Keyword/vector merged candidates re-filtered by ACL before scoring.
- **Reranking authorization model:** Reranker input set is ACL-pruned; output cannot reintroduce unauthorized items.
- **Citation/source attribution authorization model:** Unauthorized source references are removed.
- **Context assembly authorization model:** Unauthorized chunks excluded from final context window.
- **Prompt context boundary model:** Prompt-eligible context is constrained to authorized chunks only.
- **Cache interaction model:** Cache read allowed only when ACL-context fingerprint matches request context.

## Audit Events
Planned structured events for stage decisions: allow/deny reason category, tenant ID, subject hash, stage ID, policy version, snapshot version, mode (monitor/shadow/enforce).

## Findings
Findings planned for repeated denies, stale snapshots, permission drift signals, metadata mismatch, and namespace mismatch.

## Metrics
Per-stage allow/deny counters, stale-snapshot rate, unauthorized candidate drop counts, citation suppression count, cache ACL mismatch count.

## Safe Denial Behavior for Retrieval
All deny responses must avoid revealing denied document IDs, chunk IDs, connector identities, source titles, or namespace details beyond safe category labels.

## Monitor-only / Shadow-deny / Enforce-mode Plan
1. **Monitor-only:** Record decisions, no request blocking.
2. **Shadow-deny:** Compute deny outcomes and record deltas vs live behavior, still no live block.
3. **Enforce-mode (future):** Block unsafe paths only after evidence gate approval.

## Test Strategy
See `docs/security/retrieval_acl_test_plan.md` for stage-mapped planned coverage.

## Evidence Requirements
- Stage inventory and traceability summary.
- Test plan + test evidence templates.
- Audit sample schemas and metric catalog.
- Remote-sync limitation note when applicable.

## Known Limitations
- Design-only; no production path wiring.
- No runtime enforcement activation.
- No retrieval/search/vector/rerank/context/prompt/cache integration in this step.

## Retrieval ACL Stages (Planned)

### RACL-01 — query_received
- **Stage ID:** RACL-01
- **Purpose:** Register retrieval request + initialize decision context.
- **Mapped risks:** R-RET-001, R-RET-008
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-01
- **Required context fields:** request_id, query_id, tenant_id(optional), subject_id(optional), mode
- **Planned policy check:** request metadata completeness precheck
- **Safe denial category:** DENY_MISSING_CONTEXT
- **Audit event:** retrieval.query_received
- **Finding condition:** malformed request context observed
- **Metric:** retrieval_query_received_total
- **Planned tests:** RET-ACL-T001, RET-ACL-T002
- **Implementation status:** planned

### RACL-02 — subject_context_validated
- **Stage ID:** RACL-02
- **Purpose:** Ensure subject identity/principals are present.
- **Mapped risks:** R-RET-001
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-01
- **Required context fields:** subject_id, subject_groups, subject_roles
- **Planned policy check:** subject identity validation
- **Safe denial category:** DENY_SUBJECT_MISSING
- **Audit event:** retrieval.subject_context_validated
- **Finding condition:** missing/invalid subject context
- **Metric:** retrieval_subject_context_deny_total
- **Planned tests:** RET-ACL-T002, RET-ACL-T005, RET-ACL-T006
- **Implementation status:** planned

### RACL-03 — tenant_context_validated
- **Stage ID:** RACL-03
- **Purpose:** Enforce tenant/workspace presence and validity.
- **Mapped risks:** R-RET-001
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-01
- **Required context fields:** tenant_id, workspace_id
- **Planned policy check:** tenant/workspace boundary validation
- **Safe denial category:** DENY_TENANT_MISSING_OR_INVALID
- **Audit event:** retrieval.tenant_context_validated
- **Finding condition:** tenant missing or malformed
- **Metric:** retrieval_tenant_context_deny_total
- **Planned tests:** RET-ACL-T001, RET-ACL-T003
- **Implementation status:** planned

### RACL-04 — retrieval_scope_resolved
- **Stage ID:** RACL-04
- **Purpose:** Determine authorized retrieval scope constraints.
- **Mapped risks:** R-RET-001, R-RET-010
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-01
- **Required context fields:** tenant_id, workspace_id, principal_set
- **Planned policy check:** scope derivation policy
- **Safe denial category:** DENY_SCOPE_RESOLUTION
- **Audit event:** retrieval.scope_resolved
- **Finding condition:** scope inconsistent with context
- **Metric:** retrieval_scope_resolution_fail_total
- **Planned tests:** RET-ACL-T003, RET-ACL-T004
- **Implementation status:** planned

### RACL-05 — candidate_sources_resolved
- **Stage ID:** RACL-05
- **Purpose:** Resolve candidate sources/connectors with ACL metadata.
- **Mapped risks:** R-RET-009
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-02
- **Required context fields:** connector_ids, acl_snapshot_version
- **Planned policy check:** connector entitlement consistency
- **Safe denial category:** DENY_CONNECTOR_PERMISSION_DRIFT
- **Audit event:** retrieval.candidate_sources_resolved
- **Finding condition:** connector permission drift detected
- **Metric:** retrieval_connector_drift_total
- **Planned tests:** RET-ACL-T018
- **Implementation status:** planned

### RACL-06 — document_acl_checked
- **Stage ID:** RACL-06
- **Purpose:** Filter unauthorized documents.
- **Mapped risks:** R-RET-001, R-RET-005
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-02
- **Required context fields:** document_id, document_acl, deleted_flag
- **Planned policy check:** doc ACL + deleted-state check
- **Safe denial category:** DENY_DOCUMENT_UNAUTHORIZED
- **Audit event:** retrieval.document_acl_checked
- **Finding condition:** repeated doc-level denies or deleted-doc candidate
- **Metric:** retrieval_document_acl_denied_total
- **Planned tests:** RET-ACL-T003, RET-ACL-T007, RET-ACL-T008
- **Implementation status:** planned

### RACL-07 — chunk_acl_checked
- **Stage ID:** RACL-07
- **Purpose:** Enforce chunk-level ACL.
- **Mapped risks:** R-RET-002, R-RET-010
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-02
- **Required context fields:** chunk_id, chunk_acl, parent_doc_id
- **Planned policy check:** effective chunk ACL decision
- **Safe denial category:** DENY_CHUNK_UNAUTHORIZED
- **Audit event:** retrieval.chunk_acl_checked
- **Finding condition:** chunk allowed while doc denied (consistency issue)
- **Metric:** retrieval_chunk_acl_denied_total
- **Planned tests:** RET-ACL-T004, RET-ACL-T014
- **Implementation status:** planned

### RACL-08 — vector_namespace_checked
- **Stage ID:** RACL-08
- **Purpose:** Validate vector namespace isolation.
- **Mapped risks:** R-RET-003
- **Mapped requirements:** SR-VEC-001, SR-RET-001
- **Mapped patch points:** PP-VEC-01
- **Required context fields:** vector_namespace, tenant_id
- **Planned policy check:** namespace equals authorized tenant/workspace namespace
- **Safe denial category:** DENY_NAMESPACE_MISMATCH
- **Audit event:** retrieval.vector_namespace_checked
- **Finding condition:** namespace mismatch observed
- **Metric:** retrieval_namespace_mismatch_total
- **Planned tests:** RET-ACL-T009
- **Implementation status:** planned

### RACL-09 — vector_metadata_checked
- **Stage ID:** RACL-09
- **Purpose:** Validate immutable vector metadata filters.
- **Mapped risks:** R-RET-003
- **Mapped requirements:** SR-VEC-001, SR-RET-001
- **Mapped patch points:** PP-VEC-02
- **Required context fields:** vector_metadata_filter, tenant_id, workspace_id, acl_snapshot_version
- **Planned policy check:** required metadata predicates present and matching
- **Safe denial category:** DENY_VECTOR_METADATA_MISMATCH
- **Audit event:** retrieval.vector_metadata_checked
- **Finding condition:** missing/mismatched filter predicate
- **Metric:** retrieval_vector_metadata_mismatch_total
- **Planned tests:** RET-ACL-T010
- **Implementation status:** planned

### RACL-10 — hybrid_search_filtered
- **Stage ID:** RACL-10
- **Purpose:** ACL-filter merged hybrid candidates.
- **Mapped risks:** R-RET-001, R-RET-002
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-02
- **Required context fields:** hybrid_candidates, acl_decisions
- **Planned policy check:** post-merge ACL filter check
- **Safe denial category:** DENY_HYBRID_CANDIDATE
- **Audit event:** retrieval.hybrid_search_filtered
- **Finding condition:** unauthorized candidate appears post-filter
- **Metric:** retrieval_hybrid_candidates_filtered_total
- **Planned tests:** RET-ACL-T011
- **Implementation status:** planned

### RACL-11 — rerank_candidates_filtered
- **Stage ID:** RACL-11
- **Purpose:** Ensure reranker cannot reintroduce denied candidates.
- **Mapped risks:** R-RET-006
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-02
- **Required context fields:** rerank_input_ids, rerank_output_ids, denied_ids
- **Planned policy check:** rerank output subset of authorized input
- **Safe denial category:** DENY_RERANK_REINTRODUCTION
- **Audit event:** retrieval.rerank_candidates_filtered
- **Finding condition:** rerank output contains denied ID
- **Metric:** retrieval_rerank_reintroduction_total
- **Planned tests:** RET-ACL-T012
- **Implementation status:** planned

### RACL-12 — citation_sources_filtered
- **Stage ID:** RACL-12
- **Purpose:** Remove unauthorized citation/source references.
- **Mapped risks:** R-RET-007
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-02
- **Required context fields:** citation_source_ids, authorized_source_ids
- **Planned policy check:** citation sources subset authorization check
- **Safe denial category:** DENY_CITATION_SOURCE
- **Audit event:** retrieval.citation_sources_filtered
- **Finding condition:** unauthorized source present in citation set
- **Metric:** retrieval_citation_sources_filtered_total
- **Planned tests:** RET-ACL-T013
- **Implementation status:** planned

### RACL-13 — context_chunks_authorized
- **Stage ID:** RACL-13
- **Purpose:** Ensure final context chunk list is authorized.
- **Mapped risks:** R-RET-002, R-RET-010
- **Mapped requirements:** SR-RET-001
- **Mapped patch points:** PP-RET-02
- **Required context fields:** context_chunk_ids, authorized_chunk_ids
- **Planned policy check:** context chunks subset authorization check
- **Safe denial category:** DENY_CONTEXT_CHUNK
- **Audit event:** retrieval.context_chunks_authorized
- **Finding condition:** unauthorized chunk in assembled context
- **Metric:** retrieval_context_chunks_filtered_total
- **Planned tests:** RET-ACL-T014
- **Implementation status:** planned

### RACL-14 — prompt_context_authorized
- **Stage ID:** RACL-14
- **Purpose:** Enforce prompt context boundary.
- **Mapped risks:** R-RET-010
- **Mapped requirements:** SR-RET-001, SR-PROMPT-001
- **Mapped patch points:** PP-PROMPT-01, PP-RET-02
- **Required context fields:** prompt_context_chunk_ids, authorized_chunk_ids
- **Planned policy check:** prompt context contains only authorized chunk-derived text
- **Safe denial category:** DENY_PROMPT_CONTEXT
- **Audit event:** retrieval.prompt_context_authorized
- **Finding condition:** unauthorized text lineage in prompt context
- **Metric:** retrieval_prompt_context_filtered_total
- **Planned tests:** RET-ACL-T015
- **Implementation status:** planned

### RACL-15 — cache_read_authorized
- **Stage ID:** RACL-15
- **Purpose:** Prevent cache ACL bypass.
- **Mapped risks:** R-RET-008, R-RET-004
- **Mapped requirements:** SR-CACHE-001, SR-RET-001
- **Mapped patch points:** PP-CACHE-01, PP-RET-02
- **Required context fields:** cache_key, acl_fingerprint, snapshot_version
- **Planned policy check:** cache ACL fingerprint + snapshot version equality
- **Safe denial category:** DENY_CACHE_ACL_MISMATCH
- **Audit event:** retrieval.cache_read_authorized
- **Finding condition:** cache hit with mismatched ACL context
- **Metric:** retrieval_cache_acl_mismatch_total
- **Planned tests:** RET-ACL-T016, RET-ACL-T017
- **Implementation status:** planned

### RACL-16 — retrieval_audit_written
- **Stage ID:** RACL-16
- **Purpose:** Persist retrieval ACL decision audit record.
- **Mapped risks:** R-008
- **Mapped requirements:** SR-AUDIT-001
- **Mapped patch points:** PP-AUDIT-01
- **Required context fields:** request_id, stage_decisions, mode, outcome
- **Planned policy check:** audit payload completeness check
- **Safe denial category:** DENY_AUDIT_WRITE_FAILURE
- **Audit event:** retrieval.audit_written
- **Finding condition:** audit write failure/incomplete record
- **Metric:** retrieval_audit_write_total
- **Planned tests:** RET-ACL-T022
- **Implementation status:** planned

### RACL-17 — retrieval_finding_recorded_if_needed
- **Stage ID:** RACL-17
- **Purpose:** Record findings for suspicious/unsafe retrieval patterns.
- **Mapped risks:** R-RET-004, R-RET-009
- **Mapped requirements:** SR-AUDIT-001, SR-EVIDENCE-001
- **Mapped patch points:** PP-AUDIT-02, PP-EVIDENCE-01
- **Required context fields:** deny_reason_counts, drift_flags, stale_snapshot_flags
- **Planned policy check:** finding-threshold policy check
- **Safe denial category:** DENY_FINDING_PIPELINE_FAILURE
- **Audit event:** retrieval.finding_recorded
- **Finding condition:** stale snapshot, drift, repeated denies, consistency violations
- **Metric:** retrieval_findings_total
- **Planned tests:** RET-ACL-T023, RET-ACL-T024, RET-ACL-T025
- **Implementation status:** planned

## Step 16B Implementation Note (2026-05-27)
- Minimal isolated retrieval ACL controls implemented under `backend/security_layer/retrieval/`.
- No live retrieval integration enabled.
- No search/vector/rerank/cache/context/prompt integration performed.
- No production enforcement activation.

## Step 16C Validation Note (2026-05-27)
- Validation cleanup completed in isolated scope only.
- Stage-level authorizers validated across all 17 retrieval ACL stages.
- No live retrieval/search/vector/rerank/citation/context/prompt/cache/worker/web/deployment wiring was added.
- Runtime production enforcement remains inactive.

## Step 17B Integration-Plan Reference (2026-05-27)
See `docs/security/retrieval_path_integration_plan.md`, `docs/security/retrieval_path_integration_checklist.md`, and `docs/security/retrieval_path_integration_test_plan.md` for planned runtime integration sequencing while keeping production enforcement inactive in this step.
