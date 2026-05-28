# Tool Authorization Design (Step 21A)

## Purpose
Define a planned, non-live design for policy-driven authorization of tool calls with safe denial, audit, findings, and metrics.

## Scope
Design/specification only. No runtime wiring, no live blocking, no enforce enablement.

## Status
Planned / design.

## Owner
Security Architecture + Platform Runtime teams.

## Non-claim Statement
This document does not claim live enforcement exists. It is a forward design artifact only.

## Relationships
- **Policy engine**: consumes policy decisions and registry metadata contracts.
- **Runtime wrappers**: future integration point for monitor-only decision capture.
- **Safe denial behavior**: denial category and non-leakage response model.
- **Retrieval/vector/cache controls**: aligned patterns only; no shared live execution path yet.

## Design Models
- Threat model: unknown-tool execution, identity bypass, cross-tenant misuse, argument/result abuse, prompt-induced abuse.
- Trust boundaries: caller -> orchestration -> policy/registry -> tool adapter -> result processing.
- Tool identity model: `tool_id` + versioned metadata + status.
- Tool registry model: signed/validated metadata contract with default-deny semantics.
- Caller identity model: subject type (user/service account), tenant/workspace, groups/roles/permissions.
- Tenant/workspace scope model: explicit scope binding required before authorization.
- User/group/role model: union of explicit grants, denied when missing.
- Service-account model: explicit allowlist and scope constraints.
- Delegated credential model: required for selected tools, must match tenant/scope and validity window.
- Tool category model: read/query/write/admin/integration/exec classes.
- Tool risk-tier model: low/medium/high/critical with approval gates.
- Tool argument safety model: schema + content checks (path traversal, SSRF, injection, secret leakage).
- Tool result safety model: redaction/flagging policy before downstream exposure.
- Approval model: high-risk tools may require pre-execution approval token.
- Audit/finding/metric model: stage-level events and violations.
- Rollout model: monitor-only active design target; shadow-deny/enforce remain blocked.

## Behavioral Expectations (Planned)
- Default-deny behavior: deny when registry/policy/context incomplete.
- Unknown-tool behavior: deny + finding.
- Unsafe-argument behavior: deny (future enforce), record finding in monitor-only.
- High-risk approval behavior: unauthorized until valid approval artifact.
- Credential-isolation behavior: delegated creds scoped per tenant/workspace/tool.
- Prompt-injection tool-abuse handling: classify and flag injection indicators in request and argument provenance.
- Tool result redaction model: redact obvious secrets; flag restricted text leakage.

## Stage Inventory
All stages below are **implementation status: planned**.

