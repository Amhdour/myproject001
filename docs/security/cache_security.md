# Cache Security Design (Step 20A)

- **Status:** planned/design
- **Owner:** AI Trust & Security Readiness Engineer
- **Purpose:** Define non-runtime cache security controls, telemetry, and validation strategy without changing live behavior.
- **Scope:** Retrieval cache, vector cache, prompt/context cache, answer cache, and tool result cache design only.
- **Non-claim statement:** This document does not claim implementation, activation, or production readiness.

## Relationships
- **Retrieval ACL:** Cache controls inherit tenant/subject/ACL constraints from retrieval ACL design (`docs/security/retrieval_acl.md`).
- **Vector DB security:** Cache controls must preserve vector namespace and metadata isolation (`docs/security/vector_db_security.md`).
- **Monitor-only retrieval hook:** Cache telemetry design follows monitor-only/non-blocking behavior model (`docs/security/retrieval_path_live_patch_go_no_go.md`).
- **Retrieval security tests:** Cache test planning aligns with negative-test structure and evidence conventions (`docs/security/retrieval_security_tests.md`).

## Threat Model and Trust Boundaries
- **Threat model:** cross-tenant reuse, cross-subject reuse, stale ACL snapshots, deleted/stale document reuse, connector permission drift, poisoning markers, prompt-injection marker loss, sensitive metadata leakage.
- **Trust boundaries:** requester identity boundary, tenant/workspace boundary, ACL snapshot boundary, provenance boundary, cache store boundary, telemetry/audit boundary.

## Cache Security Models
- Retrieval cache security model
- Vector cache security model
- Prompt/context cache security model
- Answer cache security model
- Tool result cache security model

Each model is planned to require tenant/subject/ACL/provenance binding plus safe denial and audit/metric emission.

## Key Design Areas
- tenant-aware cache key model
- subject-aware cache key model
- group/role-aware cache key model
- ACL-aware cache key model
- provenance-aware cache key model
- cache read authorization model
- cache write authorization model
- cache invalidation model
- ACL snapshot invalidation model
- deleted/stale document invalidation model
- connector permission drift invalidation model
- cache poisoning handling
- prompt-injection marker propagation
- sensitive-data cache rules
- cache telemetry rules
- audit events
- findings
- metrics
- safe denial behavior
- monitor-only / shadow-deny / enforce-mode plan (monitor-only planning only; shadow-deny/enforce remain blocked)
- test strategy
- evidence requirements
- known limitations

## Stage Inventory (all implementation status: planned)

