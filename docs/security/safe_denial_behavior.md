# Safe Denial Behavior Design (Step 14A)

## purpose
Define planned, non-enforcing denial response behavior across all security surfaces so denied operations fail safely without leaking sensitive information.

## scope
Documentation, taxonomy, and test-planning only for denial behavior in isolated security-layer components. No runtime integration or API enforcement activation.

## status: planned/design
Planned (design-only).

## owner
AI Trust & Security Readiness Engineer.

## non-claim statement
This document does not claim production readiness and does not indicate active enforcement.

## relationship to policy engine
Policy engine decisions are inputs to denial categories; this step does not change policy evaluation logic.

## relationship to runtime wrappers
Runtime wrappers are future patch points for surfacing standardized denial outputs; wrappers are not wired into request paths.

## denial principles
- Fail closed where required.
- Default to minimal-disclosure messages.
- Separate user and admin messaging.
- Emit auditable, traceable denial metadata.
- Keep behavior consistent across UI/API/streaming/tooling surfaces.

## safe user-facing denial behavior
Generic language with no tenant/resource identity leakage.

## safe admin-facing denial behavior
Actionable summary including category, code, and trace ID but no secret content.

## safe API error behavior
Return stable safe error codes and generic denial text.

## safe audit behavior
Emit denial audit events with redacted contextual fields.

## safe finding behavior
Generate findings for repeated/high-severity denial patterns.

## safe metric behavior
Emit per-category counters and rate metrics without sensitive labels.

## safe UI behavior
Display generic denial banners/messages and safe support guidance.

## safe streaming-response behavior
Terminate stream safely with denial sentinel and no partial sensitive payload.

## safe artifact denial behavior
Block unsafe artifact release with non-leaking denial reason category.

## safe tool denial behavior
Block tool execution with generic message and redacted arguments/secrets.

## safe MCP denial behavior
Block MCP operations with no server credential/endpoint leakage.

## safe sandbox denial behavior
Block sandbox operations with no filesystem or command detail leakage.

## safe retrieval denial behavior
Deny retrieval without revealing denied source/document/chunk metadata.

## safe model/prompt denial behavior
Deny model/prompt operations without exposing prompt internals or policy rules.

## approval-required response behavior
Return approval-required category and safe message; do not disclose policy internals.

## monitor-only behavior
Do not alter end-user behavior; record monitor event without internal-decision leakage.

## shadow-deny behavior
Record hypothetical deny outcome in telemetry only; no internal decision details in user-visible content.

## enforce-mode behavior
Return explicit safe denial category and code with redaction rules applied.

## localization/readability expectations
Use plain-language, translatable message templates with consistent severity semantics.

## error code taxonomy
Prefix `SD-` with deterministic suffixes per denial category.

## redaction rules
Redact tenant IDs, subject IDs, document/chunk content, tool arguments, secrets, MCP credentials, sandbox paths, prompt internals, and policy rule internals.

## non-leakage rules
No raw object identifiers, policy expressions, connector credentials, or stack traces in user-facing denials.

## test strategy
Execute planned unit and integration-style denial message safety tests in isolated security-layer scope.

## evidence requirements
Record prerequisite checks, category inventory, test-plan summary, and traceability summary in `docs/security/evidence/safe_denial_behavior_design/`.

## known limitations
Design-only; enforcement not wired; localization not implemented; telemetry schema not runtime-bound.

## Denial Message Categories (status: planned)

### access_denied
- category ID: access_denied
- user-facing message: Access to this action is not permitted.
- admin-facing summary: Access denied for subject/context boundary check.
- safe error code: SD-ACCESS-001
- audit event name: security.denial.access_denied
- finding condition: repeated denies for same subject/action threshold exceeded
- metric name: security_denial_access_denied_total
- redaction requirements: redact tenant/subject identifiers
- forbidden leaked details: tenant ID, role matrix internals
- mapped risks: R-DENY-001, R-DENY-005
- mapped requirements: SR-DENY-001
- mapped patch points: PP-DENY-01
- planned tests: T-DENY-001, T-DENY-010, T-DENY-012
- status: planned

### policy_denied
- category ID: policy_denied
- user-facing message: The request cannot be completed due to security policy.
- admin-facing summary: Policy decision denied requested operation.
- safe error code: SD-POLICY-001
- audit event name: security.denial.policy_denied
- finding condition: high-rate policy denials for same route
- metric name: security_denial_policy_denied_total
- redaction requirements: redact policy rule internals
- forbidden leaked details: policy expression, rule IDs not approved for display
- mapped risks: R-DENY-002, R-DENY-005
- mapped requirements: SR-DENY-001
- mapped patch points: PP-DENY-01
- planned tests: T-DENY-009, T-DENY-017
- status: planned

