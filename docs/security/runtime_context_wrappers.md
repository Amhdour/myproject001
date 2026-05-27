# Runtime Context and Enforcement Wrappers Design (Step 13A)

## Purpose
Define the planned runtime context model and wrapper API surface that will eventually mediate policy decisions at mapped backend security patch points.

## Scope
Documentation/design/test-planning only. No runtime path wiring, no backend API enforcement activation, and no application behavior changes.

## Status
planned

## Owner
AI Trust & Security Readiness Engineer

## Non-Claim Statement
This document does not claim production readiness, operational effectiveness, or active enforcement. Wrapper behavior is design-only.

## Relationship to Isolated Policy Engine
Wrappers are planned callers of the isolated policy engine (`models.py`, `loader.py`, `validator.py`, `evaluator.py`) once future integration is authorized.

## Relationship to Patch Points
Each context/wrapper maps to previously documented patch points in `docs/security/patch_points.md`; no patch point is implemented in this step.

## Context Propagation Model
1. Build `RequestContext` at entry boundary.
2. Derive `SubjectContext`, `TenantContext`, `SessionContext`.
3. Compose operation-specific context (ingestion/retrieval/vector/etc.).
4. Build `SecurityDecisionContext` with mode (`monitor_only`, `shadow_deny`, `enforce`).
5. Call wrapper -> policy evaluator input.
6. Persist decision side-effects (audit/finding/metric) per mode.

## Enforcement Expectations
- **Fail-closed:** Missing required context or policy engine unavailability yields deny/safe-fail.
- **Monitor-only:** Decision evaluated and logged, execution allowed, finding optionally informational.
- **Shadow-deny:** Execution allowed but deny counterfactual recorded.
- **Enforce-mode:** Policy deny blocks action using safe denial output.
- **Audit:** Every wrapper decision emits an audit event with correlation IDs.
- **Finding:** Violations and policy failures emit standardized findings.
- **Metric:** Decision counters/timers emitted with mode + wrapper labels.
- **Denial behavior:** Denials must avoid leaking sensitive policy internals or resource secrets.

## Test Strategy
Use isolated wrapper tests only (no runtime integration): context construction, allow/deny paths, mode behavior, fail-closed behavior, and side-effect emission.

## Evidence Requirements
- Prerequisite verification log.
- Context model summary.
- Wrapper inventory.
- Wrapper test-plan summary.
- Wrapper traceability summary.
- Remote limitation record when applicable.

## Known Limitations
- Design only; wrappers are not implemented or wired.
- Enforcement is inactive.
- Behavior in production/runtime paths remains unchanged.

## Planned Runtime Context Models
Implementation status for all below: **planned**.

