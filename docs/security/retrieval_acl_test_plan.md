# Retrieval ACL Test Plan (Step 16A)

Status: planned/design-only

| Test ID | Purpose | Mapped Requirement | Mapped Risk | Mapped Patch Point | Expected Result | Planned Evidence |
|---|---|---|---|---|---|---|
| RET-ACL-T001 | Query without tenant denied | SR-RET-001 | R-RET-001 | PP-RET-01 | Deny decision for missing tenant context | deny audit sample + metric snapshot |
| RET-ACL-T002 | Query without subject denied | SR-RET-001 | R-RET-001 | PP-RET-01 | Deny decision for missing subject context | deny audit sample + metric snapshot |
| RET-ACL-T003 | Cross-tenant document denied | SR-RET-001 | R-RET-001 | PP-RET-02 | Unauthorized cross-tenant document removed/denied | candidate filter log + deny audit |
| RET-ACL-T004 | Cross-tenant chunk denied | SR-RET-001 | R-RET-002 | PP-RET-02 | Unauthorized cross-tenant chunk excluded | chunk filter trace + deny audit |
| RET-ACL-T005 | Unauthorized group denied | SR-RET-001 | R-RET-001 | PP-RET-01 | Group-not-allowed subject denied | decision trace + deny event |
| RET-ACL-T006 | Unauthorized role denied | SR-RET-001 | R-RET-001 | PP-RET-01 | Role-not-allowed subject denied | decision trace + deny event |
| RET-ACL-T007 | Stale ACL snapshot denied | SR-RET-001 | R-RET-004 | PP-RET-02 | Stale snapshot request denied and finding eligible | deny event + finding record |
| RET-ACL-T008 | Deleted document denied | SR-RET-001 | R-RET-005 | PP-RET-02 | Deleted/tombstoned doc never returned | filter trace + deny audit |
| RET-ACL-T009 | Vector namespace mismatch denied | SR-VEC-001 | R-RET-003 | PP-VEC-01 | Namespace mismatch denied | vector check audit + metric |
| RET-ACL-T010 | Vector metadata mismatch denied | SR-VEC-001 | R-RET-003 | PP-VEC-02 | Missing/mismatched metadata filter denied | vector metadata audit + metric |
| RET-ACL-T011 | Hybrid search filters unauthorized candidates | SR-RET-001 | R-RET-002 | PP-RET-02 | Unauthorized candidates dropped after merge | hybrid filter trace |
| RET-ACL-T012 | Reranker cannot reintroduce unauthorized candidates | SR-RET-001 | R-RET-006 | PP-RET-02 | Any reintroduced denied ID removed and finding raised | rerank comparison log + finding |
| RET-ACL-T013 | Citation source filtered when unauthorized | SR-RET-001 | R-RET-007 | PP-RET-02 | Unauthorized citation/source suppressed | citation filter audit |
| RET-ACL-T014 | Context assembly excludes unauthorized chunks | SR-RET-001 | R-RET-002 | PP-RET-02 | Final context chunk set contains only authorized chunks | context assembly trace |
| RET-ACL-T015 | Prompt context excludes unauthorized text | SR-PROMPT-001 | R-RET-010 | PP-PROMPT-01 | Prompt payload contains only authorized text lineage | prompt context trace |
| RET-ACL-T016 | Cache read denied without matching ACL context | SR-CACHE-001 | R-RET-008 | PP-CACHE-01 | Cache read denied on ACL fingerprint mismatch | cache deny audit + metric |
| RET-ACL-T017 | Cache hit does not bypass ACL | SR-CACHE-001 | R-RET-008 | PP-CACHE-01 | Cached response still ACL-validated | cache hit validation trace |
| RET-ACL-T018 | Connector permission drift detected | SR-RET-001 | R-RET-009 | PP-RET-02 | Drift signal emits finding/audit | drift detection finding + audit |
| RET-ACL-T019 | Monitor-only retrieval records decision | SR-AUDIT-001 | R-008 | PP-AUDIT-01 | Decision recorded, no live blocking | monitor mode audit event |
| RET-ACL-T020 | Shadow-deny retrieval records deny without live block | SR-AUDIT-001 | R-008 | PP-AUDIT-01 | Shadow deny decision recorded, request not blocked | shadow mode delta log |
| RET-ACL-T021 | Enforce-mode retrieval blocks unsafe path | SR-RET-001 | R-RET-001 | PP-RET-02 | Unsafe path blocked when enforce mode enabled | enforce-mode deny record |
| RET-ACL-T022 | Retrieval audit event created | SR-AUDIT-001 | R-008 | PP-AUDIT-01 | Structured retrieval ACL event emitted | audit payload sample |
| RET-ACL-T023 | Retrieval finding created | SR-AUDIT-001 | R-RET-004 | PP-AUDIT-02 | Finding recorded when threshold/condition met | finding record sample |
| RET-ACL-T024 | Retrieval metric emitted | SR-AUDIT-001 | R-RET-009 | PP-AUDIT-02 | Stage metric increments for decision path | metric export snapshot |
| RET-ACL-T025 | Safe denial does not reveal denied document/source/chunk | SR-RET-001 | R-RET-007 | PP-RET-02 | Deny response redacts sensitive identifiers | response sample + safe-denial checklist |
