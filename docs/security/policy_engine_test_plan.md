# Policy Engine Test Plan (Step 12A)

Status: planned only.

| Test ID | Purpose | Mapped Requirement | Mapped Risk | Mapped Policy File | Expected Result | Planned Evidence |
|---|---|---|---|---|---|---|
| PE-T-001 | valid policy loads | SR-POL-001 | R-PE-001 | docs/security/policies/default_deny_policy.yaml | Loader accepts valid policy bundle. | test report + loader logs |
| PE-T-002 | invalid policy rejected | SR-POL-001 | R-PE-001 | docs/security/policies/default_deny_policy.yaml | Validator rejects invalid schema. | validation error artifact |
| PE-T-003 | missing policy rejected | SR-POL-001 | R-PE-001 | docs/security/policies/default_deny_policy.yaml | Missing file causes fail-closed startup failure. | startup failure log |
| PE-T-004 | malformed rule rejected | SR-POL-001 | R-PE-001 | docs/security/policies/default_deny_policy.yaml | Rule parse error rejected before activation. | validator output |
| PE-T-005 | unknown effect rejected | SR-POL-001 | R-PE-001 | docs/security/policies/default_deny_policy.yaml | Unknown effect is rejected. | validator output |
| PE-T-006 | unknown scope rejected | SR-POL-001 | R-PE-001 | docs/security/policies/default_deny_policy.yaml | Unknown scope is rejected. | validator output |
| PE-T-007 | missing required context rejected | SR-POL-001 | R-PE-002 | docs/security/policies/default_deny_policy.yaml | Decision returns deny with missing-context reason. | decision log |
| PE-T-008 | default-deny behavior | SR-POL-001 | R-PE-002 | docs/security/policies/default_deny_policy.yaml | No match results in explicit deny. | decision evidence |
| PE-T-009 | allow decision | SR-POL-001 | R-PE-002 | docs/security/policies/default_deny_policy.yaml | Matched allow returns allow. | decision evidence |
| PE-T-010 | deny decision | SR-POL-001 | R-PE-002 | docs/security/policies/default_deny_policy.yaml | Matched deny returns deny. | decision evidence |
| PE-T-011 | approval-required decision | SR-APPROVAL-001 | R-PE-002 | docs/security/policies/approvals_policy.yaml | Matched rule returns approval_required with metadata. | decision evidence |
| PE-T-012 | monitor-only mode | SR-AUDIT-001 | R-PE-004 | docs/security/policies/default_deny_policy.yaml | Decision tagged monitor_only and audited. | audit sample |
| PE-T-013 | shadow-deny mode | SR-AUDIT-001 | R-PE-005 | docs/security/policies/default_deny_policy.yaml | Decision comparison output includes projected deny. | comparison artifact |
| PE-T-014 | enforce mode | SR-POL-001 | R-PE-003 | docs/security/policies/default_deny_policy.yaml | Engine marks decision authoritative for enforcement path. | mode run report |
| PE-T-015 | policy version recorded | SR-AUDIT-001 | R-PE-004 | docs/security/policies/default_deny_policy.yaml | Audit event includes policy version. | audit sample |
| PE-T-016 | policy hash recorded | SR-AUDIT-001 | R-PE-005 | docs/security/policies/default_deny_policy.yaml | Audit event includes policy hash. | audit sample |
| PE-T-017 | explainable decision generated | SR-AUDIT-001 | R-PE-004 | docs/security/policies/default_deny_policy.yaml | Explanation payload emitted for every decision. | explanation artifact |
| PE-T-018 | startup validation failure | SR-POL-001 | R-PE-003 | docs/security/policies/default_deny_policy.yaml | Invalid startup policy blocks activation. | startup failure evidence |
| PE-T-019 | fail-closed behavior | SR-POL-001 | R-PE-003 | docs/security/policies/default_deny_policy.yaml | Engine internal failure results in deny. | failure-mode evidence |
| PE-T-020 | policy comparison result | SR-POL-001 | R-PE-005 | docs/security/policies/default_deny_policy.yaml | Version comparison emits drift summary. | comparison report |
| PE-T-021 | regression replay compatibility | SR-CI-001 | R-PE-005 | docs/security/policies/default_deny_policy.yaml | Historical context replay completes with diff report. | replay report |

## Step 12B Test Implementation Status (2026-05-27)

Implemented in `backend/security_layer/tests`:
- valid policy object
- invalid missing required fields
- unknown effect rejected
- unknown scope rejected
- default deny behavior
- allow decision
- deny decision
- deny precedence over allow
- approval-required decision
- explainable decision output
- policy hash generated
- unsupported file extension rejected
