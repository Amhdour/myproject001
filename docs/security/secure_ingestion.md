# Secure Ingestion Design (Step 15A)

## Purpose
Define a design-only secure-ingestion control model for future integration into Onyx ingestion paths.

## Scope
Documentation, traceability, and test-planning only. No runtime wiring, no enforcement activation, and no application behavior changes.

## Status
planned/design

## Owner
AI Trust & Security Readiness Engineer

## Non-Claim Statement
This document does not claim implemented controls, effective enforcement, compliance, or production readiness.

## Relationship to Policy Engine
Planned ingestion decisions reference isolated policy engine contracts under `backend/security_layer/policies` only as design dependencies.

## Relationship to Runtime Wrappers
Planned ingestion controls are intended to be evaluated via isolated runtime wrapper patterns under `backend/security_layer/runtime` in a future integration step.

## Relationship to Safe Denial Behavior
All deny paths are designed to map to safe-denial categories in `backend/security_layer/runtime/denials.py`; no live path is wired.

## Ingestion Threat Model
- Cross-tenant contamination during upload or connector sync.
- Poisoned or prompt-injection-bearing documents entering indexing.
- Missing/stale ACL ownership metadata enabling unauthorized retrieval.
- Unsafe file type/size/count abuse impacting availability or safety.
- Missing provenance/source attribution reducing forensic trust.

## Ingestion Trust Boundaries
- External source (connector/system) -> ingestion entrypoint.
- Upload/API caller -> tenant/workspace boundary.
- Parser/chunker/embedding/vector subsystems (internal trust but policy-gated).
- Security policy decision/audit/finding recording plane.

## Ingestion Entrypoints
- User file upload requests.
- Connector sync starts and per-document processing.
- Re-ingestion/update/deletion reconciliation flows.

## Security Models
### Connector ingestion security model
Connector identity, owner subject, tenant context, and ACL snapshot are required before indexing progression.

### File upload security model
Upload requires tenant + subject context, validated source attribution, type/size/count checks, and provenance intent.

### Parser security model
Parser must be selected from approved parser classes; parser errors map to safe denial and finding conditions.

### Chunking security model
Chunks inherit immutable tenant/ownership/provenance metadata; missing metadata blocks downstream stages.

### Embedding security model
Embedding request requires previously authorized context and chunk metadata completeness.

### Vector write security model
Vector write is planned as a separate authorization checkpoint gated by tenant, ACL, provenance, and decision mode.

### Metadata validation model
Required metadata: tenant_id, workspace_id (if applicable), subject_id/owner_id, source_id, source_type, content_type, document_id, ingestion_timestamp.

### Document ownership model
Each document must bind to a canonical owner subject and tenant scope with explicit unknown-owner denial behavior.

### Tenant/workspace boundary model
Tenant boundary is mandatory; workspace segmentation (if used) must be validated before parser and vector stages.

### ACL propagation model
ACL snapshot captured early and attached through parser/chunk/embedding/vector stages; stale snapshot triggers block/deny plan.

### Provenance requirements
Every document requires provenance fields (source system, source object identifier, ingestion timestamp, checksum/hash placeholder).

### Source attribution requirements
Source attribution must include source_type and source_id; missing attribution is deny-path planned behavior.

### Content-type validation requirements
Allowlist-based validation by source category; unsupported/malformed types denied.

### File-size and file-count controls
Planned limits include per-file max size and per-request file count caps with explicit deny metrics.

### Malware/unsafe-content placeholder requirements
Placeholder hooks only (no runtime integration yet) for malware/unsafe-content scanners and findings.

### Prompt-injection-in-document handling
Documents with prompt-injection indicators are flagged findings; mode-specific block behavior is planned for later enforcement mode.

### Poisoned document handling
Poisoning indicators produce findings and planned deny/shadow-deny decisions depending on mode.

### Sensitive-data detection placeholder requirements
Placeholder DLP/sensitive data checks are planned; findings-only behavior in monitor-only mode.

### Duplicate/stale/deleted document handling
Duplicate documents are deduplicated/safely handled; stale ACL or deleted source state blocks re-index/vector write.

## Ingestion Audit Events
Planned event family: `security.ingestion.*` including stage decisions, denial categories, and mode.

## Ingestion Findings
Planned findings for poisoning, prompt-injection indicators, sensitive-data placeholder hits, stale ACL, missing provenance.

