# Runtime Context Wrappers Test Plan (Step 13A)

Status: planned (design only, no runtime integration).

| Test ID | Purpose | Mapped requirement | Mapped risk | Mapped patch point | Expected result | Planned evidence |
|---|---|---|---|---|---|---|
| TC-RW-001 | request context creation | SR-AUDIT-001 | R-WRAP-004 | PP-AUDIT-01 | RequestContext built with IDs and route metadata | unit test output + fixture sample |
| TC-RW-002 | subject context creation | SR-RET-001 | R-WRAP-001 | PP-RET-01 | SubjectContext built with principal and role fields | unit test output |
| TC-RW-003 | tenant context creation | SR-RET-001 | R-WRAP-001 | PP-RET-01 | TenantContext built with tenant partition fields | unit test output |
| TC-RW-004 | missing tenant blocked | SR-RET-001 | R-WRAP-001 | PP-RET-01 | Wrapper returns deny/safe-fail when tenant missing | deny-path test log |
| TC-RW-005 | missing subject blocked | SR-RET-001 | R-WRAP-001 | PP-RET-01 | Wrapper returns deny/safe-fail when subject missing | deny-path test log |
| TC-RW-006 | retrieval wrapper allow path | SR-RET-001 | R-WRAP-005 | PP-RET-01 | allow decision path recorded | decision fixture + audit event |
| TC-RW-007 | retrieval wrapper deny path | SR-RET-001 | R-WRAP-002 | PP-RET-01 | deny decision triggers safe denial handling | denial assertion record |
| TC-RW-008 | vector wrapper deny path | SR-VEC-001 | R-WRAP-005 | PP-VEC-01 | unauthorized vector query denied | vector deny test output |
| TC-RW-009 | cache wrapper deny path | SR-CACHE-001 | R-WRAP-005 | PP-CACHE-01 | unauthorized cache access denied | cache deny test output |
| TC-RW-010 | tool wrapper approval-required path | SR-APPROVAL-001 | R-WRAP-002 | PP-TOOL-01 | policy returns approval_required and blocks until approved | approval-required test output |
| TC-RW-011 | MCP wrapper deny path | SR-MCP-001 | R-WRAP-005 | PP-MCP-01 | unauthorized mcp action denied | mcp deny test output |
| TC-RW-012 | artifact wrapper redaction/block path | SR-ART-001 | R-WRAP-003 | PP-ART-01 | sensitive artifact denied or marked redact_required | artifact decision record |
| TC-RW-013 | sandbox wrapper deny path | SR-SBX-001 | R-WRAP-002 | PP-SBX-01 | unsafe execution denied | sandbox deny log |
| TC-RW-014 | model call wrapper policy path | SR-MODEL-001 | R-WRAP-005 | PP-MODEL-01 | model/provider route evaluated per policy | model wrapper test output |
| TC-RW-015 | prompt wrapper policy path | SR-PROMPT-001 | R-WRAP-003 | PP-PROMPT-01 | prompt usage decision emitted | prompt wrapper test output |
| TC-RW-016 | approval wrapper path | SR-APPROVAL-001 | R-WRAP-002 | PP-APPROVAL-01 | require_human_approval enforces proceed/block contract | approval wrapper assertions |
| TC-RW-017 | audit event generated for decision | SR-AUDIT-001 | R-WRAP-004 | PP-AUDIT-01 | write_audit_event invoked for each decision | audit emission test output |
| TC-RW-018 | finding generated for violation | SR-EVIDENCE-001 | R-WRAP-004 | PP-EVIDENCE-01 | record_finding called on violation/engine error | finding emission output |
| TC-RW-019 | metric emitted for decision | SR-EVIDENCE-001 | R-WRAP-004 | PP-EVIDENCE-01 | emit_security_metric called with mode/status labels | metric emission output |
| TC-RW-020 | safe denial raised | SR-RET-001 | R-WRAP-003 | PP-RET-01 | raise_security_denial redacts sensitive detail | denial payload assertion |
| TC-RW-021 | fail-closed when policy engine unavailable | SR-RET-001 | R-WRAP-002 | PP-RET-01 | policy engine failure results in deny + finding | fail-closed test output |
| TC-RW-022 | monitor-only mode behavior | SR-AUDIT-001 | R-WRAP-004 | PP-AUDIT-01 | deny decision logged while action allowed | mode behavior test output |
| TC-RW-023 | shadow-deny mode behavior | SR-AUDIT-001 | R-WRAP-004 | PP-AUDIT-01 | shadow deny recorded without blocking action | shadow decision output |
| TC-RW-024 | no runtime integration yet | SR-EVIDENCE-001 | R-WRAP-005 | PP-EVIDENCE-01 | confirms wrappers remain unbound from request paths | integration-absence checklist |

## Step 13B Status
- [x] request context creation
- [x] subject context creation
- [x] tenant context creation
- [x] wrapper allow/deny/approval paths and mode handling
- [x] audit/finding/metric emission assertions

## Step 13C Coverage Status (2026-05-27)
- Coverage executed in isolated tests: `PYTHONPATH=. python -m pytest backend/security_layer/tests -q`
- Result: 36 passed.
- All wrapper function entry points are now explicitly covered.
- Added/confirmed checks for fail-closed behavior, mode handling, side-effect emission, and safe denial non-leak constraints.