### approval_required
- category ID: approval_required
- user-facing message: This action requires approval before it can continue.
- admin-facing summary: Approval checkpoint required for high-risk action.
- safe error code: SD-APPROVAL-001
- audit event name: security.denial.approval_required
- finding condition: approval bypass attempt detected
- metric name: security_denial_approval_required_total
- redaction requirements: redact request payload details
- forbidden leaked details: risk score internals, policy thresholds
- mapped risks: R-DENY-002, R-DENY-004
- mapped requirements: SR-APPROVAL-001, SR-DENY-001
- mapped patch points: PP-APPROVAL-01, PP-DENY-01
- planned tests: T-DENY-016, T-DENY-012
- status: planned

### unsafe_artifact_blocked
- category ID: unsafe_artifact_blocked
- user-facing message: The artifact could not be released due to safety checks.
- admin-facing summary: Artifact release blocked by safety classification.
- safe error code: SD-ART-001
- audit event name: security.denial.unsafe_artifact_blocked
- finding condition: confirmed secret/data class pattern detected
- metric name: security_denial_unsafe_artifact_blocked_total
- redaction requirements: redact artifact content and secret patterns
- forbidden leaked details: file names containing sensitive terms, secret snippets
- mapped risks: R-DENY-001, R-DENY-003
- mapped requirements: SR-ART-001, SR-DENY-001
- mapped patch points: PP-ART-01, PP-DENY-02
- planned tests: T-DENY-021
- status: planned

### unsafe_tool_blocked
- category ID: unsafe_tool_blocked
- user-facing message: The requested tool action is not permitted.
- admin-facing summary: Tool execution denied by safety/authorization controls.
- safe error code: SD-TOOL-001
- audit event name: security.denial.unsafe_tool_blocked
- finding condition: tool deny with high-risk operation signature
- metric name: security_denial_unsafe_tool_blocked_total
- redaction requirements: redact tool arguments/secrets
- forbidden leaked details: tool tokens, argument payloads
- mapped risks: R-DENY-003, R-DENY-005
- mapped requirements: SR-TOOL-001, SR-DENY-001
- mapped patch points: PP-TOOL-02, PP-DENY-02
- planned tests: T-DENY-004, T-DENY-005, T-DENY-023
- status: planned

### unsafe_mcp_blocked
- category ID: unsafe_mcp_blocked
- user-facing message: The MCP request could not be completed safely.
- admin-facing summary: MCP capability request denied.
- safe error code: SD-MCP-001
- audit event name: security.denial.unsafe_mcp_blocked
- finding condition: repeated denied capability escalation attempts
- metric name: security_denial_unsafe_mcp_blocked_total
- redaction requirements: redact server credentials/endpoints
- forbidden leaked details: auth headers, server secret config
- mapped risks: R-DENY-003, R-DENY-005
- mapped requirements: SR-MCP-001, SR-DENY-001
- mapped patch points: PP-MCP-02, PP-DENY-02
- planned tests: T-DENY-006, T-DENY-024
- status: planned

### unsafe_sandbox_blocked
- category ID: unsafe_sandbox_blocked
- user-facing message: The sandbox operation was blocked for safety.
- admin-facing summary: Sandbox policy denied requested operation.
- safe error code: SD-SBX-001
- audit event name: security.denial.unsafe_sandbox_blocked
- finding condition: blocked command family exceeds threshold
- metric name: security_denial_unsafe_sandbox_blocked_total
- redaction requirements: redact sandbox paths/commands
- forbidden leaked details: host paths, exact denied command args
- mapped risks: R-DENY-003, R-DENY-005
- mapped requirements: SR-SBX-001, SR-DENY-001
- mapped patch points: PP-SBX-02, PP-DENY-02
- planned tests: T-DENY-007
- status: planned

### retrieval_denied
- category ID: retrieval_denied
- user-facing message: Requested information is not available for this context.
- admin-facing summary: Retrieval denied by ACL/scope boundary.
- safe error code: SD-RET-001
- audit event name: security.denial.retrieval_denied
- finding condition: repeated cross-scope retrieval attempts
- metric name: security_denial_retrieval_denied_total
- redaction requirements: redact document/chunk identifiers and text
- forbidden leaked details: document names, chunk excerpts, source IDs
- mapped risks: R-DENY-001, R-DENY-005
- mapped requirements: SR-RET-001, SR-DENY-001
- mapped patch points: PP-RET-02, PP-DENY-02
- planned tests: T-DENY-002, T-DENY-003, T-DENY-022
- status: planned

