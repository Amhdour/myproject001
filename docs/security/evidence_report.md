# Evidence Report

## Purpose
Define and maintain the evidence index, acceptance criteria, and review checklist for security-readiness documentation artifacts.

## Scope
Documentation-only security evidence under `docs/security/` and `docs/security/evidence/`.

## Status
draft

## Evidence Index Structure
- `docs/security/evidence/` as the canonical evidence root.
- `docs/security/evidence/templates/` for standardized artifact templates.
- Step/topic subdirectories (for example: `evidence_standardization/`) containing inventories and supporting records.

## Current Evidence Categories
- Baseline and baseline validation evidence.
- Architecture discovery evidence.
- Patch-point mapping evidence.
- Requirements/risk/traceability evidence.
- Evidence standardization artifacts and template inventories.
- Known limitations and blocker records.
- Execution tracker records and tracker-support evidence artifacts.

## Baseline Evidence Section
References baseline commit and baseline validation state:
- `BASELINE_COMMIT.md`
- `docs/security/baseline_validation.md`

## Architecture Discovery Evidence Section
References architecture analysis and system mapping:
- `docs/security/architecture_discovery.md`

## Patch-Point Evidence Section
References control insertion and ownership mapping:
- `docs/security/patch_points.md`

## Requirements/Risk/Traceability Evidence Section
References requirements and traceability artifacts:
- `docs/security/security_requirements.md`
- `docs/security/risk_register.md`
- `docs/security/control_traceability_matrix.md`

## Execution Tracker Evidence Section
References execution-governance tracking artifacts:
- `docs/security/execution_tracker.md`
- `docs/security/evidence/execution_tracker/prerequisite_check.txt`
- `docs/security/evidence/execution_tracker/tracker_summary.md`

## Missing Evidence Section
Current gaps to be filled in later phases:
- Control implementation artifacts.
- Executed security test logs with final outcomes.
- CI-integrated evidence bundles.
- Formal launch-gate signoff records.

## Evidence Acceptance Criteria
Evidence is accepted when it:
1. Uses standard metadata fields.
2. Links to requirement/risk/patch-point IDs when applicable.
3. Includes command/action, expected vs actual outcome, and pass/fail/skipped status.
4. Identifies raw artifact location.
5. Contains redaction and reviewer status.
6. Avoids unsupported readiness or compliance claims.

## Evidence Review Checklist
- [ ] Evidence ID present and unique.
- [ ] Requirement/risk/patch-point links present (or marked N/A).
- [ ] Environment, commit SHA, operator, and timestamp recorded.
- [ ] Expected/actual result and status recorded.
- [ ] Raw artifact path is valid.
- [ ] Redaction status declared.
- [ ] Reviewer and notes completed.
- [ ] Non-claim language preserved when blockers exist.

## Related Links
- [Evidence Standard](./evidence_standard.md)
- [Known Limitations](./known_limitations.md)
- [Security README](./README.md)

## No-Readiness-Claim Statement
This evidence report summarizes documentation artifacts and evidence format status only. It does **not** claim production readiness, control effectiveness, or compliance certification.

## Test-Data-Fixtures Evidence Section (Step 9)
References Step 9 planning and evidence artifacts:
- `docs/security/test_data_factories.md`
- `docs/security/evidence/test_data_factories/prerequisite_check.txt`
- `docs/security/evidence/test_data_factories/fixture_inventory.md`
- `docs/security/evidence/test_data_factories/fixture_traceability_summary.md`
- `docs/security/evidence/test_data_factories/remote_sync_limitation.txt` (when remote verification is unavailable)


## Migration-Safety Evidence Category (Step 10)
References Step 10 migration-safety planning artifacts:
- `docs/security/migration_safety.md`
- `docs/security/evidence/migration_safety/prerequisite_check.txt`
- `docs/security/evidence/migration_safety/migration_safety_plan_summary.md`
- `docs/security/evidence/migration_safety/migration_risk_traceability.md`
- `docs/security/evidence/migration_safety/remote_sync_limitation.txt` (when remote verification remains unavailable)

## Step 11 Evidence Category: Policy Schema and Policy Files

Added evidence category `policy_schema` to track:
- prerequisite verification
- draft policy file inventory
- policy schema summary
- policy traceability summary
- remote/main verification limitation (when applicable)