| Context | Purpose | Required fields | Mapped patch points | Mapped requirements | Mapped risks | Expected policy input | Expected policy decision output | Audit event needed | Planned tests |
|---|---|---|---|---|---|---|---|---|---|
| RequestContext | Canonical request metadata | request_id, trace_id, timestamp, route, method | PP-RET-01, PP-TOOL-01, PP-MCP-01 | SR-AUDIT-001 | R-WRAP-004 | request envelope | allow/deny + rationale code | security.decision.request | TC-RW-001 |
| SubjectContext | Caller identity/principal | subject_id, subject_type, roles, authn_level | PP-RET-01, PP-ADMIN-01 | SR-RET-001, SR-ADMIN-001 | R-WRAP-001 | subject attributes | allow/deny/approval_required | security.decision.subject | TC-RW-002, TC-RW-005 |
| TenantContext | Tenant isolation metadata | tenant_id, tenant_slug, partition_key | PP-RET-01, PP-VEC-01, PP-CACHE-01 | SR-RET-001, SR-VEC-001, SR-CACHE-001 | R-WRAP-001 | tenant constraints | allow/deny | security.decision.tenant | TC-RW-003, TC-RW-004 |
| SessionContext | Session continuity and trust | session_id, auth_method, session_age, mfa_state | PP-APPROVAL-01 | SR-APPROVAL-001 | R-WRAP-002 | session posture | allow/deny/approval_required | security.decision.session | TC-RW-016 |
| IngestionContext | Ingestion authorization scope | connector_id, source_type, dataset_id, action | PP-ING-01, PP-ING-02 | SR-ING-001 | R-WRAP-005 | ingestion action + resource | allow/deny | security.decision.ingestion | TC-RW-024 |
| RetrievalContext | Retrieval authorization scope | query_id, corpora, acl_tags, retrieval_mode | PP-RET-01, PP-RET-02 | SR-RET-001 | R-WRAP-005 | retrieval operation | allow/deny | security.decision.retrieval | TC-RW-006, TC-RW-007 |
| VectorContext | Vector query constraints | namespace, metadata_filters, top_k | PP-VEC-01, PP-VEC-02 | SR-VEC-001 | R-WRAP-005 | vector query envelope | allow/deny | security.decision.vector | TC-RW-008 |
| CacheContext | Cache ACL and tenancy scope | cache_key_class, tenant_id, acl_version, operation | PP-CACHE-01 | SR-CACHE-001 | R-WRAP-005 | cache op attributes | allow/deny | security.decision.cache | TC-RW-009 |
| ToolContext | Tool authorization context | tool_name, tool_args_hash, risk_level, capability | PP-TOOL-01, PP-TOOL-02 | SR-TOOL-001, SR-APPROVAL-001 | R-WRAP-005 | tool invocation summary | allow/deny/approval_required | security.decision.tool | TC-RW-010 |
| MCPContext | MCP capability-bound context | mcp_server, action, delegated_cred_scope | PP-MCP-01, PP-MCP-02 | SR-MCP-001 | R-WRAP-005 | mcp action context | allow/deny | security.decision.mcp | TC-RW-011 |
| ArtifactContext | Artifact release safety context | artifact_type, sensitivity, destination, redaction_state | PP-ART-01, PP-DLP-01 | SR-ART-001, SR-DLP-001 | R-WRAP-003 | artifact classification | allow/deny/redact_required | security.decision.artifact | TC-RW-012 |
| SandboxContext | Sandbox execution policy context | runtime, command_class, network_intent, fs_scope | PP-SBX-01, PP-SBX-02 | SR-SBX-001 | R-WRAP-005 | execution intent | allow/deny/approval_required | security.decision.sandbox | TC-RW-013 |
| ApprovalContext | Human approval state | approval_required, approver_role, ticket_id, expiry | PP-APPROVAL-01 | SR-APPROVAL-001 | R-WRAP-002 | approval evidence | proceed/block | security.decision.approval | TC-RW-016 |
| ModelContext | Model/provider routing context | provider, model, region, data_classification | PP-MODEL-01 | SR-MODEL-001 | R-WRAP-005 | model call envelope | allow/deny | security.decision.model | TC-RW-014 |
| PromptContext | Prompt governance context | template_id, includes_untrusted_content, guardrails | PP-PROMPT-01, PP-PROMPT-02 | SR-PROMPT-001 | R-WRAP-003 | prompt metadata | allow/deny/transform_required | security.decision.prompt | TC-RW-015 |
| SecurityDecisionContext | Unified decision metadata | mode, policy_version, decision_id, decision_time | PP-AUDIT-01, PP-EVIDENCE-01 | SR-AUDIT-001, SR-EVIDENCE-001 | R-WRAP-004 | decision frame | serialized decision record | security.decision.finalized | TC-RW-017, TC-RW-018, TC-RW-019 |

## Planned Wrapper Functions
Implementation status for all below: **planned**.

