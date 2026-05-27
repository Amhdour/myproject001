# Retrieval Security Tests Design (Step 18A)

## Purpose
Define the planned retrieval security test suite for ACL, data lineage, and non-leakage assurance before any shadow-deny or enforce rollout.

## Scope
Design-only test planning for retrieval-path security validation across disabled, monitor-only, future shadow-deny, and future enforce modes.

## Status
planned/design

## Owner
Security + Retrieval Engineering

## Non-Claim Statement
This document does **not** claim implemented enforcement, implemented blocking/filtering, or production activation of denial behavior.

## Relationships
- Retrieval ACL controls: validates and traces requirements from `docs/security/retrieval_acl.md`.
- Monitor-only live hook: validates non-blocking telemetry behavior in `search_runner.py` + `live_monitor_adapter.py`.
- Future shadow-deny/enforce: defines preconditions and test expectations before activation.

## Test Safety Principles
- No real customer data.
- No production enforcement toggles.
- Fail-safe test harness defaults to disabled or monitor-only.
- Generic safe-denial assertions for future enforce.

## Test Data Rules
- Synthetic tenants/users/groups/roles/documents/chunks only.
- Secrets redacted; no real connector IDs, tokens, file content, or customer identifiers.
- Deterministic fixtures for repeatable evidence.

## Test Models
- Tenant isolation test model
- Subject/user/group/role test model
- Document ACL test model
- Chunk ACL test model
- Vector namespace test model
- Vector metadata test model
- Stale ACL test model
- Deleted document test model
- Connector permission drift test model
- Cache bypass test model
- Reranker reintroduction test model
- Citation leakage test model
- Context assembly leakage test model
- Prompt context leakage test model
- Monitor-only behavior tests
- Shadow-deny future tests
- Enforce-mode future tests
- Non-leakage tests
- Behavior-preservation tests

## Evidence Requirements
Audit/finding/metric samples, mode-delta artifacts, non-leakage proofs, and traceability coverage.

## Known Limitations
Design-only; suite not yet implemented. Shadow-deny/enforce remain blocked pending implementation + passing evidence.

## Retrieval Security Test Groups
Each group status: **planned**.

### RST-G01 tenant isolation
Purpose: same-tenant allowed and cross-tenant unsafe-path detection.
Mapped risks: R-RET-001, R-RTEST-001. Requirements: SR-RET-001. Patch candidates: PP-RET-01/02. Fixtures: tenant_a, tenant_b, document_cross_tenant, chunk_cross_tenant. Planned cases: same-tenant allow, cross-tenant detect/deny-by-mode. Evidence: decision log + matrix row.

### RST-G02 subject identity
Purpose: subject binding validation. Risks: R-RET-001. Requirements: SR-RET-001. Patch: PP-RET-01. Fixtures: user_allowed, user_denied. Cases: missing subject, mismatched subject. Evidence: audit sample.

### RST-G03 group/role authorization
Purpose: group/role mismatch detection. Risks: R-RET-001. Requirements: SR-RET-001. Patch: PP-RET-01. Fixtures: group_allowed/denied, role_allowed/denied. Cases: unauthorized group flagged, unauthorized role flagged. Evidence: finding sample.

### RST-G04 document ACL
Purpose: document-level authorization behavior by mode. Risks: R-RET-001. Requirements: SR-RET-001. Patch: PP-RET-02. Fixtures: document_allowed, document_cross_tenant, document_deleted. Cases: allow/flag/future deny. Evidence: candidate trace.

### RST-G05 chunk ACL
Purpose: chunk-level authorization behavior by mode. Risks: R-RET-002. Requirements: SR-RET-001. Patch: PP-RET-02. Fixtures: chunk_allowed, chunk_cross_tenant, chunk_denied_group, chunk_denied_role. Cases: allow/flag/future deny. Evidence: chunk trace.

### RST-G06 vector namespace
Purpose: namespace mismatch detection. Risks: R-RET-003. Requirements: SR-VEC-001. Patch: PP-VEC-01. Fixtures: vector_namespace_allowed/denied. Cases: mismatch flagged and future denied. Evidence: vector check logs.

### RST-G07 vector metadata
Purpose: metadata integrity checks. Risks: R-RET-003. Requirements: SR-VEC-001. Patch: PP-VEC-02. Fixtures: vector_metadata_allowed/denied. Cases: missing/mismatch flagged and future denied. Evidence: metadata trace.

### RST-G08 stale ACL
Purpose: stale authorization detection. Risks: R-RET-004. Requirements: SR-RET-001. Patch: PP-RET-02. Fixtures: stale_acl_snapshot, fresh_acl_snapshot. Cases: stale flagged/future denied. Evidence: stale audit.

### RST-G09 deleted document
Purpose: tombstoned document handling. Risks: R-RET-005. Requirements: SR-RET-001. Patch: PP-RET-02. Fixtures: document_deleted. Cases: deleted flagged/future denied. Evidence: tombstone trace.

