# Vector DB Security Design (Step 19A)

## Purpose
Define planned security controls for vector write/read/delete/update flows without changing live runtime behavior.

## Scope
Design-only coverage for namespace isolation, metadata integrity, authorization checkpoints, auditing, findings, metrics, and denial semantics for vector operations.

## Status
planned/design

## Owner
AI Trust & Security Readiness Engineer

## Non-Claim Statement
This document does **not** claim live enforcement is active. No runtime vector DB behavior is changed in Step 19A.

## Relationships
- **Secure ingestion:** provides upstream provenance, ACL, and content markers consumed by planned vector metadata checks.
- **Retrieval ACL:** provides authorization context and policy expectations for vector query filtering.
- **Retrieval monitor-only hook:** informs monitor-first rollout strategy and evidence-first gating.
- **Retrieval security tests:** informs negative-test structure and planned monitor-only validation patterns.

## Vector DB Threat Model
- Cross-tenant namespace leakage.
- Metadata tampering/bypass on write or query.
- Missing ACL snapshot/provenance at vector-write time.
- Stale/deleted vectors returned to callers.
- Prompt-injection or poisoned content embedded without marker propagation.
- Cache-mediated ACL bypass.

## Trust Boundaries
1. Ingestion/trust boundary (connector + parser output).
2. Indexing boundary (embedding + vector write).
3. Retrieval boundary (query + candidate evaluation).
4. Cache boundary (candidate reuse and invalidation).
5. Audit/evidence boundary (security telemetry sinks).

## Boundary and Namespace Models
- **Vector index boundary model:** vector index treated as untrusted persistence requiring metadata-backed policy checks.
- **Tenant namespace model:** every vector operation scoped to tenant namespace key.
- **Workspace namespace model:** workspace-partitioned sub-namespace under tenant.
- **Document namespace model:** document/chunk lineage required for all writes/reads/deletes.

## Metadata Models
- **Chunk metadata model:** chunk-safe identifiers + flags (stale/deleted/injection/poison).
- **Embedding metadata model:** model id, created timestamp, schema version, run id.

## Authorization Models
- **Vector write authorization model:** require tenant/subject, resolved namespace, ACL snapshot, provenance.
- **Vector read authorization model:** require tenant/subject + namespace + metadata consistency + ACL filter compatibility.
- **Vector delete authorization model:** require tenant/subject + namespace ownership + document lineage.
- **Vector update/re-embedding authorization model:** same as write, plus preserve ACL/provenance continuity.

## Validation and Filter Models
- **Vector metadata validation model:** schema-bound required fields, type checks, forbidden sensitive payloads.
- **Vector namespace validation model:** resolved namespace must match request tenant/workspace/document context.
- **Vector search filter model:** tenant/workspace/document and ACL snapshot constraints in search filter composition.

## Data Lifecycle Handling
- stale vector handling: stale marker checked and filtered/flagged per mode.
- deleted document vector handling: deleted marker checked and filtered/flagged per mode.
- duplicate vector handling: deterministic tie-break + duplicate finding/metric.
- poisoned vector/document handling: poisoning flag required for unsafe content and escalated finding path.
- prompt-injection marker propagation: prompt_injection_flag propagated from ingestion through vector metadata.
- ACL snapshot propagation into vector metadata: snapshot id/version/timestamps required.
- provenance propagation into vector metadata: provenance_id and ingestion_run_id required.
- connector permission drift handling: compare ACL snapshot freshness to query-time context; emit findings when stale.

## Vector Cache Interaction Model
Cache lookups are policy-aware and must not bypass namespace/ACL checks; cached candidates undergo metadata checks before use.

## Audit Events
Planned events include write requested/validated/committed, query requested/validated, candidate anomalies, denial-safe events, and finding records.

## Findings
Planned findings for cross-tenant candidates, stale/deleted candidates, missing ACL/provenance, metadata mismatch, poisoning/prompt-injection markers.

## Metrics
Planned metrics include stage pass/fail counts, denial categories, stale/deleted candidate rates, duplicate rates, and metadata validation failure rates.

## Safe Denial Behavior
Denials return generic non-secret-safe responses without exposing tenant/workspace/document/chunk/source identifiers.

## Monitor-only / Shadow-deny / Enforce-mode Plan
- monitor-only: first implementation target, no blocking.
- shadow-deny: planned future, remains blocked in current program state.
- enforce-mode: planned future, remains no-go in current program state.

## Test Strategy
See `docs/security/vector_db_security_test_plan.md` for planned negative/consistency/telemetry tests.