### tenant_context_missing
- category ID: tenant_context_missing
- user-facing message: The request context is incomplete and cannot be processed.
- admin-facing summary: Tenant context missing at authorization boundary.
- safe error code: SD-CTX-001
- audit event name: security.denial.tenant_context_missing
- finding condition: systemic missing tenant context across routes
- metric name: security_denial_tenant_context_missing_total
- redaction requirements: redact fallback context values
- forbidden leaked details: inferred tenant mapping logic
- mapped risks: R-DENY-001, R-DENY-005
- mapped requirements: SR-RET-001, SR-DENY-001
- mapped patch points: PP-CTX-01, PP-DENY-01
- planned tests: T-DENY-001, T-DENY-012
- status: planned

### subject_context_missing
- category ID: subject_context_missing
- user-facing message: The request identity context is incomplete.
- admin-facing summary: Subject context missing for secure decisioning.
- safe error code: SD-CTX-002
- audit event name: security.denial.subject_context_missing
- finding condition: repeated subject-context failures
- metric name: security_denial_subject_context_missing_total
- redaction requirements: redact identity token details
- forbidden leaked details: token claims/session internals
- mapped risks: R-DENY-001, R-DENY-004
- mapped requirements: SR-RET-001, SR-DENY-001
- mapped patch points: PP-CTX-01, PP-DENY-01
- planned tests: T-DENY-012
- status: planned

### policy_engine_unavailable
- category ID: policy_engine_unavailable
- user-facing message: The request cannot be completed at this time.
- admin-facing summary: Policy engine unavailable; fail-closed denial applied.
- safe error code: SD-PE-001
- audit event name: security.denial.policy_engine_unavailable
- finding condition: outage window exceeds SLO threshold
- metric name: security_denial_policy_engine_unavailable_total
- redaction requirements: redact backend topology and stack details
- forbidden leaked details: stack traces, hostnames, internal endpoints
- mapped risks: R-DENY-002, R-DENY-004
- mapped requirements: SR-DENY-001
- mapped patch points: PP-DENY-01
- planned tests: T-DENY-017
- status: planned

### validation_failed
- category ID: validation_failed
- user-facing message: The request is invalid for this action.
- admin-facing summary: Security validation preconditions failed.
- safe error code: SD-VAL-001
- audit event name: security.denial.validation_failed
- finding condition: abnormal validation failure spike
- metric name: security_denial_validation_failed_total
- redaction requirements: redact raw invalid payload fields
- forbidden leaked details: schema internals with security-sensitive fields
- mapped risks: R-DENY-002, R-DENY-004
- mapped requirements: SR-DENY-001
- mapped patch points: PP-DENY-01
- planned tests: T-DENY-012
- status: planned

### rate_or_quota_blocked
- category ID: rate_or_quota_blocked
- user-facing message: Request limit reached. Please try again later.
- admin-facing summary: Security rate/quota threshold triggered denial.
- safe error code: SD-RATE-001
- audit event name: security.denial.rate_or_quota_blocked
- finding condition: repeated quota trips from same subject scope
- metric name: security_denial_rate_or_quota_blocked_total
- redaction requirements: redact exact quota tuning values
- forbidden leaked details: dynamic threshold internals
- mapped risks: R-DENY-004, R-DENY-005
- mapped requirements: SR-DENY-001
- mapped patch points: PP-DENY-01
- planned tests: T-DENY-012
- status: planned

### admin_action_denied
- category ID: admin_action_denied
- user-facing message: Administrative action is not permitted.
- admin-facing summary: Privileged operation denied by admin security policy.
- safe error code: SD-ADMIN-001
- audit event name: security.denial.admin_action_denied
- finding condition: privileged deny with separation-of-duties violation
- metric name: security_denial_admin_action_denied_total
- redaction requirements: redact privilege graph and role internals
- forbidden leaked details: role mapping internals, privileged target identifiers
- mapped risks: R-DENY-004, R-DENY-005
- mapped requirements: SR-ADMIN-001, SR-DENY-001
- mapped patch points: PP-ADMIN-01, PP-DENY-01
- planned tests: T-DENY-011, T-DENY-013
- status: planned

## Step 14B implementation note (2026-05-27)
- Implemented isolated safe denial helpers and structured payload builders in `backend/security_layer/runtime/denials.py`.
- Implemented all 14 denial categories and safe error-code mapping.
- Added isolated wrapper usage for deny/fail-closed and approval-required structured response.
- Runtime enforcement remains inactive and not wired into backend request paths.

## Step 14C validation update (2026-05-27)
- Validation cleanup executed in isolated scope only.
- Denial helpers remain isolated under `backend/security_layer/runtime` and are not wired to production request paths.
- Added strengthened tests for 14 categories, safe error codes, admin summary redaction, forbidden detail filtering, payload helper safety, JSON serializability, and wrapper-safe structured outputs.
- Remote/main verification remained blocked in this environment; local verified state was used.