### RST-G10 connector permission drift
Purpose: drift detection telemetry. Risks: R-RET-009. Requirements: SR-AUDIT-001. Patch: PP-AUDIT-02. Fixtures: stale/fresh snapshot pairs. Cases: drift finding emitted. Evidence: finding + metric.

### RST-G11 cache bypass
Purpose: ensure cache cannot bypass ACL in future enforce. Risks: R-RET-008, R-RTEST-005. Requirements: SR-CACHE-001. Patch: PP-CACHE-01. Fixtures: cache_entry_allowed, cache_entry_cross_tenant. Cases: allowed hit, denied hit (future enforce). Evidence: cache trace.

### RST-G12 reranker reintroduction
Purpose: prevent unauthorized candidate reintroduction. Risks: R-RET-006. Requirements: SR-RET-001. Patch: PP-RET-02. Fixtures: rerank_candidate_allowed/denied. Cases: future enforce removal. Evidence: pre/post rerank diff.

### RST-G13 citation leakage
Purpose: citation source authorization and leakage checks. Risks: R-RET-007. Requirements: SR-RET-001. Patch: PP-RET-02. Fixtures: citation_allowed, citation_denied. Cases: denied source removed in enforce. Evidence: citation diff.

### RST-G14 context assembly leakage
Purpose: unauthorized chunk exclusion from context assembly. Risks: R-RET-002. Requirements: SR-RET-001. Patch: PP-RET-02. Fixtures: chunk_denied_* . Cases: enforce exclusion. Evidence: context chunk list.

### RST-G15 prompt context leakage
Purpose: unauthorized text exclusion from prompt context. Risks: R-RET-010. Requirements: SR-PROMPT-001. Patch: PP-PROMPT-01. Fixtures: chunk_denied_*, citation_denied. Cases: enforce redaction/exclusion. Evidence: prompt lineage report.

### RST-G16 monitor-only behavior preservation
Purpose: ensure monitor-only does not change outputs. Risks: R-RTEST-002. Requirements: SR-AUDIT-001. Patch: PP-AUDIT-01. Fixtures: allowed + denied candidates. Cases: output equivalence + hook failure fail-open. Evidence: response diff=none.

### RST-G17 non-leakage and safe denial
Purpose: no sensitive text in telemetry and generic safe denial in future enforce. Risks: R-RTEST-003/R-RTEST-006. Requirements: SR-AUDIT-001, SR-RET-001. Patch: PP-AUDIT-01/02. Fixtures: synthetic secret markers. Cases: telemetry redaction + generic deny text. Evidence: payload scan.

### RST-G18 audit/finding/metric evidence
Purpose: observability completeness. Risks: R-RTEST-006. Requirements: SR-AUDIT-001. Patch: PP-AUDIT-01/02. Fixtures: monitor-only unsafe candidates. Cases: audit/finding/metric emitted. Evidence: event snapshots.

### RST-G19 future shadow-deny behavior
Purpose: shadow deny records deny without live block. Risks: R-RTEST-004. Requirements: SR-AUDIT-001. Patch: PP-AUDIT-01. Fixtures: unauthorized candidates. Cases: deny decision with unchanged output. Evidence: mode delta log.

### RST-G20 future enforce-mode behavior
Purpose: live blocking/filtering behavior validation prerequisites. Risks: R-RTEST-004/R-RTEST-005. Requirements: SR-RET-001. Patch: PP-RET-02, PP-CACHE-01, PP-PROMPT-01. Fixtures: cross-tenant/denied/cached/rerank sets. Cases: safe deny + unauthorized exclusion + no reintroduction. Evidence: enforcement regression pack.

## Step 18B Implementation Note (2026-05-27)
- Safe fake retrieval security fixtures implemented in `backend/security_layer/tests/retrieval_security_fixtures.py`.
- Monitor-only retrieval security skeleton tests implemented in `backend/security_layer/tests/test_retrieval_security_monitor_only.py`.
- Future shadow-deny/enforce skeletons added in `backend/security_layer/tests/test_retrieval_security_future_modes.py` and marked skipped/xfail (`future mode not enabled yet`).
- No enforcement enabled in this step.

## Step 18B-A Execution Cleanup (2026-05-27)
- Executed `PYTHONPATH=. python -m pytest backend/security_layer/tests -q` -> `73 passed, 8 skipped`.
- Executed direct Step 18B skeleton suite -> `6 passed, 8 skipped`.
- Step 18B tests are now validated as passing evidence.

## Step 18C Validation Update (2026-05-27)
- Fixture quality validated (synthetic-only, non-leaking, deterministic IDs).
- Monitor-only skeleton behavior validated as non-blocking/non-filtering with telemetry evidence.
- Future shadow-deny/enforce skeletons remain skipped/xfail (`future mode not enabled yet`).
- No enforcement mode enabled.

## Step 18D-A coverage cleanup (2026-05-27)

Added explicit retrieval security negative-case coverage in `backend/security_layer/tests/test_retrieval_security_negative_cases.py` to satisfy acceptance threshold (>=10 negative tests) while preserving monitor-only behavior.