## Evidence Requirements
Stage inventory, metadata contract summary, test-plan summary, traceability summary, prerequisite verification, and remote sync limitation record (if present).

## Known Limitations
Design-only. No live vector write/read/delete/update enforcement wired in Step 19A.

## Vector DB Security Stages (Planned)

### Stage: vector_write_requested
- stage ID: VEC-STAGE-001
- purpose: register intent to write vector.
- mapped risks: R-VEC-001, R-VEC-003
- mapped requirements: SR-VEC-001
- mapped patch points: PP-VEC-01
- required context fields: request_id, tenant_id, subject_id, document_id, chunk_id
- planned policy check: context presence + operation type allowlist
- safe denial category: DENY_MISSING_CONTEXT
- audit event: vector_write_requested
- finding condition: missing tenant/subject
- metric: vec_write_requested_total
- planned tests: VEC-TST-001, VEC-TST-002
- implementation status: planned

### Stage: vector_write_context_validated
- stage ID: VEC-STAGE-002
- purpose: validate tenant/subject/document/chunk context consistency.
- mapped risks: R-VEC-001, R-VEC-002
- mapped requirements: SR-VEC-001
- mapped patch points: PP-VEC-01
- required context fields: tenant_id, subject_id, workspace_id, document_id, chunk_id
- planned policy check: required-field + tenant-subject binding
- safe denial category: DENY_CONTEXT_INVALID
- audit event: vector_write_context_validated
- finding condition: context mismatch
- metric: vec_write_context_validation_failures_total
- planned tests: VEC-TST-003
- implementation status: planned

### Stage: vector_namespace_resolved
- stage ID: VEC-STAGE-003
- purpose: resolve canonical vector namespace.
- mapped risks: R-VEC-001
- mapped requirements: SR-VEC-001
- mapped patch points: PP-VEC-01
- required context fields: tenant_id, workspace_id, index_name
- planned policy check: deterministic namespace resolution from safe ids
- safe denial category: DENY_NAMESPACE_UNRESOLVED
- audit event: vector_namespace_resolved
- finding condition: namespace resolution failure
- metric: vec_namespace_resolution_failures_total
- planned tests: VEC-TST-003
- implementation status: planned

### Stage: vector_namespace_authorized
- stage ID: VEC-STAGE-004
- purpose: authorize operation on resolved namespace.
- mapped risks: R-VEC-001, R-VEC-002
- mapped requirements: SR-VEC-001
- mapped patch points: PP-VEC-01, PP-VEC-02
- required context fields: subject_id, tenant_id, workspace_id, namespace
- planned policy check: tenant/workspace namespace ownership check
- safe denial category: DENY_NAMESPACE_UNAUTHORIZED
- audit event: vector_namespace_authorized
- finding condition: cross-tenant namespace attempt
- metric: vec_namespace_unauthorized_total
- planned tests: VEC-TST-003
- implementation status: planned

### Stage: vector_metadata_validated
- stage ID: VEC-STAGE-005
- purpose: validate vector metadata contract compliance.
- mapped risks: R-VEC-002, R-VEC-010
- mapped requirements: SR-VEC-001
- mapped patch points: PP-VEC-01
- required context fields: metadata_schema_version plus all required metadata fields
- planned policy check: type/required/forbidden-content validation
- safe denial category: DENY_METADATA_INVALID
- audit event: vector_metadata_validated
- finding condition: missing or invalid metadata
- metric: vec_metadata_validation_failures_total
- planned tests: VEC-TST-007
- implementation status: planned

### Stage: vector_acl_snapshot_attached
- stage ID: VEC-STAGE-006
- purpose: ensure ACL snapshot exists and is fresh.
- mapped risks: R-VEC-003
- mapped requirements: SR-VEC-001, SR-RET-001
- mapped patch points: PP-VEC-01, PP-RET-02
- required context fields: acl_snapshot_id, acl_snapshot_version, acl_snapshot_expires_at
- planned policy check: snapshot required and not stale at write time
- safe denial category: DENY_ACL_SNAPSHOT_MISSING_OR_STALE
- audit event: vector_acl_snapshot_attached
- finding condition: missing/stale ACL snapshot
- metric: vec_acl_snapshot_failures_total
- planned tests: VEC-TST-004, VEC-TST-005
- implementation status: planned

