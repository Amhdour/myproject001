# MCP Hardening Design (Step 22A)

## Purpose
Define planned MCP hardening controls and traceability without changing runtime behavior.

## Scope
Design, documentation, and planned testing only. No live MCP enforcement, filtering, or blocking is enabled.

## Status
planned/design

## Owner
AI Trust & Security Readiness Engineer

## Non-Claim Statement
This document does not claim implementation, effectiveness, compliance, or production readiness.

## Relationships
- Tool authorization: extends existing tool policy concepts to MCP-specific identities and scopes.
- Runtime wrappers: planned MCP checks would eventually execute through isolated wrapper patterns.
- Policy engine: all stage decisions are planned as policy-evaluated outcomes.
- Safe denial behavior: all denials map to existing safe-denial categories and sanitized messages.

## Models
- MCP threat model: unknown server/tool/resource/prompt, cross-tenant access, credential abuse, prompt injection, response exfiltration.
- MCP trust boundaries: caller, MCP client, MCP server, external egress, credential stores, tenant/workspace boundaries.
- MCP server identity model: stable `mcp_server_id` + status + trust tier.
- MCP client identity model: calling runtime identity bound to tenant/workspace/subject.
- MCP tool identity model: `mcp_tool_id` and risk tier per server.
- MCP resource identity model: `mcp_resource_id` and ACL policy binding.
- MCP prompt identity model: `mcp_prompt_id` with isolation policy.
- MCP credential identity model: credential handle ids only; no raw secrets in control planes.
- Tenant/workspace scope model: explicit allowlists for tenant/workspace; default deny outside scope.
- User/group/role permission model: required permission sets must match request subject.
- Service-account permission model: service accounts must be explicitly allowed per registry entry.
- Delegated credential model: delegated credential must exist, be scoped, tenant-matching, and unexpired.
- MCP server/tool/resource/prompt registry models: schema-driven registry records, validated before use.
- MCP risk-tier model: low/medium/high/critical tiers drive approvals and evidence depth.
- MCP request safety model: schema validation + argument safety + identity/scope checks.
- MCP response safety model: secret/restricted-data detection and finding emission.
- MCP resource ACL model: resource access requires ACL policy pass.
- MCP prompt isolation model: prompt IDs and isolation policy prevent cross-context leakage.
- Confused-deputy prevention model: caller identity, target identity, and delegated scope binding required.
- Credential isolation model: tenant/user/service/delegated boundaries enforced by policy.
- Outbound egress control model: egress policy IDs constrain destination domains/networks.
- Replay protection model: nonce/timestamp/request-id expectations and duplicate detection.
- Request signing model: required signatures for designated risk tiers.
- Approval requirement model: high-risk actions require approval prior to execute.
- Audit/finding/metric model: each stage emits mapped telemetry events.
- Rollout model: monitor-only planned first; shadow-deny/enforce documented but blocked.

## Behavior Rules (Planned)
- Default-deny behavior: unknown or untrusted MCP entities are denied by default.
- Unknown MCP server/tool/resource/prompt behavior: deny and audit/finding/metric.
- Unsafe MCP argument behavior: deny in future enforce; monitor-only flag in design phase.
- Unsafe MCP response behavior: flag findings and sanitize output channels.
- High-risk MCP approval behavior: must not execute before approval.
- Prompt-injection MCP-abuse handling: detect/flag payload indicators and bind to approval/risk tier.
- MCP disable/rollback model: feature-flag disable with fail-open monitor-only fallback until enforce explicitly authorized.

## Test Strategy
See `docs/security/mcp_hardening_test_plan.md` for planned deny/flag/approval/audit tests.

## Evidence Requirements
Stage inventory, registry contract summary, request/credential/egress summaries, test-plan summary, traceability summary, and remote-sync limitation note where applicable.

## Known Limitations
Design-only; no live enforcement, registry runtime, credential isolation runtime, egress runtime, signing/replay runtime, shadow-deny, or enforce activation.