## Step 12A Evidence Category: Policy Engine Design
Evidence bundle path: `docs/security/evidence/policy_engine_design/`
- prerequisite_check.txt
- policy_engine_design_summary.md
- policy_engine_test_plan_summary.md
- policy_engine_traceability_summary.md
- remote_sync_limitation.txt (if remote verification remains unavailable)

## Policy Engine Minimal Implementation Evidence (Step 12B)

Evidence artifacts for Step 12B are stored in:
`docs/security/evidence/policy_engine_minimal/`

## Step 12C Evidence Category: Policy Engine Validation Cleanup

Evidence bundle path: `docs/security/evidence/policy_engine_validation/`
- prerequisite_check.txt
- isolation_check.txt
- test_coverage_summary.md
- test_output.txt
- test_exitcode.txt
- remote_sync_limitation.txt (if remote verification remains unavailable)

## Step 13A Evidence Category: Runtime Context/Wrapper Design

Planned evidence set for runtime context and enforcement wrapper design is tracked under:
- `docs/security/evidence/runtime_context_wrappers_design/`

This category is documentation-only evidence and does not indicate active runtime enforcement.

## Runtime Context/Wrapper Minimal Evidence
- Added isolated runtime contexts, wrappers, denials, and in-memory test helpers.
- Added isolated test coverage for allow/deny/approval and mode handling.

## Step 13C Evidence Category: Runtime Wrapper Validation Cleanup
Evidence bundle path: `docs/security/evidence/runtime_wrapper_validation/`
- prerequisite_check.txt
- isolation_check.txt
- wrapper_coverage_summary.md
- test_output.txt
- test_exitcode.txt
- remote_sync_limitation.txt (when remote verification remains unavailable)

## Step 14A Evidence Update — Safe Denial Behavior Design

- Status: complete (documentation/design/test-planning only)
- Evidence path: `docs/security/evidence/safe_denial_behavior_design/`
- Included artifacts:
  - `prerequisite_check.txt`
  - `denial_category_inventory.md`
  - `safe_denial_test_plan_summary.md`
  - `safe_denial_traceability_summary.md`
  - `remote_sync_limitation.txt` (if remote sync limitation applies)
- Runtime enforcement status: not wired / not activated.

## Step 14B Evidence Category: Safe Denial Behavior Minimal
Evidence bundle path: `docs/security/evidence/safe_denial_behavior_minimal/`
- prerequisite_check.txt
- implementation_summary.md
- denial_category_coverage.md
- non_leakage_test_summary.md
- test_output.txt
- test_exitcode.txt
- remote_sync_limitation.txt (if remote verification remains unavailable)

## Safe Denial Validation Evidence Category (Step 14C)
References Step 14C validation artifacts:
- `docs/security/evidence/safe_denial_validation/prerequisite_check.txt`
- `docs/security/evidence/safe_denial_validation/isolation_check.txt`
- `docs/security/evidence/safe_denial_validation/denial_coverage_summary.md`
- `docs/security/evidence/safe_denial_validation/non_leakage_validation_summary.md`
- `docs/security/evidence/safe_denial_validation/test_output.txt`
- `docs/security/evidence/safe_denial_validation/test_exitcode.txt`
- `docs/security/evidence/safe_denial_validation/remote_sync_limitation.txt` (when remote remains inaccessible)

## Step 15A Evidence Category: Secure Ingestion Design
- Category: `secure_ingestion_design`
- Scope: design-only secure ingestion stages, test planning, and traceability mapping.
- Required artifacts:
  - `docs/security/evidence/secure_ingestion_design/prerequisite_check.txt`
  - `docs/security/evidence/secure_ingestion_design/ingestion_stage_inventory.md`
  - `docs/security/evidence/secure_ingestion_design/secure_ingestion_test_plan_summary.md`
  - `docs/security/evidence/secure_ingestion_design/secure_ingestion_traceability_summary.md`
  - `docs/security/evidence/secure_ingestion_design/remote_sync_limitation.txt` (if applicable)
- Non-claim: no runtime enforcement activation is represented by this category.

## Step 15B Evidence Category: Secure Ingestion Minimal Isolated Controls
Evidence bundle path: `docs/security/evidence/secure_ingestion_minimal/`
- prerequisite_check.txt
- implementation_summary.md
- ingestion_control_coverage.md
- test_output.txt
- test_exitcode.txt
- remote_sync_limitation.txt (when remote verification remains unavailable)

