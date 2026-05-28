# Cache Security Test Plan (Step 20A)

Status: planned/design-only.

| Test ID | Purpose | Mapped Requirement | Mapped Risk | Mapped Patch Point | Expected Result | Planned Evidence | Implementation Status |
|---|---|---|---|---|---|---|---|
| CACHE-001 | cache key without tenant denied | SR-CACHE-001 | R-CACHE-001 | PP-CACHE-01 | safe denial + audit/metric | negative test log | planned |
| CACHE-002 | cache key without subject denied | SR-CACHE-001 | R-CACHE-002 | PP-CACHE-01 | safe denial + audit/metric | negative test log | planned |
| CACHE-003 | cache key missing ACL context denied | SR-CACHE-001 | R-CACHE-003 | PP-CACHE-01 | safe denial + finding | policy trace | planned |
| CACHE-004 | cache key missing provenance denied | SR-CACHE-001 | R-CACHE-010 | PP-CACHE-01 | safe denial | policy trace | planned |
| CACHE-005 | cross-tenant cache read denied | SR-CACHE-001 | R-CACHE-001 | PP-CACHE-01 | deny/read blocked in planned mode | audit sample | planned |
| CACHE-006 | cross-subject cache read denied | SR-CACHE-001 | R-CACHE-002 | PP-CACHE-01 | deny/read blocked in planned mode | audit sample | planned |
| CACHE-007 | unauthorized group cache hit denied | SR-CACHE-001 | R-CACHE-002 | PP-CACHE-01 | deny hit reuse | test transcript | planned |
| CACHE-008 | unauthorized role cache hit denied | SR-CACHE-001 | R-CACHE-002 | PP-CACHE-01 | deny hit reuse | test transcript | planned |
| CACHE-009 | stale ACL snapshot invalidates cache | SR-CACHE-001 | R-CACHE-003 | PP-CACHE-01 | invalidate + miss | invalidation evidence | planned |
| CACHE-010 | deleted document invalidates cache | SR-CACHE-001 | R-CACHE-004 | PP-CACHE-01 | invalidate + miss | invalidation evidence | planned |
| CACHE-011 | connector permission drift invalidates cache | SR-CACHE-001 | R-CACHE-005 | PP-CACHE-01 | invalidate + finding | drift evidence | planned |
| CACHE-012 | vector cache namespace mismatch denied | SR-VEC-001 | R-CACHE-006 | PP-VEC-01 | safe denial | namespace mismatch log | planned |
| CACHE-013 | retrieval cache ACL mismatch denied | SR-RET-001 | R-CACHE-003 | PP-RET-02 | safe denial | ACL mismatch log | planned |
| CACHE-014 | prompt/context cache excludes unauthorized chunks | SR-PROMPT-001 | R-CACHE-007 | PP-PROMPT-01 | unauthorized chunks excluded | context evidence | planned |
| CACHE-015 | answer cache does not reuse unauthorized context | SR-PROMPT-001 | R-CACHE-008 | PP-PROMPT-02 | no unauthorized answer reuse | answer trace | planned |
| CACHE-016 | tool result cache does not cross tenant boundary | SR-TOOL-001 | R-CACHE-009 | PP-TOOL-01 | no cross-tenant reuse | tool cache trace | planned |
| CACHE-017 | cache poisoning marker flagged | SR-CACHE-001 | R-CACHE-007 | PP-CACHE-01 | finding emitted | finding sample | planned |
| CACHE-018 | prompt-injection marker propagated | SR-PROMPT-001 | R-CACHE-007 | PP-PROMPT-01 | marker preserved in cache metadata | metadata trace | planned |
| CACHE-019 | sensitive-data placeholder cache rule applied | SR-DLP-001 | R-CACHE-010 | PP-DLP-01 | redact/placeholder only | redaction evidence | planned |
| CACHE-020 | cache write without authorization denied | SR-CACHE-001 | R-CACHE-009 | PP-CACHE-01 | write denied safely | authz deny log | planned |
| CACHE-021 | cache read monitor-only records evidence without blocking | SR-CACHE-001 | R-CACHE-001 | PP-CACHE-01 | behavior unchanged + evidence recorded | monitor-only diff | planned |
| CACHE-022 | shadow-deny cache future test remains blocked | SR-CACHE-001 | R-CACHE-001 | PP-CACHE-01 | blocked by policy | blocker note | planned |
| CACHE-023 | enforce-mode cache future test remains blocked | SR-CACHE-001 | R-CACHE-001 | PP-CACHE-01 | blocked by policy | blocker note | planned |
| CACHE-024 | audit event emitted | SR-AUDIT-001 | R-CACHE-010 | PP-AUDIT-01 | structured audit event exists | audit artifact | planned |
| CACHE-025 | finding emitted | SR-EVIDENCE-001 | R-CACHE-003 | PP-EVIDENCE-01 | finding record exists | finding artifact | planned |
| CACHE-026 | metric emitted | SR-AUDIT-001 | R-CACHE-010 | PP-AUDIT-01 | metric emitted with stage/risk tags | metric artifact | planned |
| CACHE-027 | safe denial does not reveal cache key/document/chunk/source secret/tenant internals | SR-CACHE-001 | R-CACHE-010 | PP-CACHE-01 | denial redaction verified | safe denial transcript | planned |

## Step 20B Test Status
- Implemented isolated cache security tests: models, key contract, validators, controls.
