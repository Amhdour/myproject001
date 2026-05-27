# Policy Schema (Planned)

## Purpose
Define a **draft, documentation-only** schema for future security policy artifacts. This schema standardizes how policy intent, scope, risk alignment, and evidence expectations are captured before any runtime implementation.

## Scope
- Applies only to policy design artifacts under `docs/security/`.
- Does **not** alter running system behavior.
- Does **not** implement evaluation or enforcement in application runtime.

## Status
- Status: `draft` / `planned`
- Owner: Security Engineering (design phase)

## Non-Claim Statement
This document and associated policy files are planning artifacts only. They are **not active controls**, **not enforced**, and **not sufficient evidence** of production security effectiveness.

## Policy Design Principles
1. Default deny unless an allow rule is explicitly satisfied.
2. Least privilege across subjects, resources, and actions.
3. Explicit risk and requirement traceability for each policy.
4. Explainable decisions with auditable rationale.
5. Versioned, owned, reviewable artifacts.
6. Environment-aware policy targeting.

## Policy File Structure
Each policy file must include:
- `policy_id`
- `title`
- `version`
- `status`
- `owner`
- `environment`
- `scope`
- `default_effect`
- `rules`
- `required_context`
- `approval_requirements`
- `audit_requirements`
- `mapped_requirements`
- `mapped_risks`
- `mapped_patch_points`
- `planned_tests`
- `planned_evidence`
- `non_claim_statement`

## Policy Evaluation Model (Planned)
- Input: subject, resource, action, context.
- Rule matching: evaluate all relevant scoped rules.
- Conflict handling: `deny` overrides `allow`.
- Decision output: effect, matched rules, findings, explainability payload.
- Enforcement mode support: planning for monitor-only and blocking modes.

## Default-Deny Principle
If no rule grants explicit allow conditions, the effective decision is deny. The baseline/default-deny policy anchors this behavior in design.

## Policy Effects
- `allow`
- `deny`
- `conditional_allow` (requires additional approvals/constraints)
- `monitor_only` (observation/logging intent only)

## Policy Scopes
- `ingestion`
- `retrieval`
- `vector_db`
- `cache`
- `tools`
- `mcp`
- `artifacts`
- `sandbox`
- `approvals`
- `admin`
- `audit`
- `model_provider`
- `prompt`
- `dlp`
- `launch_gate`
- `global_default`

## Risk Levels
- `low`
- `medium`
- `high`
- `critical`

## Approval Requirements
Planned requirements can declare:
- approval role(s) (e.g., security_reviewer, system_owner)
- approval threshold (single, two-person, quorum)
- approval freshness/validity window

## Audit Requirements
Planned audit requirements can declare:
- mandatory event capture fields
- retention targets
- immutable evidence references
- periodic review cadence

## Enforcement Modes (Planned)
- `disabled` (documentation only)
- `monitor`
- `soft_fail`
- `hard_fail`

## Policy Versioning
- Semantic version format: `MAJOR.MINOR.PATCH`
- Draft files begin at `0.x.y`
- Breaking schema changes increment MAJOR

## Policy Ownership
Each policy must declare explicit owner metadata and reviewer expectations in future governance workflows.

## Policy Environment Targeting
Policies must name intended environment(s): `dev`, `staging`, `prod`, or `all`. Environment targeting is design metadata only at this phase.

## Policy Hash / Integrity Expectations
Planned integrity controls:
- Canonical file hashing for policy artifacts
- Change approvals tied to hash/version
- Evidence snapshots storing hash manifests

## Explainability Requirements
Planned decisions should include:
- policy_id and rule_id references
- rationale text
- required context keys used
- unresolved conditions/exceptions

## Validation Requirements (Planned)
- Schema linting of required fields/types
- Reference integrity checks for mapped requirements/risks/patch points
- Duplicate policy/rule identifier detection

## Test Requirements (Planned)
- Static schema validation tests
- Policy inventory coverage tests
- Traceability completeness checks
- Decision fixture tests (once engine exists)

## Evidence Requirements (Planned)
- Policy inventory snapshots
- Traceability summaries
- Validation output artifacts
- Review/approval records

## Known Limitations
- No runtime policy engine exists yet.
- No active enforcement path exists yet.
- Validation automation is not implemented.
- Policy files are draft planning artifacts.

## Planned Schema Objects

### 1) `Policy`
Top-level policy artifact containing metadata, scope, defaults, and rules.

### 2) `PolicyRule`
Atomic rule with match criteria and intended effect.

### 3) `PolicyDecision`
Planned decision output object: effective effect + explainability + findings.

### 4) `PolicyEffect`
Enumerated effect type (`allow`, `deny`, etc.).

### 5) `PolicyScope`
Enumerated domain scope (ingestion, retrieval, etc.).

### 6) `RiskLevel`
Enumerated risk severity associated to rule/policy.

### 7) `ApprovalRequirement`
Planned approval constraints needed for policy, rule, or exception.

### 8) `AuditRequirement`
Planned audit logging and retention expectations.

### 9) `EnforcementMode`
Planned enforcement posture (`disabled`, `monitor`, `soft_fail`, `hard_fail`).

### 10) `PolicySubject`
Actor attributes used in policy matching (human, service, automation identity).

### 11) `PolicyResource`
Target object attributes (data class, index, artifact, tool, provider, etc.).

### 12) `PolicyAction`
Requested operation (`read`, `write`, `invoke`, `approve`, etc.).

### 13) `PolicyContext`
Auxiliary context used in decisions (environment, ticket, approval id, source).

### 14) `PolicyException`
Planned temporary override object with expiration and approval provenance.

### 15) `PolicyFinding`
Structured finding emitted during evaluation/validation (info/warn/error).

### 16) `PolicyAuditEvent`
Canonical audit event shape for future policy decision recording.
