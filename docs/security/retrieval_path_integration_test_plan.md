# Retrieval Path Integration Test Plan (Step 17B)

Status: planned/test-plan

## Planned Tests

| Test ID | Purpose | Mapped Requirement | Mapped Risk | Mapped Patch Candidate | Expected Result | Planned Evidence |
|---|---|---|---|---|---|---|
| RPIT-001 | Validate config flag defaults to monitor-only or disabled. | SR-RET-001, SR-CI-001 | R-RINT-002 | RPC-001, RPC-002 | Unsafe default is prevented. | Config snapshot + test output. |
| RPIT-002 | Validate retrieval context builder creates subject context. | SR-RET-001 | R-RINT-006 | RPC-003 | Subject fields present when identity exists. | Unit test logs. |
| RPIT-003 | Validate retrieval context builder creates tenant context. | SR-RET-001 | R-RINT-006 | RPC-003 | Tenant/workspace fields normalized. | Unit test logs. |
| RPIT-004 | Validate context builder handles missing subject safely. | SR-RET-001 | R-RINT-006 | RPC-004 | Missing subject yields safe/neutral handling. | Unit test output + denial category sample. |
| RPIT-005 | Validate context builder handles missing tenant safely. | SR-RET-001 | R-RINT-006 | RPC-004 | Missing tenant handled safely without leakage. | Unit test output. |
| RPIT-006 | Validate monitor-only hook records decision and does not block. | SR-RET-001 | R-RINT-003 | RPC-005 | Request continues while decision is recorded. | Integration logs showing non-blocking path. |
| RPIT-007 | Validate audit event created from monitor-only hook. | SR-AUDIT-001 | R-RINT-001 | RPC-008 | Structured audit event emitted. | Audit sample record. |
| RPIT-008 | Validate finding recorded for unsafe candidate in monitor-only. | SR-AUDIT-001 | R-RINT-001 | RPC-009 | Unsafe pattern creates finding, no block. | Finding sample record. |
| RPIT-009 | Validate metric emitted from hook. | SR-AUDIT-001 | R-RINT-001 | RPC-009 | Metric increments with decision outcome labels. | Metric snapshot/export. |
| RPIT-010 | Validate shadow-deny records denial and does not block. | SR-RET-001 | R-RINT-003 | RPC-010 | Shadow deny is recorded; response remains allowed. | Shadow diff report. |
| RPIT-011 | Validate enforce mode blocks cross-tenant document. | SR-RET-001 | R-RINT-001 | RPC-011 | Cross-tenant candidate removed/denied. | Integration evidence + deny logs. |
| RPIT-012 | Validate enforce mode blocks unauthorized chunk. | SR-RET-001 | R-RINT-001 | RPC-012 | Unauthorized chunk excluded before context assembly. | Candidate filter logs. |
| RPIT-013 | Validate safe denial returned in enforce mode. | SR-RET-001 | R-RINT-004 | RPC-013 | Denial response is safe and non-leaking. | Response capture + safe-denial assertion. |
| RPIT-014 | Validate feature flag disables hook safely. | SR-CI-001 | R-RINT-002 | RPC-002 | Hook bypassed with no behavior change. | Disabled-mode regression output. |
| RPIT-015 | Validate rollback removes/neutralizes hook. | SR-EVIDENCE-001 | R-RINT-005 | RPC-015 | Rollback returns expected neutral behavior. | Rollback rehearsal logs. |
| RPIT-016 | Validate no unauthorized candidate reaches context assembly in enforce mode. | SR-RET-001 | R-RINT-001 | RPC-014 | Unauthorized candidate absent from final context input. | Context assembly trace evidence. |
| RPIT-017 | Validate no unauthorized source appears in citation in enforce mode. | SR-RET-001 | R-RINT-001 | RPC-014 | Unauthorized source references suppressed. | Citation output evidence. |
| RPIT-018 | Validate cache read cannot bypass retrieval ACL in enforce mode. | SR-CACHE-001, SR-RET-001 | R-RINT-001 | RPC-014 | Cached candidate still ACL-checked and denied if unauthorized. | Cache + ACL decision logs. |
| RPIT-019 | Validate no unrelated retrieval behavior changes in disabled mode. | SR-CI-001 | R-RINT-001 | RPC-016, RPC-017 | Baseline retrieval parity maintained when disabled. | Regression diff report. |
\n## Step 17C Update\n- Isolated feature-flag helper implemented.\n- Isolated retrieval context builder implemented.\n- Isolated monitor/shadow/enforce hook helper implemented.\n- No live retrieval path patched; production enforcement remains inactive.