## Ingestion Metrics
Planned counters/timers: stage decision counts, deny counts by category, finding counts, latency by stage, mode-specific deny shadow counts.

## Safe Denial Behavior for Ingestion
Safe denials must avoid leaking document name/content/source secrets and return only category + minimal reason code.

## Monitor-only / Shadow-deny / Enforce-mode Plan
- monitor-only: record allow/deny decision and findings without live block.
- shadow-deny: record hypothetical deny where current live path continues.
- enforce-mode: future-only plan to block unsafe paths.

## Test Strategy
Use `docs/security/secure_ingestion_test_plan.md` for explicit planned cases mapped to requirements/risks/patch points.

## Evidence Requirements
- Stage inventory and mapping evidence.
- Test-plan summary and traceability summary.
- Prerequisite verification and remote-sync limitation note when applicable.

## Known Limitations
Design-only artifact; no runtime enforcement or path integration is active.

## Secure Ingestion Stages (Planned)

### SI-01 upload_received
- **Stage ID:** SI-01
- **Purpose:** Capture upload request context and initialize ingestion decision context.
- **Mapped risks:** R-ING-001, R-ING-007
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** tenant_id, subject_id, request_id, source_type, file_count
- **Planned policy check:** deny if tenant/subject missing or file_count above limit.
- **Safe denial category:** missing_context_or_limit
- **Audit event:** security.ingestion.upload_received
- **Finding condition:** malformed metadata or anomalous file count.
- **Metric:** ingestion_upload_received_total, ingestion_upload_denied_total
- **Planned tests:** SITP-001, SITP-002, SITP-007
- **Implementation status:** planned

### SI-02 connector_sync_started
- **Stage ID:** SI-02
- **Purpose:** Validate connector sync request is tenant/owner scoped.
- **Mapped risks:** R-ING-001, R-ING-008
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-02
- **Required context fields:** tenant_id, connector_id, owner_id, sync_id
- **Planned policy check:** deny if tenant or owner missing.
- **Safe denial category:** missing_connector_context
- **Audit event:** security.ingestion.connector_sync_started
- **Finding condition:** connector permission drift signal.
- **Metric:** connector_sync_denied_total
- **Planned tests:** SITP-003, SITP-004
- **Implementation status:** planned

### SI-03 source_metadata_validated
- **Stage ID:** SI-03
- **Purpose:** Validate source attribution and required metadata fields.
- **Mapped risks:** R-ING-005, R-ING-006
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** source_id, source_type, content_type, document_id
- **Planned policy check:** deny if source attribution/provenance primitives missing.
- **Safe denial category:** metadata_validation_failed
- **Audit event:** security.ingestion.source_metadata_validated
- **Finding condition:** suspicious/malformed source metadata.
- **Metric:** ingestion_metadata_validation_failures_total
- **Planned tests:** SITP-018, SITP-019
- **Implementation status:** planned

### SI-04 tenant_boundary_validated
- **Stage ID:** SI-04
- **Purpose:** Confirm tenant/workspace boundary validity before processing.
- **Mapped risks:** R-ING-001
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01, PP-ING-02
- **Required context fields:** tenant_id, workspace_id, document_tenant_id
- **Planned policy check:** deny/block on mismatch or missing boundary fields.
- **Safe denial category:** tenant_boundary_violation
- **Audit event:** security.ingestion.tenant_boundary_validated
- **Finding condition:** cross-tenant mismatch detected.
- **Metric:** ingestion_tenant_boundary_violations_total
- **Planned tests:** SITP-015
- **Implementation status:** planned

### SI-05 ownership_validated
- **Stage ID:** SI-05
- **Purpose:** Validate document ownership subject.
- **Mapped risks:** R-ING-001, R-ING-008
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-02
- **Required context fields:** owner_id, subject_id, tenant_id
- **Planned policy check:** deny if owner missing or inconsistent.
- **Safe denial category:** ownership_validation_failed
- **Audit event:** security.ingestion.ownership_validated
- **Finding condition:** owner/subject drift.
- **Metric:** ingestion_ownership_denied_total
- **Planned tests:** SITP-004
- **Implementation status:** planned