## Step 15C Evidence Category: Secure Ingestion Validation Cleanup
Evidence bundle path: `docs/security/evidence/secure_ingestion_validation/`
- prerequisite_check.txt
- isolation_check.txt
- ingestion_coverage_summary.md
- non_leakage_validation_summary.md
- test_output.txt
- test_exitcode.txt
- remote_sync_limitation.txt (when remote verification remains unavailable)

## Step 16A Evidence Category — Retrieval ACL Design
- Category ID: EVID-RET-ACL-DESIGN-16A
- Required artifacts:
  - `docs/security/retrieval_acl.md`
  - `docs/security/retrieval_acl_test_plan.md`
  - `docs/security/evidence/retrieval_acl_design/prerequisite_check.txt`
  - `docs/security/evidence/retrieval_acl_design/retrieval_acl_stage_inventory.md`
  - `docs/security/evidence/retrieval_acl_design/retrieval_acl_test_plan_summary.md`
  - `docs/security/evidence/retrieval_acl_design/retrieval_acl_traceability_summary.md`
  - `docs/security/evidence/retrieval_acl_design/remote_sync_limitation.txt` (if remote verification blocked)
- Acceptance note: design/test-planning evidence only; no runtime enforcement claim.

## Step 16B Evidence Category (2026-05-27)
- Added `docs/security/evidence/retrieval_acl_minimal/` evidence pack for isolated retrieval ACL controls.

## Step 16C Evidence Category: Retrieval ACL Validation Cleanup
Evidence bundle path: `docs/security/evidence/retrieval_acl_validation/`
- prerequisite_check.txt
- isolation_check.txt
- retrieval_acl_coverage_summary.md
- non_leakage_validation_summary.md
- test_output.txt
- test_exitcode.txt
- remote_sync_limitation.txt (when remote verification remains unavailable)

## Step 17A - retrieval path patching design evidence
- Scope: retrieval-path patching design, patch-candidate inventory, rollout/test planning, and traceability.
- Evidence directory: `docs/security/evidence/retrieval_path_patching_design/`
- Core artifacts:
  - `prerequisite_check.txt`
  - `retrieval_path_inventory.md`
  - `patch_candidate_inventory.md`
  - `retrieval_path_test_plan_summary.md`
  - `retrieval_path_traceability_summary.md`
  - `remote_sync_limitation.txt` (when remote verification is blocked)

## Step 17A Evidence Category
Added retrieval path patching design evidence category and bundle references.

## Step 17B Evidence Category: Retrieval Path Integration Planning
- Category ID: EVID-RINT-PLAN
- Scope: Integration sequencing/checklist/test-plan/traceability for retrieval ACL runtime path integration.
- Required artifacts:
  - `docs/security/evidence/retrieval_path_integration_plan/prerequisite_check.txt`
  - `docs/security/evidence/retrieval_path_integration_plan/integration_phase_inventory.md`
  - `docs/security/evidence/retrieval_path_integration_plan/integration_checklist_summary.md`
  - `docs/security/evidence/retrieval_path_integration_plan/integration_test_plan_summary.md`
  - `docs/security/evidence/retrieval_path_integration_plan/integration_traceability_summary.md`
- Status: planned/collected-for-step-17b-docs
\n## Step 17C Update\n- Isolated feature-flag helper implemented.\n- Isolated retrieval context builder implemented.\n- Isolated monitor/shadow/enforce hook helper implemented.\n- No live retrieval path patched; production enforcement remains inactive.

## Step 17C Evidence Category (2026-05-27)
- Added evidence bundle: `docs/security/evidence/retrieval_context_builder_isolated/`.
- Contains prerequisite verification, implementation summaries, and isolated test outputs/exit code.

## Step 17D Evidence Category (Retrieval Integration Readiness)
- Category: `retrieval_integration_readiness`
- Required artifacts:
  - prerequisite verification output
  - readiness review summary
  - go/no-go summary
  - live patch target inventory summary
  - test readiness summary
  - isolated test output + exit code
  - remote/main sync limitation note (if applicable)
\n\n## Step 17E Update (2026-05-27)\n- Added first live retrieval monitor-only hook at  after existing retrieval guard result handling.\n- Mode is disabled by default (), and monitor_only is the only live-enabled behavior for this step.\n- Enforce mode remains NO-GO and is not wired into live retrieval path.\n- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.\n

