# Vector DB Security Test Plan (Step 19A)

Status: planned/design only.

| Test ID | Purpose | Mapped Requirement | Mapped Risk | Mapped Patch Point | Expected Result | Planned Evidence | Implementation Status |
|---|---|---|---|---|---|---|---|
| VEC-TST-001 | vector write without tenant denied | SR-VEC-001 | R-VEC-001 | PP-VEC-01 | safe deny + audit/finding as configured | test case spec + planned audit sample | planned |
| VEC-TST-002 | vector write without subject denied | SR-VEC-001 | R-VEC-002 | PP-VEC-01 | safe deny for missing subject | test matrix row | planned |
| VEC-TST-003 | vector write to wrong tenant namespace denied | SR-VEC-001 | R-VEC-001 | PP-VEC-01 | deny namespace mismatch; no secret leakage | namespace mismatch evidence stub | planned |
| VEC-TST-004 | vector write with missing ACL snapshot denied | SR-VEC-001 | R-VEC-003 | PP-VEC-01 | deny due missing ACL snapshot | ACL snapshot validation evidence stub | planned |
| VEC-TST-005 | vector write with stale ACL snapshot denied | SR-VEC-001 | R-VEC-003 | PP-VEC-01 | deny stale ACL snapshot | stale ACL timestamp scenario | planned |
| VEC-TST-006 | vector write with missing provenance denied | SR-VEC-001 | R-VEC-005 | PP-VEC-01 | deny missing provenance | provenance required-fields report | planned |
| VEC-TST-007 | vector write with invalid metadata denied | SR-VEC-001 | R-VEC-002 | PP-VEC-01 | deny invalid metadata schema | metadata contract validation matrix | planned |
| VEC-TST-008 | vector write with unsafe content marker flagged | SR-VEC-001 | R-VEC-006 | PP-VEC-01 | write decision flagged/finding in monitor-only | marker propagation evidence | planned |
| VEC-TST-009 | vector write with prompt-injection marker flagged | SR-VEC-001 | R-VEC-007 | PP-VEC-01 | flagged/finding and metric increment | prompt marker evidence | planned |
| VEC-TST-010 | vector query without tenant denied | SR-VEC-001 | R-VEC-001 | PP-VEC-02 | safe deny missing tenant | query deny audit sample | planned |
| VEC-TST-011 | vector query without subject denied | SR-VEC-001 | R-VEC-002 | PP-VEC-02 | safe deny missing subject | query deny matrix row | planned |
| VEC-TST-012 | vector query namespace mismatch denied | SR-VEC-001 | R-VEC-001 | PP-VEC-02 | deny query namespace mismatch | namespace filter evidence stub | planned |
| VEC-TST-013 | vector query metadata mismatch denied | SR-VEC-001 | R-VEC-002 | PP-VEC-02 | deny or flag mismatched candidate metadata | candidate metadata check log sample | planned |
| VEC-TST-014 | cross-tenant vector candidate flagged | SR-VEC-001 | R-VEC-001 | PP-VEC-02 | finding/metric raised for cross-tenant candidate | finding evidence stub | planned |
| VEC-TST-015 | deleted document vector candidate flagged | SR-VEC-001 | R-VEC-004 | PP-VEC-02 | candidate flagged as deleted and safe handled | deleted marker evidence | planned |
| VEC-TST-016 | stale vector candidate flagged | SR-VEC-001 | R-VEC-004 | PP-VEC-02 | stale candidate flagged and safe handled | stale marker evidence | planned |
| VEC-TST-017 | vector cache hit does not bypass ACL | SR-CACHE-001, SR-VEC-001 | R-VEC-008 | PP-CACHE-01, PP-VEC-02 | ACL and metadata checks still enforced on cache hit | cache policy test evidence | planned |
| VEC-TST-018 | duplicate vector handled safely | SR-VEC-001 | R-VEC-002 | PP-VEC-02 | duplicate candidates deduped/flagged safely | duplicate handling evidence | planned |
| VEC-TST-019 | re-embedding preserves ACL/provenance metadata | SR-VEC-001 | R-VEC-009 | PP-VEC-01 | ACL/provenance preserved across re-embedding | re-embedding comparison evidence | planned |
| VEC-TST-020 | monitor-only vector decision records evidence without blocking | SR-VEC-001, SR-EVIDENCE-001 | R-VEC-003 | PP-VEC-02, PP-EVIDENCE-01 | no blocking; audit/finding/metric evidence recorded | monitor-only evidence bundle | planned |
| VEC-TST-021 | shadow-deny vector decision future test remains blocked | SR-VEC-001 | R-VEC-001 | PP-VEC-02 | explicitly blocked/not enabled in this step | blocked test annotation | planned |
| VEC-TST-022 | enforce-mode vector decision future test remains blocked | SR-VEC-001 | R-VEC-001 | PP-VEC-02 | explicitly blocked/not enabled in this step | blocked test annotation | planned |
| VEC-TST-023 | audit event emitted | SR-AUDIT-001 | R-VEC-010 | PP-AUDIT-01 | required vector security audit event emitted | audit event schema sample | planned |
| VEC-TST-024 | finding emitted | SR-AUDIT-001, SR-EVIDENCE-001 | R-VEC-006 | PP-AUDIT-02, PP-EVIDENCE-01 | finding emitted when condition met | finding record sample | planned |
| VEC-TST-025 | metric emitted | SR-AUDIT-001 | R-VEC-008 | PP-AUDIT-02 | metric increment recorded | metric sample series | planned |
| VEC-TST-026 | safe denial does not reveal namespace/document/chunk/source secret | SR-VEC-001 | R-VEC-010 | PP-VEC-02 | denial response generic and non-sensitive | denial payload review evidence | planned |

## Step 19B Implementation Status (2026-05-27)
- Implemented isolated tests in `backend/security_layer/tests/test_vector_*.py` covering context denials, namespace mismatch, metadata contract validation, forbidden content rejection, ACL/provenance checks, candidate filtering/flagging, and audit/finding/metric emissions.
- Status updated: isolated helper tests implemented and executed.

## Step 19C Coverage Status (2026-05-27)
- Validation coverage executed for all isolated vector security stages (18/18).
- Metadata contract validation coverage executed for all required fields (21/21).
- Negative coverage includes forbidden metadata keys/content patterns, missing tenant/subject, namespace mismatch, missing/stale ACL snapshot, missing provenance, deleted/stale candidate filtering, and injection/poisoning markers.
- No live integration behavior was introduced by this step.