## MCP Hardening Stages (Planned)
### 1. `mcp_registry_loaded`
- **Stage ID:** mcp_registry_loaded
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_registry_loaded`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_registry_loaded.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 2. `mcp_registry_validated`
- **Stage ID:** mcp_registry_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_registry_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_registry_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 3. `mcp_request_received`
- **Stage ID:** mcp_request_received
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_request_received`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_request_received.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 4. `mcp_context_validated`
- **Stage ID:** mcp_context_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_context_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_context_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 5. `mcp_server_identity_resolved`
- **Stage ID:** mcp_server_identity_resolved
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_server_identity_resolved`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_server_identity_resolved.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 6. `mcp_client_identity_resolved`
- **Stage ID:** mcp_client_identity_resolved
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_client_identity_resolved`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_client_identity_resolved.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 7. `mcp_tool_identity_resolved`
- **Stage ID:** mcp_tool_identity_resolved
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_tool_identity_resolved`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_tool_identity_resolved.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 8. `mcp_resource_identity_resolved`
- **Stage ID:** mcp_resource_identity_resolved
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_resource_identity_resolved`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_resource_identity_resolved.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 9. `mcp_prompt_identity_resolved`
- **Stage ID:** mcp_prompt_identity_resolved
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_prompt_identity_resolved`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_prompt_identity_resolved.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 10. `mcp_tenant_scope_validated`
- **Stage ID:** mcp_tenant_scope_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_tenant_scope_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_tenant_scope_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 11. `mcp_workspace_scope_validated`
- **Stage ID:** mcp_workspace_scope_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_workspace_scope_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_workspace_scope_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 12. `mcp_subject_permission_validated`
- **Stage ID:** mcp_subject_permission_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_subject_permission_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_subject_permission_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 13. `mcp_service_account_permission_validated`
- **Stage ID:** mcp_service_account_permission_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_service_account_permission_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_service_account_permission_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 14. `mcp_delegated_credential_validated`
- **Stage ID:** mcp_delegated_credential_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_delegated_credential_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_delegated_credential_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 15. `mcp_resource_acl_validated`
- **Stage ID:** mcp_resource_acl_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_resource_acl_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_resource_acl_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 16. `mcp_prompt_isolation_validated`
- **Stage ID:** mcp_prompt_isolation_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_prompt_isolation_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_prompt_isolation_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 17. `mcp_request_arguments_validated`
- **Stage ID:** mcp_request_arguments_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_request_arguments_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_request_arguments_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 18. `mcp_confused_deputy_checked`
- **Stage ID:** mcp_confused_deputy_checked
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_confused_deputy_checked`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_confused_deputy_checked.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 19. `mcp_egress_policy_checked`
- **Stage ID:** mcp_egress_policy_checked
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_egress_policy_checked`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_egress_policy_checked.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 20. `mcp_request_signature_validated`
- **Stage ID:** mcp_request_signature_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_request_signature_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_request_signature_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 21. `mcp_replay_protection_checked`
- **Stage ID:** mcp_replay_protection_checked
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_replay_protection_checked`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_replay_protection_checked.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 22. `mcp_approval_requirement_evaluated`
- **Stage ID:** mcp_approval_requirement_evaluated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_approval_requirement_evaluated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_approval_requirement_evaluated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 23. `mcp_execution_authorized`
- **Stage ID:** mcp_execution_authorized
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_execution_authorized`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_execution_authorized.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 24. `mcp_response_received`
- **Stage ID:** mcp_response_received
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_response_received`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_response_received.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 25. `mcp_response_safety_validated`
- **Stage ID:** mcp_response_safety_validated
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_response_safety_validated`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_response_safety_validated.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 26. `mcp_audit_written`
- **Stage ID:** mcp_audit_written
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_audit_written`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_audit_written.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned

### 27. `mcp_finding_recorded_if_needed`
- **Stage ID:** mcp_finding_recorded_if_needed
- **Purpose:** Validate this control checkpoint before MCP execution proceeds.
- **Mapped risks:** R-MCP-001..R-MCP-012 (as applicable).
- **Mapped requirements:** SR-MCP-001, SR-MCP-002, SR-MCP-003.
- **Mapped patch points:** PP-MCP-01, PP-MCP-02, PP-MCP-03.
- **Required context fields:** tenant_id, workspace_id, subject_id, server_id, tool_id, resource_id, prompt_id, request_id.
- **Planned policy check:** policy engine evaluation for stage preconditions and risk tier constraints.
- **Safe denial category:** authorization_denied / validation_denied / safety_denied (sanitized).
- **Audit event:** `audit.mcp.mcp_finding_recorded_if_needed`.
- **Finding condition:** emit finding when policy denies, safety flags, or required context missing.
- **Metric:** `metric.mcp.mcp_finding_recorded_if_needed.count`, outcome-labeled.
- **Planned tests:** mapped in `docs/security/mcp_hardening_test_plan.md`.
- **Implementation status:** planned