## Step 17E Update (2026-05-27)
- Added first live retrieval monitor-only hook at `backend/onyx/context/search/retrieval/search_runner.py` after existing retrieval guard result handling.
- Mode is disabled by default (`default_retrieval_integration_config`), and monitor_only is the only live-enabled behavior for this step.
- Enforce mode remains NO-GO and is not wired into live retrieval path.
- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.


## Step 17F Update (2026-05-27)
- Retrieval monitor-only validation completed.
- Disabled mode preserves retrieval behavior.
- Monitor-only mode preserves retrieval behavior.
- Enforce mode remains NO-GO/inactive.
- Retrieval blocking/filtering/denial remains disabled in live path.

## Step 18A Evidence Category (2026-05-27)
- Added retrieval security test design evidence category under `docs/security/evidence/retrieval_security_tests_design/`.

## Step 18B Evidence Category (2026-05-27)
- Category: Retrieval Security Test Fixtures and Skeletons
- Evidence location: `docs/security/evidence/retrieval_security_test_skeletons/`
- Includes prerequisite verification, fixture summary, monitor-only skeleton summary, future-mode skipped/xfail summary, and test command output/exit code.

## Step 18B-A Evidence Refresh (2026-05-27)
- Retrieval security test skeleton execution rerun passed.
- Artifacts updated under `docs/security/evidence/retrieval_security_test_skeletons/`.

## Step 18C Evidence Category Added (2026-05-27)
- `docs/security/evidence/retrieval_security_test_validation/`
- Captures prerequisite checks, fixture-quality validation, monitor-only validation, future-mode skip validation, and test outputs/exit code.


## Step 18D-A Retrieval Security Negative Test Coverage Cleanup (2026-05-27)
- Focused suite: pass (20 passed, 8 skipped).
- Full security_layer suite: pass (87 passed, 8 skipped).
- Evidence folder: `docs/security/evidence/retrieval_security_negative_tests/`.

## Step 18E Evidence Category (2026-05-27)
- Added `docs/security/evidence/retrieval_security_negative_validation/` for Step 18E validation artifacts.
- Includes prerequisite verification, negative-case quality checks, monitor-only preservation checks, non-leakage checks, future-mode blocker validation, and test command evidence.

## Step 19A Evidence Category — Vector DB Security Design
- Category: `vector_db_security_design`
- Scope: design, traceability, planned tests, planned metadata contract.
- Required artifacts:
  - `docs/security/evidence/vector_db_security_design/prerequisite_check.txt`
  - `docs/security/evidence/vector_db_security_design/vector_stage_inventory.md`
  - `docs/security/evidence/vector_db_security_design/vector_metadata_contract_summary.md`
  - `docs/security/evidence/vector_db_security_design/vector_test_plan_summary.md`
  - `docs/security/evidence/vector_db_security_design/vector_traceability_summary.md`
  - `docs/security/evidence/vector_db_security_design/remote_sync_limitation.txt` (if remote verification remains unavailable)
- Runtime claim: none. This category is design/planning evidence only.

## Step 19B Evidence Category (2026-05-27)
- Added `docs/security/evidence/vector_db_security_minimal/` for prerequisite verification, implementation summary, metadata/control coverage, and test execution evidence.

## Step 19C Evidence Category (2026-05-27)
- Added `docs/security/evidence/vector_db_security_validation/` with prerequisite verification, model/metadata/validator/control validation notes, non-leakage validation notes, and captured test output/exit codes.

## Step 20A Evidence Category — Cache Security Design
- Design artifacts:
  - `docs/security/cache_security.md`
  - `docs/security/cache_security_test_plan.md`
  - `docs/security/cache_key_contract.md`
- Evidence directory:
  - `docs/security/evidence/cache_security_design/`
- Scope note: design/test-planning only; no runtime enforcement activation.

## Step 20B Evidence
- Added `docs/security/evidence/cache_security_minimal/` with prerequisite check, implementation summaries, control/key coverage, and test artifacts.

## Step 20C Evidence Category (2026-05-28)
- Added `docs/security/evidence/cache_security_validation/`.
- Includes prerequisite check, model/key/validator/control validation notes, non-leakage notes, and test run artifacts.

## Step 21A Evidence Category
- `docs/security/evidence/tool_authorization_design/` contains prerequisite checks, stage inventory, registry contract summary, argument security summary, test plan summary, traceability summary, and remote limitation note.
