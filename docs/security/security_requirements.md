# Security Requirements Catalog (Step 6)

Status: Initial documentation baseline only. No controls implemented in this step.

## Requirement Entries

### SR-ING-001 — Secure Ingestion Admission Controls
- **Requirement ID:** SR-ING-001
- **Title:** Secure ingestion admission controls
- **Requirement statement:** The ingestion pipeline must validate connector identity, content provenance metadata, and tenant scope before document acceptance.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-ING-01, PP-ING-02
- **Required tests:** Integration test with valid/invalid connector identity and tenant mismatches.
- **Required evidence:** Ingestion policy spec, test output, and audit event samples.
- **Blocker status:** Open (R-016 baseline dependency blocker may limit full local verification).

### SR-RET-001 — Retrieval Authorization and ACL Enforcement
- **Requirement ID:** SR-RET-001
- **Title:** Retrieval ACL enforcement
- **Requirement statement:** Retrieval must enforce user, tenant, and document ACL constraints at query and post-filter stages.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-RET-01, PP-RET-02
- **Required tests:** Integration tests for allow/deny across tenant and role boundaries.
- **Required evidence:** ACL test matrix, query logs, deny-event samples.
- **Blocker status:** Open.

### SR-VEC-001 — Vector Namespace and Metadata Isolation
- **Requirement ID:** SR-VEC-001
- **Title:** Vector isolation guardrails
- **Requirement statement:** Vector operations must enforce namespace partitioning and immutable tenant metadata filters.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-VEC-01, PP-VEC-02
- **Required tests:** Isolation tests proving no cross-namespace retrieval.
- **Required evidence:** Vector filter policy docs and test run artifacts.
- **Blocker status:** Open.

### SR-CACHE-001 — Cache Isolation and TTL Consistency
- **Requirement ID:** SR-CACHE-001
- **Title:** Cache isolation
- **Requirement statement:** Cache keys and invalidation flows must include tenant and ACL version dimensions to prevent stale leakage.
- **Priority:** should
- **Status:** draft
- **Mapped patch points:** PP-CACHE-01
- **Required tests:** Cache key composition tests and stale-ACL invalidation tests.
- **Required evidence:** Cache key schema and invalidation trace logs.
- **Blocker status:** Open.

### SR-TOOL-001 — Tool Authorization Policy
- **Requirement ID:** SR-TOOL-001
- **Title:** Tool authorization policy
- **Requirement statement:** Agent tool execution must be policy-gated by user role, data scope, and explicit allowlists.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-TOOL-01, PP-TOOL-02
- **Required tests:** Positive/negative tool invocation authorization tests.
- **Required evidence:** Tool policy definitions and blocked execution audit records.
- **Blocker status:** Open.

### SR-MCP-001 — MCP Trust and Capability Hardening
- **Requirement ID:** SR-MCP-001
- **Title:** MCP hardening
- **Requirement statement:** MCP server access must use explicit capability scoping, caller binding, and request intent verification.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-MCP-01, PP-MCP-02
- **Required tests:** Confused-deputy simulation tests.
- **Required evidence:** Capability map and enforcement logs.
- **Blocker status:** Open.

### SR-ART-001 — Artifact Output Safety Controls
- **Requirement ID:** SR-ART-001
- **Title:** Artifact safety
- **Requirement statement:** Generated artifacts must be scanned for secret patterns and disallowed data classes before release.
- **Priority:** should
- **Status:** draft
- **Mapped patch points:** PP-ART-01
- **Required tests:** Artifact scanning tests with seeded secrets.
- **Required evidence:** Scanner configuration and sample findings.
- **Blocker status:** Open.

### SR-SBX-001 — Sandbox Execution Safety
- **Requirement ID:** SR-SBX-001
- **Title:** Sandbox safety
- **Requirement statement:** Sandbox executions must apply command restrictions, network boundaries, and execution provenance logging.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-SBX-01, PP-SBX-02
- **Required tests:** Escape-attempt tests and command policy tests.
- **Required evidence:** Sandbox policy docs and execution logs.
- **Blocker status:** Open.