### SI-06 acl_snapshot_captured
- **Stage ID:** SI-06
- **Purpose:** Capture ACL snapshot for propagation.
- **Mapped risks:** R-ING-004, R-ING-008
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-02
- **Required context fields:** acl_snapshot_id, acl_version, acl_captured_at
- **Planned policy check:** deny/block if missing or stale snapshot.
- **Safe denial category:** acl_snapshot_invalid
- **Audit event:** security.ingestion.acl_snapshot_captured
- **Finding condition:** stale ACL snapshot.
- **Metric:** ingestion_acl_snapshot_invalid_total
- **Planned tests:** SITP-008, SITP-009
- **Implementation status:** planned

### SI-07 content_type_validated
- **Stage ID:** SI-07
- **Purpose:** Enforce content-type allowlist.
- **Mapped risks:** R-ING-006
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** content_type, source_type
- **Planned policy check:** deny unsupported content type.
- **Safe denial category:** content_type_disallowed
- **Audit event:** security.ingestion.content_type_validated
- **Finding condition:** suspicious/unknown media type.
- **Metric:** ingestion_content_type_denied_total
- **Planned tests:** SITP-005
- **Implementation status:** planned

### SI-08 file_size_validated
- **Stage ID:** SI-08
- **Purpose:** Enforce per-file size and request file-count limits.
- **Mapped risks:** R-ING-007
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** file_size_bytes, file_count, tenant_id
- **Planned policy check:** deny if thresholds exceeded.
- **Safe denial category:** size_or_count_limit_exceeded
- **Audit event:** security.ingestion.file_size_validated
- **Finding condition:** repeated upload abuse pattern.
- **Metric:** ingestion_size_count_denied_total
- **Planned tests:** SITP-006, SITP-007
- **Implementation status:** planned

### SI-09 parser_selected
- **Stage ID:** SI-09
- **Purpose:** Select approved parser for content type.
- **Mapped risks:** R-ING-006
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** parser_id, content_type, source_type
- **Planned policy check:** deny if parser not approved for type.
- **Safe denial category:** parser_selection_denied
- **Audit event:** security.ingestion.parser_selected
- **Finding condition:** fallback parser used unexpectedly.
- **Metric:** ingestion_parser_selection_denied_total
- **Planned tests:** SITP-010
- **Implementation status:** planned

### SI-10 parser_completed
- **Stage ID:** SI-10
- **Purpose:** Validate parser outcome before chunking/indexing.
- **Mapped risks:** R-ING-002, R-ING-003
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** parser_status, parse_error_code, extracted_text_hash
- **Planned policy check:** safe deny on parser failure or unsafe parse indicators.
- **Safe denial category:** parser_failure_or_unsafe_output
- **Audit event:** security.ingestion.parser_completed
- **Finding condition:** parse anomaly / unsafe markers.
- **Metric:** ingestion_parser_failure_total
- **Planned tests:** SITP-010, SITP-011, SITP-012
- **Implementation status:** planned

### SI-11 chunks_created
- **Stage ID:** SI-11
- **Purpose:** Create chunks with bounded metadata consistency.
- **Mapped risks:** R-ING-002, R-ING-010
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** chunk_count, chunk_ids, document_id
- **Planned policy check:** block/flag if chunk metadata invalid or suspicious.
- **Safe denial category:** chunk_integrity_failed
- **Audit event:** security.ingestion.chunks_created
- **Finding condition:** poisoned chunk indicators.
- **Metric:** ingestion_chunk_integrity_failures_total
- **Planned tests:** SITP-011, SITP-013
- **Implementation status:** planned

### SI-12 chunk_metadata_attached
- **Stage ID:** SI-12
- **Purpose:** Attach tenant/owner/ACL/provenance metadata to chunks.
- **Mapped risks:** R-ING-001, R-ING-004, R-ING-005
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-02
- **Required context fields:** chunk_id, tenant_id, owner_id, acl_snapshot_id, provenance_id
- **Planned policy check:** deny if mandatory metadata missing.
- **Safe denial category:** chunk_metadata_missing
- **Audit event:** security.ingestion.chunk_metadata_attached
- **Finding condition:** metadata propagation gap.
- **Metric:** ingestion_chunk_metadata_missing_total
- **Planned tests:** SITP-018, SITP-019
- **Implementation status:** planned