| Wrapper | Purpose | Required fields | Mapped patch points | Mapped requirements | Mapped risks | Expected policy input | Expected policy decision output | Audit event needed | Planned tests |
|---|---|---|---|---|---|---|---|---|---|
| authorize_ingestion() | Gate ingestion action | RequestContext, SubjectContext, TenantContext, IngestionContext | PP-ING-01, PP-ING-02 | SR-ING-001 | R-WRAP-005 | ingestion decision input | allow/deny | security.wrapper.ingestion | TC-RW-024 |
| authorize_retrieval() | Gate retrieval execution | RequestContext, SubjectContext, TenantContext, RetrievalContext | PP-RET-01, PP-RET-02 | SR-RET-001 | R-WRAP-001, R-WRAP-005 | retrieval decision input | allow/deny | security.wrapper.retrieval | TC-RW-006, TC-RW-007 |
| authorize_vector_query() | Gate vector access | RequestContext, TenantContext, VectorContext | PP-VEC-01, PP-VEC-02 | SR-VEC-001 | R-WRAP-005 | vector decision input | allow/deny | security.wrapper.vector | TC-RW-008 |
| authorize_cache_access() | Gate cache read/write | RequestContext, TenantContext, CacheContext | PP-CACHE-01 | SR-CACHE-001 | R-WRAP-005 | cache decision input | allow/deny | security.wrapper.cache | TC-RW-009 |
| authorize_tool_call() | Gate tool invocation | RequestContext, SubjectContext, ToolContext, ApprovalContext | PP-TOOL-01, PP-TOOL-02, PP-APPROVAL-01 | SR-TOOL-001, SR-APPROVAL-001 | R-WRAP-005 | tool decision input | allow/deny/approval_required | security.wrapper.tool | TC-RW-010 |
| authorize_mcp_action() | Gate MCP delegated actions | RequestContext, SubjectContext, MCPContext | PP-MCP-01, PP-MCP-02 | SR-MCP-001 | R-WRAP-005 | mcp decision input | allow/deny | security.wrapper.mcp | TC-RW-011 |
| authorize_artifact_release() | Gate artifact output | RequestContext, SubjectContext, ArtifactContext | PP-ART-01, PP-DLP-01 | SR-ART-001, SR-DLP-001 | R-WRAP-003 | artifact decision input | allow/deny/redact_required | security.wrapper.artifact | TC-RW-012 |
| authorize_sandbox_execution() | Gate sandbox execution | RequestContext, SubjectContext, SandboxContext, ApprovalContext | PP-SBX-01, PP-SBX-02, PP-APPROVAL-01 | SR-SBX-001, SR-APPROVAL-001 | R-WRAP-002, R-WRAP-005 | sandbox decision input | allow/deny/approval_required | security.wrapper.sandbox | TC-RW-013 |
| authorize_model_call() | Gate model/provider use | RequestContext, TenantContext, ModelContext | PP-MODEL-01 | SR-MODEL-001 | R-WRAP-005 | model decision input | allow/deny | security.wrapper.model | TC-RW-014 |
| authorize_prompt_use() | Gate prompt template/use | RequestContext, SubjectContext, PromptContext | PP-PROMPT-01, PP-PROMPT-02 | SR-PROMPT-001 | R-WRAP-003 | prompt decision input | allow/deny/transform_required | security.wrapper.prompt | TC-RW-015 |
| require_human_approval() | Enforce approval precondition | ApprovalContext, SecurityDecisionContext | PP-APPROVAL-01 | SR-APPROVAL-001 | R-WRAP-002 | approval state | proceed/block | security.wrapper.approval | TC-RW-016 |
| write_audit_event() | Persist decision audit | SecurityDecisionContext + operation context | PP-AUDIT-01, PP-AUDIT-02 | SR-AUDIT-001 | R-WRAP-004 | normalized audit payload | stored event | security.wrapper.audit | TC-RW-017 |
| raise_security_denial() | Raise safe denial surface | SecurityDecisionContext + denial code | PP-RET-01, PP-TOOL-01 | SR-RET-001, SR-TOOL-001 | R-WRAP-003 | deny decision | safe error/exception | security.wrapper.denial | TC-RW-020 |
| record_finding() | Record violation/failure finding | SecurityDecisionContext + finding severity | PP-EVIDENCE-01 | SR-EVIDENCE-001 | R-WRAP-004 | finding payload | finding emitted | security.wrapper.finding | TC-RW-018 |
| emit_security_metric() | Emit security telemetry | SecurityDecisionContext + metric labels | PP-EVIDENCE-01, PP-CI-01 | SR-EVIDENCE-001, SR-CI-001 | R-WRAP-004 | metric event | metric emitted | security.wrapper.metric | TC-RW-019 |

## Step 13B Implementation Note (Minimal)
- Minimal isolated context/wrapper skeletons implemented under `backend/security_layer/runtime/`.
- No runtime integration yet.
- In-memory audit/finding/metric helpers are test-only.
- Enforcement is not active in application paths.

## Step 13C Validation Note (2026-05-27)
- Runtime wrappers validated in isolated scope only.
- Verified wrappers remain unbound from backend runtime request paths.
- Verified no web/deployment runtime references were introduced.
- Added coverage updates for wrapper function inventory and safe denial redaction checks.
- Runtime enforcement remains inactive.