### SR-APPROVAL-001 — Human Approval Workflow
- **Requirement ID:** SR-APPROVAL-001
- **Title:** Approval workflow
- **Requirement statement:** High-risk actions must require a human approval checkpoint with immutable decision records.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-APPROVAL-01
- **Required tests:** Approval-required and bypass-attempt test cases.
- **Required evidence:** Approval decision logs and workflow configuration.
- **Blocker status:** Open.

### SR-AUDIT-001 — End-to-End Auditability
- **Requirement ID:** SR-AUDIT-001
- **Title:** Auditability
- **Requirement statement:** Security-relevant actions must emit structured, attributable, and queryable audit events.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-AUDIT-01, PP-AUDIT-02
- **Required tests:** Audit completeness and tamper-evidence tests.
- **Required evidence:** Audit schema, sample events, retention policy.
- **Blocker status:** Open.

### SR-DLP-001 — Data Loss Prevention Boundaries
- **Requirement ID:** SR-DLP-001
- **Title:** DLP safeguards
- **Requirement statement:** Sensitive data classes must be detected and restricted based on policy during ingestion, retrieval, and output.
- **Priority:** should
- **Status:** draft
- **Mapped patch points:** PP-DLP-01
- **Required tests:** DLP detection and policy action tests.
- **Required evidence:** DLP taxonomy and test report.
- **Blocker status:** Open.

### SR-PROMPT-001 — Prompt Governance and Injection Resistance
- **Requirement ID:** SR-PROMPT-001
- **Title:** Prompt governance
- **Requirement statement:** Prompt assembly must separate trusted instructions from untrusted content and apply injection defenses.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-PROMPT-01, PP-PROMPT-02
- **Required tests:** Prompt injection red-team scenarios.
- **Required evidence:** Prompt composition rules and attack replay results.
- **Blocker status:** Open.

### SR-MODEL-001 — Model/Provider Data Boundary Controls
- **Requirement ID:** SR-MODEL-001
- **Title:** Model/provider controls
- **Requirement statement:** Provider routing must enforce approved models, data handling constraints, and tenant-appropriate endpoints.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-MODEL-01
- **Required tests:** Provider policy enforcement tests and deny-path tests.
- **Required evidence:** Provider allowlist config and route decision logs.
- **Blocker status:** Open.

### SR-ADMIN-001 — Administrative Action Security
- **Requirement ID:** SR-ADMIN-001
- **Title:** Admin security
- **Requirement statement:** Administrative interfaces must require strong authorization, separation of duties, and elevated action logging.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-ADMIN-01
- **Required tests:** Admin role boundary tests and privileged-action logging checks.
- **Required evidence:** Role matrix and privileged audit samples.
- **Blocker status:** Open.

### SR-CI-001 — CI Security and Quality Gates
- **Requirement ID:** SR-CI-001
- **Title:** CI/security gates
- **Requirement statement:** CI pipelines must enforce required security checks, documentation checks, and release blockers for critical findings.
- **Priority:** should
- **Status:** draft
- **Mapped patch points:** PP-CI-01
- **Required tests:** Pipeline policy test and required-check failure simulation.
- **Required evidence:** CI gate definitions and run results.
- **Blocker status:** Open (R-016 impacts one local baseline test path).

### SR-EVIDENCE-001 — Evidence and Launch Gate Criteria
- **Requirement ID:** SR-EVIDENCE-001
- **Title:** Evidence and launch gates
- **Requirement statement:** Production-readiness decisions must be conditioned on complete evidence artifacts and unresolved-risk thresholds.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-EVIDENCE-01
- **Required tests:** Readiness checklist completeness validation.
- **Required evidence:** Signed evidence report, residual risk acceptance record.
- **Blocker status:** Open (No production readiness claim).

## Step 9 Planned Fixture Coverage References
The following planned fixture catalog provides requirement-level test data coverage mapping for all security requirements in this document:
- `docs/security/test_data_factories.md`
- `docs/security/evidence/test_data_factories/fixture_traceability_summary.md`

