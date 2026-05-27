# Retrieval Path Patching Test Plan (Step 17A)

Design-only planned tests for future runtime patch integration.

| test ID | purpose | mapped requirement | mapped risk | mapped patch point | mapped patch candidate | expected result | planned evidence |
|---|---|---|---|---|---|---|---|
| RPT-001 | live query path can build retrieval ACL context | SR-RET-001 | R-RPATCH-007 | PP-RET-01 | RPC-001 | Context object built with required fields. | decision logs + test output |
| RPT-002 | missing subject context blocks safely in enforce mode | SR-RET-001 | R-RPATCH-007 | PP-RET-01 | RPC-002 | Safe deny returned, no sensitive leak. | deny response snapshot + audit log |
| RPT-003 | missing tenant context blocks safely in enforce mode | SR-RET-001 | R-RPATCH-007 | PP-RET-01 | RPC-003 | Safe deny returned and audited. | deny response + audit metric |
| RPT-004 | monitor-only records retrieval decision without blocking | SR-AUDIT-001 | R-RPATCH-003 | PP-AUDIT-01 | RPC-001 | Request succeeds, decision recorded. | monitor-only audit sample |
| RPT-005 | shadow-deny records denial without blocking | SR-AUDIT-001 | R-RPATCH-004 | PP-AUDIT-01 | RPC-001 | Request succeeds with shadow-deny record. | shadow-deny audit + metric |
| RPT-006 | enforce mode blocks cross-tenant document | SR-RET-001 | R-RPATCH-001 | PP-RET-02 | RPC-004/RPC-008 | Cross-tenant docs excluded or denied. | filtered candidate log |
| RPT-007 | enforce mode blocks unauthorized chunk | SR-RET-001 | R-RPATCH-001 | PP-RET-02 | RPC-009 | Unauthorized chunk excluded. | chunk filter evidence |
| RPT-008 | vector namespace mismatch blocked | SR-VEC-001 | R-RPATCH-001 | PP-VEC-01 | RPC-006 | Mismatch causes safe deny. | namespace deny audit |
| RPT-009 | vector metadata mismatch blocked | SR-VEC-001 | R-RPATCH-001 | PP-VEC-02 | RPC-007 | Mismatched metadata candidate excluded/denied. | metadata decision logs |
| RPT-010 | hybrid search filters unauthorized candidates | SR-RET-001 | R-RPATCH-002 | PP-RET-02 | RPC-010 | Unauthorized hybrid results removed. | pre/post hybrid candidate diff |
| RPT-011 | reranker cannot reintroduce unauthorized candidates | SR-RET-001 | R-RPATCH-004 | PP-RET-02 | RPC-011 | Output contains only authorized candidates. | rerank guard assertion log |
| RPT-012 | citation filtering removes unauthorized source | SR-PROMPT-001 | R-RPATCH-002 | PP-PROMPT-02 | RPC-012 | Unauthorized citation absent. | response citation snapshot |
| RPT-013 | context assembly excludes unauthorized chunk | SR-PROMPT-001 | R-RPATCH-002 | PP-PROMPT-01 | RPC-013 | Unauthorized chunk absent from context payload. | context payload diff |
| RPT-014 | prompt context excludes unauthorized text | SR-PROMPT-001 | R-RPATCH-002 | PP-PROMPT-01 | RPC-014 | Prompt input contains only authorized text. | prompt trace redacted sample |
| RPT-015 | cache read cannot bypass ACL | SR-CACHE-001 | R-RPATCH-008 | PP-CACHE-01 | RPC-015 | Unauthorized cached entry denied/evicted. | cache decision + eviction log |
| RPT-016 | audit event emitted from patched path | SR-AUDIT-001 | R-RPATCH-003 | PP-AUDIT-01 | RPC-016 | Audit event emitted for allow/deny. | audit event records |
| RPT-017 | finding emitted from patched path | SR-EVIDENCE-001 | R-RPATCH-004 | PP-EVIDENCE-01 | RPC-017 | Finding entry created for drift/failure. | finding record |
| RPT-018 | metric emitted from patched path | SR-AUDIT-001 | R-RPATCH-004 | PP-AUDIT-02 | RPC-017 | Metric emitted for decision outcomes. | metric export sample |
| RPT-019 | safe denial does not reveal denied document/source/chunk | SR-DENY-001 | R-RPATCH-002 | PP-DENY-01 | RPC-014 | Denial message sanitized. | denial response corpus |
| RPT-020 | feature flag disables enforcement safely | SR-CI-001 | R-RPATCH-006 | PP-CI-01 | RPC-001..RPC-017 | Enforcement off restores non-blocking behavior with observability as configured. | config snapshot + regression result |
| RPT-021 | rollback restores prior behavior | SR-CI-001 | R-RPATCH-005 | PP-CI-01 | RPC-001..RPC-017 | Rollback sequence returns baseline behavior. | rollback checklist + before/after runs |
| RPT-022 | no unrelated retrieval behavior changed | SR-EVIDENCE-001 | R-RPATCH-002 | PP-EVIDENCE-01 | RPC-001..RPC-017 | Regression suite shows no unrelated retrieval deltas. | regression report |