| Stage ID | Purpose | Mapped Risks | Mapped Requirements | Mapped Patch Points | Required Context Fields | Planned Policy Check | Safe Denial Category | Audit Event | Finding Condition | Metric | Planned Tests | Implementation Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cache_key_build_requested | Start key construction | R-CACHE-001,R-CACHE-002 | SR-CACHE-001 | PP-CACHE-01 | tenant,subject,purpose | request context present | SD-CACHE-CTX | cache_key_build_requested | missing base context | cache.key.build.requested | CACHE-001,CACHE-002 | planned |
| cache_key_context_validated | Validate key context shape | R-CACHE-010 | SR-CACHE-001 | PP-CACHE-01 | tenant,subject,acl,provenance | context schema validation | SD-CACHE-CTX | cache_key_context_validated | forbidden metadata present | cache.key.context.validated | CACHE-003,CACHE-004 | planned |
| cache_key_tenant_bound | Bind tenant dimension | R-CACHE-001 | SR-CACHE-001 | PP-CACHE-01 | tenant_id_hash_or_safe_id | tenant binding required | SD-CACHE-TENANT | cache_key_tenant_bound | missing tenant binding | cache.key.tenant.bound | CACHE-001,CACHE-005 | planned |
| cache_key_subject_bound | Bind subject dimension | R-CACHE-002 | SR-CACHE-001 | PP-CACHE-01 | subject_id_hash_or_safe_id | subject binding required | SD-CACHE-SUBJECT | cache_key_subject_bound | missing subject binding | cache.key.subject.bound | CACHE-002,CACHE-006 | planned |
| cache_key_acl_bound | Bind ACL snapshot | R-CACHE-003 | SR-CACHE-001,SR-RET-001 | PP-CACHE-01,PP-RET-02 | acl_snapshot_id,version,expiry | ACL snapshot required | SD-CACHE-ACL | cache_key_acl_bound | ACL context absent | cache.key.acl.bound | CACHE-003,CACHE-013 | planned |
| cache_key_provenance_bound | Bind provenance | R-CACHE-010 | SR-CACHE-001,SR-ING-001 | PP-CACHE-01,PP-ING-02 | provenance_id,source_type | provenance required | SD-CACHE-PROV | cache_key_provenance_bound | provenance absent | cache.key.provenance.bound | CACHE-004 | planned |
| cache_read_requested | Start read flow | R-CACHE-001,R-CACHE-002 | SR-CACHE-001 | PP-CACHE-01 | request context,key | pre-read auth check | SD-CACHE-READ | cache_read_requested | read w/o full context | cache.read.requested | CACHE-005,CACHE-006 | planned |
| cache_read_authorized | Authorize read | R-CACHE-001,R-CACHE-002 | SR-CACHE-001,SR-RET-001 | PP-CACHE-01,PP-RET-02 | tenant,subject,groups,roles,acl | principal/ACL match | SD-CACHE-AUTHZ | cache_read_authorized | authz mismatch | cache.read.authorized | CACHE-007,CACHE-008 | planned |
| cache_hit_validated | Validate hit metadata | R-CACHE-003,R-CACHE-006 | SR-CACHE-001,SR-VEC-001 | PP-CACHE-01,PP-VEC-01 | acl snapshot,namespace,ttl | hit metadata consistency | SD-CACHE-HIT | cache_hit_validated | stale/mismatched metadata | cache.hit.validated | CACHE-009,CACHE-012,CACHE-013 | planned |
| cache_miss_recorded | Record miss safely | R-CACHE-010 | SR-AUDIT-001 | PP-AUDIT-01 | key fingerprint,purpose | no secret leakage | SD-CACHE-SAFE | cache_miss_recorded | leaked sensitive metadata | cache.miss.recorded | CACHE-025 | planned |
| cache_write_requested | Start write flow | R-CACHE-009 | SR-CACHE-001 | PP-CACHE-01 | request context,payload metadata | pre-write auth check | SD-CACHE-WRITE | cache_write_requested | unauth write request | cache.write.requested | CACHE-020 | planned |
| cache_write_authorized | Authorize write | R-CACHE-009,R-CACHE-010 | SR-CACHE-001,SR-TOOL-001 | PP-CACHE-01,PP-TOOL-01 | tenant,subject,purpose | write principal binding | SD-CACHE-AUTHZ | cache_write_authorized | write authz mismatch | cache.write.authorized | CACHE-020,CACHE-016 | planned |
| cache_entry_metadata_validated | Validate stored metadata | R-CACHE-010 | SR-CACHE-001,SR-DLP-001 | PP-CACHE-01,PP-DLP-01 | source/document/chunk safe ids | no forbidden content | SD-CACHE-META | cache_entry_metadata_validated | sensitive raw metadata | cache.entry.metadata.validated | CACHE-019,CACHE-027 | planned |
| cache_entry_ttl_validated | Validate TTL | R-CACHE-003,R-CACHE-004 | SR-CACHE-001 | PP-CACHE-01 | ttl,acl expiry | ttl<=policy and acl expiry | SD-CACHE-TTL | cache_entry_ttl_validated | ttl exceeds policy | cache.entry.ttl.validated | CACHE-009,CACHE-010 | planned |
| cache_invalidation_requested | Start invalidation | R-CACHE-003,R-CACHE-005 | SR-CACHE-001 | PP-CACHE-01 | invalidation reason | reason must be explicit | SD-CACHE-INV | cache_invalidation_requested | invalidation missing reason | cache.invalidation.requested | CACHE-009,CACHE-011 | planned |
| cache_acl_snapshot_invalidated | Invalidate on ACL change | R-CACHE-003 | SR-CACHE-001,SR-RET-001 | PP-CACHE-01,PP-RET-02 | acl snapshot id/version | invalidate stale snapshot | SD-CACHE-ACL | cache_acl_snapshot_invalidated | stale ACL hit observed | cache.invalidation.acl_snapshot | CACHE-009 | planned |
| cache_deleted_or_stale_invalidated | Invalidate deleted/stale docs | R-CACHE-004,R-CACHE-005 | SR-CACHE-001,SR-ING-001 | PP-CACHE-01,PP-ING-02 | doc status,connector drift marker | invalidate deleted/stale entries | SD-CACHE-STALE | cache_deleted_or_stale_invalidated | stale deleted doc served | cache.invalidation.deleted_stale | CACHE-010,CACHE-011 | planned |
| cache_audit_written | Persist audit event | R-CACHE-010 | SR-AUDIT-001 | PP-AUDIT-01 | event id,time,actor,result | structured audit completeness | SD-CACHE-SAFE | cache_audit_written | missing audit fields | cache.audit.written | CACHE-024 | planned |
| cache_finding_recorded_if_needed | Emit findings on policy violations | R-CACHE-001..R-CACHE-010 | SR-EVIDENCE-001 | PP-EVIDENCE-01 | risk,stage,severity | finding emission threshold | SD-CACHE-SAFE | cache_finding_recorded | high severity mismatch/violation | cache.finding.recorded | CACHE-026 | planned |

## Known Limitations
- Design-only: no live cache enforcement wired.
- No shadow-deny or enforce activation.
- No live cache/retrieval/vector blocking/filtering.
- No application behavior change in this step.

## Step 20B Update (2026-05-28)
- Implemented minimal isolated cache security controls under `backend/security_layer/cache/`.
- No live cache/retrieval/vector/search integration added.
- Production enforcement remains inactive.