Per-requirement fixture references (planned):
- SR-ING-001: FX-CONN-001, FX-DOC-001, FX-MALDOC-001
- SR-RET-001: FX-TENANT-001, FX-USER-001, FX-ACL-001, FX-XTENANT-001, FX-EXPACL-001, FX-DELDOC-001
- SR-VEC-001: FX-VNS-001, FX-EMBED-001, FX-CHUNK-001, FX-POISONCHUNK-001
- SR-CACHE-001: FX-CACHE-001, FX-STALEACL-001
- SR-TOOL-001: FX-TOOL-001, FX-UNAUTH-TOOL-001
- SR-MCP-001: FX-MCPSRV-001, FX-MCPRES-001, FX-UNAUTH-MCP-001
- SR-ART-001: FX-ART-001, FX-SECRETA-001
- SR-SBX-001: FX-SBXCFG-001, FX-POLICY-001
- SR-APPROVAL-001: FX-APPROVAL-001, FX-APPBYPASS-001
- SR-AUDIT-001: FX-AUDIT-001
- SR-DLP-001: FX-ART-001, FX-SECRETA-001, FX-MALDOC-001
- SR-PROMPT-001: FX-PROMPT-001, FX-POISONCHUNK-001
- SR-MODEL-001: FX-MODEL-001
- SR-ADMIN-001: FX-ADMIN-001, FX-ROLE-001
- SR-CI-001: FX-FINDING-001 (evidence completeness fixtures)
- SR-EVIDENCE-001: FX-FINDING-001, FX-AUDIT-001

All fixture references above are planning metadata only; no fixture implementation is included in this step.


## Step 10 Migration-Safety Requirement References
The following requirement mappings add migration-safety planning references relevant to CI, evidence, admin, and retrieval domains:
- SR-CI-001: Planned migration CI gates include dry-run, rollback, clean/existing DB migration, drift detection, seed validations, and backup/restore checks (see `docs/security/migration_safety.md`).
- SR-EVIDENCE-001: Migration evidence bundle requirements include prerequisite check, run logs, drift output, seed validation, and backup/restore proof.
- SR-ADMIN-001: Admin/security migration operations must be blocked without backup-before-migration and restore validation evidence.
- SR-RET-001: Retrieval safety depends on existing-database migration validation and ACL/document seed checks to prevent post-migration authorization regressions.

## Step 11 Policy-Schema References

The following SR groupings now reference policy-schema artifacts:
- SR policy governance requirements map to `docs/security/policy_schema.md`.
- SR traceability requirements map to `docs/security/policies/*.yaml` and `docs/security/control_traceability_matrix.md`.
- SR evidence requirements map to `docs/security/evidence/policy_schema/`.

These references are documentation-level only and do not represent active runtime enforcement.

### SR-POL-001 — Policy Engine Governance and Fail-Closed Evaluation
- **Requirement ID:** SR-POL-001
- **Title:** Policy engine governance and fail-closed evaluation
- **Requirement statement:** Policy evaluation must validate policy integrity at startup and operate fail-closed for invalid policies, missing required context, and engine failures.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-AUDIT-01, PP-EVIDENCE-01
- **Required tests:** Policy engine load/validate/evaluate and fail-closed test suite.
- **Required evidence:** Policy engine design doc, test plan, and decision/audit evidence set.
- **Blocker status:** Open.

## Step 13A Runtime Context & Wrapper Design References

The following planned controls define runtime authorization context propagation and enforcement wrapper contracts (design-only in Step 13A):
- `docs/security/runtime_context_wrappers.md`
- `docs/security/runtime_context_wrappers_test_plan.md`

No backend runtime enforcement is active from these additions.

## Step 14A Safe Denial Behavior Requirements

### SR-DENY-001 — Safe Denial Response Standardization
- **Requirement ID:** SR-DENY-001
- **Title:** Safe denial response standardization
- **Requirement statement:** Denial responses across API/UI/streaming/tool/MCP/sandbox/retrieval surfaces must use standardized safe categories, generic user-facing messaging, redaction, and non-leakage controls.
- **Priority:** must
- **Status:** draft
- **Mapped patch points:** PP-DENY-01, PP-DENY-02, PP-DENY-03
- **Required tests:** See `docs/security/safe_denial_behavior_test_plan.md` (T-DENY-001 through T-DENY-024).
- **Required evidence:** Denial category inventory, traceability summary, and denial test-plan evidence bundle.
- **Blocker status:** Open (design-only; no runtime enforcement wiring).