| Stage ID | Purpose | Mapped Risks | Mapped Requirements | Mapped Patch Points | Required Context Fields | Planned Policy Check | Safe Denial Category | Audit Event | Finding Condition | Metric | Planned Tests | Implementation Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tool_registry_loaded | Load registry | R-TOOL-001 | TOOL-REQ-001 | PP-TOOL-REG-LOAD | registry_source | registry present | configuration_missing | tool.registry.loaded | load failure | tool_registry_load_fail_count | TA-001 | planned |
| tool_registry_validated | Validate schema/signature | R-TOOL-001 | TOOL-REQ-002 | PP-TOOL-REG-VALIDATE | registry_entries | schema valid | configuration_invalid | tool.registry.validated | invalid field/signature | tool_registry_invalid_count | TA-001 | planned |
| tool_call_requested | capture call intent | R-TOOL-010 | TOOL-REQ-003 | PP-TOOL-CALL-REQUEST | tool_name,args,caller | request shape sanity | invalid_request | tool.call.requested | malformed request | tool_call_requested_count | TA-022 | planned |
| tool_context_validated | require minimum context | R-TOOL-002,R-TOOL-003 | TOOL-REQ-004 | PP-TOOL-CONTEXT | tenant_id,workspace_id,subject_id | context completeness | context_missing | tool.context.validated | missing required context | tool_context_missing_count | TA-002,TA-003 | planned |
| tool_identity_resolved | resolve canonical tool | R-TOOL-001 | TOOL-REQ-005 | PP-TOOL-IDENTITY | tool_name,tool_version | tool exists and active | unknown_tool | tool.identity.resolved | unknown/deprecated tool | tool_unknown_count | TA-001 | planned |
| caller_identity_resolved | resolve caller principal | R-TOOL-002 | TOOL-REQ-006 | PP-CALLER-IDENTITY | subject_type,subject_id | principal resolvable | subject_unavailable | tool.caller.resolved | unresolved caller | tool_subject_unresolved_count | TA-003 | planned |
| tenant_scope_validated | enforce tenant boundary | R-TOOL-003 | TOOL-REQ-007 | PP-TENANT-SCOPE | tenant_id,allowed_tenant_scope | tenant in scope | tenant_scope_denied | tool.tenant.validated | tenant mismatch | tool_tenant_denied_count | TA-002,TA-010 | planned |
| workspace_scope_validated | enforce workspace boundary | R-TOOL-003 | TOOL-REQ-008 | PP-WORKSPACE-SCOPE | workspace_id,allowed_workspace_scope | workspace in scope | workspace_scope_denied | tool.workspace.validated | workspace mismatch | tool_workspace_denied_count | TA-004 | planned |
| subject_permission_validated | validate user/group/role | R-TOOL-002 | TOOL-REQ-009 | PP-SUBJECT-PERM | permissions,groups,roles,required_* | required grants present | permission_denied | tool.subject.permission.validated | missing user/group/role grant | tool_permission_denied_count | TA-005,TA-006,TA-007 | planned |
| service_account_permission_validated | validate service account use | R-TOOL-002 | TOOL-REQ-010 | PP-SVC-ACCOUNT-PERM | subject_type,service_account_allowed | service acct policy compliance | service_account_denied | tool.service_account.validated | service account out of scope | tool_service_account_denied_count | TA-008 | planned |
| delegated_credential_validated | validate delegated creds | R-TOOL-008 | TOOL-REQ-011 | PP-DELEGATED-CRED | delegated_credential,scope,expiry | credential required/valid/scope match | delegated_credential_denied | tool.delegated_credential.validated | missing/expired/wrong-tenant cred | tool_delegated_credential_denied_count | TA-009,TA-010,TA-011 | planned |
| tool_risk_classified | classify risk tier | R-TOOL-007 | TOOL-REQ-012 | PP-TOOL-RISK | tool_risk_tier | tier in allowed enum | risk_classification_invalid | tool.risk.classified | unknown risk tier | tool_risk_unknown_count | TA-012 | planned |
| tool_argument_schema_validated | schema validation | R-TOOL-004 | TOOL-REQ-013 | PP-ARG-SCHEMA | args,argument_schema_id | strict schema pass | argument_schema_denied | tool.argument_schema.validated | schema mismatch | tool_arg_schema_denied_count | TA-014 | planned |
| tool_argument_content_validated | content safety checks | R-TOOL-004,R-TOOL-005,R-TOOL-006,R-TOOL-010 | TOOL-REQ-014 | PP-ARG-CONTENT | args,source_prompt | unsafe token/path/url/injection detection | unsafe_argument | tool.argument_content.validated | traversal/SSRF/injection/secret/injection markers | tool_arg_content_flag_count | TA-014..TA-018,TA-021 | planned |
| approval_requirement_evaluated | apply approval gating | R-TOOL-007 | TOOL-REQ-015 | PP-APPROVAL | approval_required,approval_token | approval token required/valid | approval_missing | tool.approval.evaluated | required approval absent/invalid | tool_approval_missing_count | TA-012,TA-013 | planned |
| tool_execution_authorized | final authorization decision | R-TOOL-001..R-TOOL-010 | TOOL-REQ-016 | PP-AUTHZ-DECISION | prior stage outcomes | all required checks passed | authorization_denied | tool.execution.authorized | any mandatory check fail | tool_authorization_denied_count | TA-022 | planned |
| tool_result_received | capture result envelope | R-TOOL-009 | TOOL-REQ-017 | PP-RESULT-INGEST | result_payload | result envelope parseable | result_unavailable | tool.result.received | missing/unreadable result | tool_result_receive_fail_count | TA-019 | planned |
| tool_result_safety_validated | validate/redact result | R-TOOL-009 | TOOL-REQ-018 | PP-RESULT-SAFETY | result_payload,result_policy | secret/restricted-content policy checks | unsafe_result | tool.result_safety.validated | secret or restricted text hit | tool_result_safety_flag_count | TA-019,TA-020 | planned |
| tool_audit_written | emit audit record | R-TOOL-002 | TOOL-REQ-019 | PP-AUDIT | decision metadata | audit required by policy | audit_write_failed | tool.audit.written | audit write failure | tool_audit_write_fail_count | TA-025 | planned |
| tool_finding_recorded_if_needed | emit findings | R-TOOL-004,R-TOOL-009,R-TOOL-010 | TOOL-REQ-020 | PP-FINDINGS | violation metadata | finding policy on violation | finding_write_failed | tool.finding.recorded | required finding missing | tool_finding_record_fail_count | TA-026,TA-027 | planned |

## Test Strategy
See `docs/security/tool_authorization_test_plan.md`.

## Evidence Requirements
Store prerequisite checks, stage inventory, contract summaries, argument rules summary, test-plan summary, and traceability summary under `docs/security/evidence/tool_authorization_design/`.

## Known Limitations
Design-only; no live enforcement/wiring; no shadow-deny or enforce activation.

## Step 21B Implementation Note (2026-05-28)
- Minimal isolated tool authorization controls implemented under `backend/security_layer/tools/`.
- No live tool/agent/MCP integration.
- No production enforcement active.