### Stage: vector_provenance_attached
- stage ID: VEC-STAGE-007
- purpose: ensure provenance metadata propagation.
- mapped risks: R-VEC-005
- mapped requirements: SR-ING-001, SR-VEC-001
- mapped patch points: PP-ING-02, PP-VEC-01
- required context fields: provenance_id, ingestion_run_id, source_type
- planned policy check: provenance presence + type validity
- safe denial category: DENY_PROVENANCE_MISSING
- audit event: vector_provenance_attached
- finding condition: provenance missing
- metric: vec_provenance_missing_total
- planned tests: VEC-TST-006
- implementation status: planned

### Stage: vector_embedding_metadata_attached
- stage ID: VEC-STAGE-008
- purpose: attach embedding model metadata and safety markers.
- mapped risks: R-VEC-006, R-VEC-007, R-VEC-009
- mapped requirements: SR-VEC-001
- mapped patch points: PP-VEC-01
- required context fields: embedding_model_id, embedding_created_at, prompt_injection_flag, poisoning_flag
- planned policy check: required embedding metadata + marker propagation
- safe denial category: DENY_EMBEDDING_METADATA_INVALID
- audit event: vector_embedding_metadata_attached
- finding condition: missing model metadata or marker mismatch
- metric: vec_embedding_metadata_failures_total
- planned tests: VEC-TST-008, VEC-TST-009, VEC-TST-019
- implementation status: planned

### Stage: vector_write_committed
- stage ID: VEC-STAGE-009
- purpose: record successful vector write with final metadata.
- mapped risks: R-VEC-003, R-VEC-005
- mapped requirements: SR-VEC-001
- mapped patch points: PP-VEC-01
- required context fields: vector_id, namespace, metadata_schema_version
- planned policy check: commit only after prior stage success
- safe denial category: DENY_COMMIT_PRECONDITION_FAILED
- audit event: vector_write_committed
- finding condition: commit attempted with missing preconditions
- metric: vec_write_committed_total
- planned tests: VEC-TST-020
- implementation status: planned

### Stage: vector_query_requested
- stage ID: VEC-STAGE-010
- purpose: register query intent for vector retrieval.
- mapped risks: R-VEC-001, R-VEC-008
- mapped requirements: SR-VEC-001, SR-RET-001
- mapped patch points: PP-VEC-02, PP-RET-01
- required context fields: request_id, tenant_id, subject_id, workspace_id
- planned policy check: presence and operation allowlist
- safe denial category: DENY_MISSING_CONTEXT
- audit event: vector_query_requested
- finding condition: missing tenant/subject
- metric: vec_query_requested_total
- planned tests: VEC-TST-010, VEC-TST-011
- implementation status: planned

### Stage: vector_query_context_validated
- stage ID: VEC-STAGE-011
- purpose: validate query context binding.
- mapped risks: R-VEC-001, R-VEC-002
- mapped requirements: SR-VEC-001, SR-RET-001
- mapped patch points: PP-VEC-02, PP-RET-01
- required context fields: tenant_id, subject_id, acl_context_version
- planned policy check: tenant/subject/query binding and ACL context existence
- safe denial category: DENY_CONTEXT_INVALID
- audit event: vector_query_context_validated
- finding condition: ACL context missing/mismatch
- metric: vec_query_context_validation_failures_total
- planned tests: VEC-TST-012, VEC-TST-013
- implementation status: planned

### Stage: vector_search_filter_built
- stage ID: VEC-STAGE-012
- purpose: build immutable namespace+metadata search filters.
- mapped risks: R-VEC-001, R-VEC-008
- mapped requirements: SR-VEC-001, SR-RET-001
- mapped patch points: PP-VEC-02, PP-RET-02
- required context fields: tenant/workspace namespace fields, acl snapshot selectors
- planned policy check: required filter clauses present and non-overridable
- safe denial category: DENY_FILTER_BUILD_FAILED
- audit event: vector_search_filter_built
- finding condition: mandatory clause absent
- metric: vec_filter_build_failures_total
- planned tests: VEC-TST-012, VEC-TST-017
- implementation status: planned

### Stage: vector_candidates_returned
- stage ID: VEC-STAGE-013
- purpose: handle raw vector candidates before trust.
- mapped risks: R-VEC-001, R-VEC-004
- mapped requirements: SR-VEC-001
- mapped patch points: PP-VEC-02
- required context fields: candidate_ids, candidate_metadata
- planned policy check: all candidates contain minimum metadata
- safe denial category: DENY_CANDIDATE_SET_INVALID
- audit event: vector_candidates_returned
- finding condition: candidate missing metadata
- metric: vec_candidates_missing_metadata_total
- planned tests: VEC-TST-013
- implementation status: planned