### SI-13 embedding_requested
- **Stage ID:** SI-13
- **Purpose:** Permit embeddings only for validated chunk contexts.
- **Mapped risks:** R-ING-002, R-ING-003
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** embedding_request_id, chunk_ids, tenant_id, acl_snapshot_id
- **Planned policy check:** block if prior validation stages incomplete.
- **Safe denial category:** embedding_request_unauthorized
- **Audit event:** security.ingestion.embedding_requested
- **Finding condition:** embedding requested before metadata complete.
- **Metric:** ingestion_embedding_request_denied_total
- **Planned tests:** SITP-014
- **Implementation status:** planned

### SI-14 vector_write_authorized
- **Stage ID:** SI-14
- **Purpose:** Final authorize step before vector index writes.
- **Mapped risks:** R-ING-001, R-ING-009
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-02
- **Required context fields:** tenant_id, vector_namespace, acl_snapshot_id, document_deleted_flag
- **Planned policy check:** deny cross-tenant, unauthorized, or deleted-doc writes.
- **Safe denial category:** vector_write_denied
- **Audit event:** security.ingestion.vector_write_authorized
- **Finding condition:** attempted write for deleted doc or namespace mismatch.
- **Metric:** ingestion_vector_write_denied_total
- **Planned tests:** SITP-014, SITP-015, SITP-016
- **Implementation status:** planned

### SI-15 provenance_recorded
- **Stage ID:** SI-15
- **Purpose:** Persist provenance and source attribution evidence.
- **Mapped risks:** R-ING-005
- **Mapped requirements:** SR-ING-001
- **Mapped patch points:** PP-ING-01
- **Required context fields:** provenance_id, source_id, source_type, checksum
- **Planned policy check:** deny if provenance/source attribution incomplete.
- **Safe denial category:** provenance_missing
- **Audit event:** security.ingestion.provenance_recorded
- **Finding condition:** incomplete attribution record.
- **Metric:** ingestion_provenance_missing_total
- **Planned tests:** SITP-018, SITP-019
- **Implementation status:** planned

### SI-16 ingestion_audit_written
- **Stage ID:** SI-16
- **Purpose:** Ensure ingestion decision audit event persisted.
- **Mapped risks:** R-ING-005
- **Mapped requirements:** SR-AUDIT-001
- **Mapped patch points:** PP-AUDIT-01
- **Required context fields:** audit_event_id, decision, mode, stage_id
- **Planned policy check:** finding if audit event missing.
- **Safe denial category:** audit_write_failure
- **Audit event:** security.ingestion.audit_written
- **Finding condition:** audit persistence failure.
- **Metric:** ingestion_audit_write_failures_total
- **Planned tests:** SITP-020, SITP-022, SITP-023, SITP-024, SITP-025
- **Implementation status:** planned

### SI-17 ingestion_finding_recorded_if_needed
- **Stage ID:** SI-17
- **Purpose:** Record findings for unsafe/suspicious ingestion outcomes.
- **Mapped risks:** R-ING-002, R-ING-003, R-ING-010
- **Mapped requirements:** SR-AUDIT-001, SR-DLP-001
- **Mapped patch points:** PP-AUDIT-02, PP-DLP-01
- **Required context fields:** finding_id, finding_type, severity, stage_id, decision_mode
- **Planned policy check:** create finding when unsafe condition indicators present.
- **Safe denial category:** finding_recorded
- **Audit event:** security.ingestion.finding_recorded
- **Finding condition:** poison/prompt-injection/sensitive-data placeholder matched.
- **Metric:** ingestion_findings_total
- **Planned tests:** SITP-011, SITP-012, SITP-013, SITP-021, SITP-026
- **Implementation status:** planned

## Step 15B Implementation Note (2026-05-27)
- Minimal isolated ingestion controls implemented under `backend/security_layer/ingestion/`.
- No live ingestion integration.
- No parser/chunker/embedder/vector DB integration.
- No production enforcement active.

## Step 15C Validation Note (2026-05-27)
- Completed isolated validation cleanup for secure ingestion controls under `backend/security_layer/ingestion`.
- Verified controls remain isolated and are not wired into live ingestion, connector, parser, chunking, embedding, indexing, worker, web, or deployment runtime paths.
- Added/strengthened isolated tests for 17 ingestion stages, denial categories, findings/audit/metrics emission, and non-leakage expectations.
- No production-path enforcement activation was introduced in this step.
