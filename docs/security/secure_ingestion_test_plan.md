# Secure Ingestion Test Plan (Step 15A)

Status: planned-only; no live ingestion enforcement enabled.

| Test ID | Purpose | Mapped Requirement | Mapped Risk | Mapped Patch Point | Expected Result | Planned Evidence |
|---|---|---|---|---|---|---|
| SITP-001 | upload without tenant denied | SR-ING-001 | R-ING-001 | PP-ING-01 | decision deny (or shadow deny), safe denial response | decision audit + denial category log |
| SITP-002 | upload without subject denied | SR-ING-001 | R-ING-001 | PP-ING-01 | deny missing subject context | stage audit and finding if repeated |
| SITP-003 | connector sync without tenant denied | SR-ING-001 | R-ING-001 | PP-ING-02 | deny connector sync start | connector sync decision event |
| SITP-004 | connector sync without owner denied | SR-ING-001 | R-ING-008 | PP-ING-02 | deny ownership validation | ownership validation event |
| SITP-005 | invalid content type denied | SR-ING-001 | R-ING-006 | PP-ING-01 | deny unsupported content type | content-type deny metric + event |
| SITP-006 | oversized file denied | SR-ING-001 | R-ING-007 | PP-ING-01 | deny oversized file | limit denial event + metric |
| SITP-007 | too many files denied | SR-ING-001 | R-ING-007 | PP-ING-01 | deny/cap exceeded file count | file-count limit evidence |
| SITP-008 | missing ACL snapshot denied | SR-ING-001 | R-ING-004 | PP-ING-02 | deny when ACL snapshot absent | acl snapshot deny audit |
| SITP-009 | stale ACL snapshot blocked | SR-ING-001 | R-ING-004 | PP-ING-02 | block/deny stale ACL state | stale ACL finding + audit |
| SITP-010 | parser failure safely denied | SR-ING-001 | R-ING-002 | PP-ING-01 | safe denial, no sensitive leak | parser failure deny record |
| SITP-011 | poisoned document flagged | SR-ING-001 | R-ING-002 | PP-ING-01 | finding created; mode-dependent decision | finding artifact + audit event |
| SITP-012 | prompt-injection document flagged | SR-ING-001 | R-ING-003 | PP-ING-01 | finding created for prompt injection indicators | finding + stage metric |
| SITP-013 | sensitive content placeholder flagged | SR-DLP-001 | R-ING-010 | PP-DLP-01 | placeholder finding recorded | DLP placeholder finding evidence |
| SITP-014 | vector write without authorization denied | SR-ING-001 | R-ING-001 | PP-ING-02 | deny vector write authorization | vector-write denied event |
| SITP-015 | cross-tenant document write denied | SR-ING-001 | R-ING-001 | PP-ING-02 | deny tenant mismatch | tenant-boundary violation evidence |
| SITP-016 | deleted document not indexed | SR-ING-001 | R-ING-009 | PP-ING-02 | block indexing/write for deleted document | deleted-doc deny audit |
| SITP-017 | duplicate document handled safely | SR-ING-001 | R-ING-009 | PP-ING-01 | dedupe or safe no-op with tracked decision | duplicate handling audit |
| SITP-018 | provenance missing denied | SR-ING-001 | R-ING-005 | PP-ING-01 | deny when provenance absent | provenance missing deny record |
| SITP-019 | source attribution missing denied | SR-ING-001 | R-ING-005 | PP-ING-01 | deny when source attribution absent | attribution deny event |
| SITP-020 | ingestion audit event created | SR-AUDIT-001 | R-ING-005 | PP-AUDIT-01 | audit event emitted for decision | structured audit sample |
| SITP-021 | ingestion finding created | SR-AUDIT-001 | R-ING-002 | PP-AUDIT-02 | finding persisted on unsafe indicator | finding persistence evidence |
| SITP-022 | metric emitted | SR-AUDIT-001 | R-ING-007 | PP-AUDIT-01 | stage/deny/finding metric incremented | metrics snapshot/log |
| SITP-023 | monitor-only ingestion records decision | SR-ING-001 | R-ING-002 | PP-ING-01 | no live block, decision recorded | monitor-only decision audit |
| SITP-024 | shadow-deny ingestion records deny without live block | SR-ING-001 | R-ING-003 | PP-ING-01 | hypothetical deny logged, path continues | shadow-deny evidence record |
| SITP-025 | enforce-mode ingestion blocks unsafe path | SR-ING-001 | R-ING-006 | PP-ING-01 | unsafe path blocked when enforcement enabled in future | enforce-mode block evidence |
| SITP-026 | safe denial does not leak document name/content/source secret | SR-ING-001 | R-ING-005 | PP-ING-01 | denial response is sanitized | redaction assertion evidence |

## Step 15B Isolated Test Execution Status (2026-05-27)
Implemented and passing in isolated tests:
SITP-001, SITP-002, SITP-003, SITP-005, SITP-006, SITP-007, SITP-008, SITP-009, SITP-011, SITP-012, SITP-014, SITP-018, SITP-020, SITP-021, SITP-022, SITP-026.