### Stage: vector_candidate_metadata_checked
- stage ID: VEC-STAGE-014
- purpose: evaluate candidate metadata for tenant/ACL/lineage consistency.
- mapped risks: R-VEC-001, R-VEC-002, R-VEC-010
- mapped requirements: SR-VEC-001, SR-RET-001
- mapped patch points: PP-VEC-02, PP-RET-02
- required context fields: candidate tenant/workspace/doc/chunk safe ids + ACL snapshot fields
- planned policy check: strict equality checks for namespace/metadata ownership
- safe denial category: DENY_CANDIDATE_METADATA_MISMATCH
- audit event: vector_candidate_metadata_checked
- finding condition: cross-tenant or metadata mismatch candidate
- metric: vec_candidate_metadata_mismatch_total
- planned tests: VEC-TST-014
- implementation status: planned

### Stage: vector_deleted_or_stale_filtered
- stage ID: VEC-STAGE-015
- purpose: identify stale/deleted candidates and safe-handle per mode.
- mapped risks: R-VEC-004
- mapped requirements: SR-VEC-001, SR-RET-001
- mapped patch points: PP-VEC-02, PP-RET-02
- required context fields: document_deleted, document_stale
- planned policy check: stale/deleted markers evaluated for each candidate
- safe denial category: DENY_STALE_OR_DELETED_CANDIDATE
- audit event: vector_deleted_or_stale_filtered
- finding condition: stale/deleted candidate returned
- metric: vec_stale_or_deleted_candidates_total
- planned tests: VEC-TST-015, VEC-TST-016
- implementation status: planned

### Stage: vector_cache_checked
- stage ID: VEC-STAGE-016
- purpose: ensure cache hit cannot bypass ACL/metadata checks.
- mapped risks: R-VEC-008
- mapped requirements: SR-CACHE-001, SR-VEC-001
- mapped patch points: PP-CACHE-01, PP-VEC-02
- required context fields: cache_key_dims, acl_snapshot_version, tenant_id
- planned policy check: cache keys include ACL dimensions and post-hit metadata validation still runs
- safe denial category: DENY_CACHE_POLICY_MISMATCH
- audit event: vector_cache_checked
- finding condition: cache key missing ACL dimension or bypass detected
- metric: vec_cache_acl_bypass_attempt_total
- planned tests: VEC-TST-017
- implementation status: planned

### Stage: vector_audit_written
- stage ID: VEC-STAGE-017
- purpose: persist structured security audit record.
- mapped risks: R-VEC-010
- mapped requirements: SR-AUDIT-001, SR-VEC-001
- mapped patch points: PP-AUDIT-01, PP-VEC-02
- required context fields: request_id, actor_safe_id, action, stage_outcome
- planned policy check: required audit schema fields present
- safe denial category: DENY_AUDIT_SCHEMA_INVALID
- audit event: vector_audit_written
- finding condition: missing required audit fields
- metric: vec_audit_write_failures_total
- planned tests: VEC-TST-023
- implementation status: planned

### Stage: vector_finding_recorded_if_needed
- stage ID: VEC-STAGE-018
- purpose: record finding and metric when anomaly/violation observed.
- mapped risks: R-VEC-001, R-VEC-004, R-VEC-006, R-VEC-007, R-VEC-008, R-VEC-010
- mapped requirements: SR-VEC-001, SR-AUDIT-001, SR-EVIDENCE-001
- mapped patch points: PP-VEC-02, PP-AUDIT-02, PP-EVIDENCE-01
- required context fields: finding_type, severity, request_id, safe identifiers
- planned policy check: finding criteria thresholds and dedupe rules
- safe denial category: DENY_FINDING_PIPELINE_UNAVAILABLE
- audit event: vector_finding_recorded
- finding condition: any mapped violation condition true
- metric: vec_findings_total
- planned tests: VEC-TST-024, VEC-TST-025, VEC-TST-026
- implementation status: planned

## Step 19B Update (2026-05-27)
- Implemented isolated vector DB security helper controls under `backend/security_layer/vector/`.
- Added isolated stages, metadata contract validation, validators, and control helpers.
- No live vector DB/search/index/cache integration or enforcement was enabled.

## Step 19C Validation Cleanup (2026-05-27)
- Isolated vector security controls validated with expanded stage-level tests.
- Metadata contract validation strengthened for all required fields, forbidden keys, and forbidden content patterns.
- Namespace/ACL/provenance behavior validated with deny/filter-safe cases.
- No live vector DB integration added.
- Production enforcement remains inactive (no enforce mode; no shadow-deny).
