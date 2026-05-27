# Safe Denial Behavior Test Plan (Step 14A)

Status: planned-only. No runtime enforcement activation.

## Planned Tests

| Test ID | Purpose | Mapped Requirement | Mapped Risk | Mapped Patch Point | Expected Result | Planned Evidence |
|---|---|---|---|---|---|---|
| T-DENY-001 | denial message does not leak tenant ID | SR-DENY-001 | R-DENY-001 | PP-DENY-01 | No tenant identifiers in user/admin payloads. | Redaction assertion output |
| T-DENY-002 | denial message does not leak document name | SR-DENY-001 | R-DENY-001 | PP-DENY-02 | Document names absent from denial outputs. | Retrieval deny transcript |
| T-DENY-003 | denial message does not leak chunk text | SR-DENY-001 | R-DENY-001 | PP-DENY-02 | Chunk content never echoed in denial. | Output diff evidence |
| T-DENY-004 | denial message does not leak tool arguments | SR-DENY-001 | R-DENY-003 | PP-DENY-02 | Tool args redacted/omitted. | Tool deny redaction log |
| T-DENY-005 | denial message does not leak tool secret | SR-DENY-001 | R-DENY-003 | PP-DENY-02 | No secret token material appears. | Secret scanner report |
| T-DENY-006 | denial message does not leak MCP server detail | SR-DENY-001 | R-DENY-003 | PP-DENY-02 | MCP endpoint/credential not exposed. | MCP deny sample |
| T-DENY-007 | denial message does not leak sandbox path | SR-DENY-001 | R-DENY-003 | PP-DENY-02 | Host/sandbox paths are removed. | Sandbox deny sample |
| T-DENY-008 | denial message does not leak prompt content | SR-DENY-001 | R-DENY-002 | PP-DENY-02 | Prompt internals absent in deny body. | Prompt deny sample |
| T-DENY-009 | denial message does not leak policy internals | SR-DENY-001 | R-DENY-002 | PP-DENY-01 | Rule internals not visible externally. | Policy deny sample |
| T-DENY-010 | user-facing message is generic | SR-DENY-001 | R-DENY-005 | PP-DENY-01 | Uses approved generic template. | Message catalog check |
| T-DENY-011 | admin-facing summary is safe but useful | SR-DENY-001 | R-DENY-004 | PP-DENY-01 | Includes category+trace only, no leaks. | Admin deny sample |
| T-DENY-012 | safe error code is returned | SR-DENY-001 | R-DENY-005 | PP-DENY-01 | Stable `SD-*` code in response. | API/error snapshot |
| T-DENY-013 | audit event is generated | SR-AUDIT-001 | R-DENY-004 | PP-AUDIT-02 | Structured denial audit event emitted. | Audit event record |
| T-DENY-014 | finding is generated where required | SR-AUDIT-001 | R-DENY-004 | PP-DENY-03 | Finding generated for configured threshold cases. | Finding sample |
| T-DENY-015 | metric is emitted | SR-DENY-001 | R-DENY-005 | PP-DENY-03 | Per-category metric increments. | Metrics snapshot |
| T-DENY-016 | approval-required message is safe | SR-APPROVAL-001 | R-DENY-002 | PP-APPROVAL-01 | Approval response has no policy internals. | Approval deny sample |
| T-DENY-017 | fail-closed message is safe | SR-DENY-001 | R-DENY-002 | PP-DENY-01 | Unavailable-engine deny is generic and safe. | Fail-closed sample |
| T-DENY-018 | monitor-only does not expose internal decision | SR-DENY-001 | R-DENY-005 | PP-DENY-03 | User output unchanged; monitor telemetry only. | Monitor-only comparison |
| T-DENY-019 | shadow-deny does not expose internal decision | SR-DENY-001 | R-DENY-005 | PP-DENY-03 | No user-visible internal decision details. | Shadow telemetry sample |
| T-DENY-020 | streaming denial terminates safely | SR-DENY-001 | R-DENY-005 | PP-DENY-02 | Stream ends with safe denial sentinel and no leak. | Stream capture |
| T-DENY-021 | artifact denial blocks unsafe release | SR-ART-001 | R-DENY-003 | PP-ART-01 | Unsafe artifact release blocked with safe message. | Artifact deny record |
| T-DENY-022 | retrieval denial does not reveal denied source | SR-RET-001 | R-DENY-001 | PP-RET-02 | Source/document identity hidden. | Retrieval deny evidence |
| T-DENY-023 | tool denial does not reveal tool secrets | SR-TOOL-001 | R-DENY-003 | PP-TOOL-02 | Secrets absent from tool denial output. | Tool deny evidence |
| T-DENY-024 | MCP denial does not reveal server credentials | SR-MCP-001 | R-DENY-003 | PP-MCP-02 | Credentials/config absent in response. | MCP deny evidence |

## Step 14B execution update (2026-05-27)
Implemented in isolated tests:
- all 14 denial categories return safe user-facing messages and safe error codes
- approval-required, validation-failed, policy-engine-unavailable, and rate/quota payload structures
- non-leakage assertions for tenant/user/document/chunk/tool/MCP/sandbox/prompt/policy/internal exception/credentials/tokens/API keys
- wrapper deny/fail-closed/approval-required safe behavior
- monitor-only and shadow-deny non-leakage behavior
