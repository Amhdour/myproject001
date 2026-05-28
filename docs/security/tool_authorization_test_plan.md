# Tool Authorization Test Plan (Step 21A)

All tests below are planned only.

| Test ID | Purpose | Mapped Requirement | Mapped Risk | Mapped Patch Point | Expected Result | Planned Evidence | Implementation Status |
|---|---|---|---|---|---|---|---|
| TA-001 | Unknown tool denied by default | TOOL-REQ-001/005 | R-TOOL-001 | PP-TOOL-IDENTITY | deny/default-deny + finding | test case spec + traceability row | planned |
| TA-002 | Tool call without tenant denied | TOOL-REQ-004/007 | R-TOOL-003 | PP-TENANT-SCOPE | deny safe category | negative-case plan | planned |
| TA-003 | Tool call without subject denied | TOOL-REQ-004/006 | R-TOOL-002 | PP-CALLER-IDENTITY | deny safe category | negative-case plan | planned |
| TA-004 | Tool call outside workspace denied | TOOL-REQ-008 | R-TOOL-003 | PP-WORKSPACE-SCOPE | deny safe category | negative-case plan | planned |
| TA-005 | Missing required permission denied | TOOL-REQ-009 | R-TOOL-002 | PP-SUBJECT-PERM | deny safe category | negative-case plan | planned |
| TA-006 | Unauthorized group denied | TOOL-REQ-009 | R-TOOL-002 | PP-SUBJECT-PERM | deny safe category | negative-case plan | planned |
| TA-007 | Unauthorized role denied | TOOL-REQ-009 | R-TOOL-002 | PP-SUBJECT-PERM | deny safe category | negative-case plan | planned |
| TA-008 | Service account outside scope denied | TOOL-REQ-010 | R-TOOL-002 | PP-SVC-ACCOUNT-PERM | deny safe category | negative-case plan | planned |
| TA-009 | Delegated credential missing denied | TOOL-REQ-011 | R-TOOL-008 | PP-DELEGATED-CRED | deny safe category | negative-case plan | planned |
| TA-010 | Delegated credential expired denied | TOOL-REQ-011 | R-TOOL-008 | PP-DELEGATED-CRED | deny safe category | negative-case plan | planned |
| TA-011 | Delegated credential wrong tenant denied | TOOL-REQ-011 | R-TOOL-008 | PP-DELEGATED-CRED | deny safe category | negative-case plan | planned |
| TA-012 | High-risk tool requires approval | TOOL-REQ-012/015 | R-TOOL-007 | PP-APPROVAL | unapproved denied | approval gating plan | planned |
| TA-013 | Approval-required tool not executed pre-approval | TOOL-REQ-015 | R-TOOL-007 | PP-APPROVAL | no execution authorization | approval gating plan | planned |
| TA-014 | Unsafe argument path traversal denied | TOOL-REQ-014 | R-TOOL-006 | PP-ARG-CONTENT | deny/flag unsafe_argument | argument safety plan | planned |
| TA-015 | Unsafe argument command injection denied | TOOL-REQ-014 | R-TOOL-004/R-TOOL-006 | PP-ARG-CONTENT | deny/flag unsafe_argument | argument safety plan | planned |
| TA-016 | Unsafe argument SSRF URL denied | TOOL-REQ-014 | R-TOOL-005 | PP-ARG-CONTENT | deny/flag unsafe_argument | argument safety plan | planned |
| TA-017 | Unsafe argument secret value denied | TOOL-REQ-014 | R-TOOL-004 | PP-ARG-CONTENT | deny/flag unsafe_argument | argument safety plan | planned |
| TA-018 | Prompt-injection payload in args flagged | TOOL-REQ-014 | R-TOOL-010 | PP-ARG-CONTENT | finding generated | argument safety plan | planned |
| TA-019 | Tool result secret redacted / future enforce blocked | TOOL-REQ-018 | R-TOOL-009 | PP-RESULT-SAFETY | monitor redaction+flag; enforce future block | result safety plan | planned |
| TA-020 | Unauthorized document text in result flagged | TOOL-REQ-018 | R-TOOL-009 | PP-RESULT-SAFETY | finding generated | result safety plan | planned |
| TA-021 | Prompt-injection tool-abuse attempt flagged | TOOL-REQ-014/020 | R-TOOL-010 | PP-ARG-CONTENT | finding generated | abuse scenario plan | planned |
| TA-022 | Monitor-only records evidence without blocking | TOOL-REQ-016 | R-TOOL-001..010 | PP-AUTHZ-DECISION | decision logged; no live block | monitor-only evidence | planned |
| TA-023 | Shadow-deny future test remains blocked | TOOL-REQ-021 | R-TOOL-001 | PP-AUTHZ-DECISION | not enabled; documented blocked | blocked mode note | planned |
| TA-024 | Enforce-mode future test remains blocked | TOOL-REQ-022 | R-TOOL-001 | PP-AUTHZ-DECISION | not enabled; documented blocked | blocked mode note | planned |
| TA-025 | Audit event emitted | TOOL-REQ-019 | R-TOOL-002 | PP-AUDIT | audit record present | audit evidence plan | planned |
| TA-026 | Finding emitted | TOOL-REQ-020 | R-TOOL-004/R-TOOL-009 | PP-FINDINGS | finding record present | finding evidence plan | planned |
| TA-027 | Metric emitted | TOOL-REQ-023 | R-TOOL-004 | PP-AUDIT/PP-FINDINGS | expected metric increment | metric evidence plan | planned |
| TA-028 | Safe denial hides secrets/internal details | TOOL-REQ-024 | R-TOOL-009 | PP-TOOL-CALL-REQUEST | denial response non-leaking | denial evidence plan | planned |
