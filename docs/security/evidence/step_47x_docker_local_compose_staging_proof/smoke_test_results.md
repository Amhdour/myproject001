# Smoke Test Results

## Summary

All required local smoke tests, portfolio checkers, and the Step 47X evidence checker passed.

## Exact output

```text
$ python -m pytest backend/security_layer/tests/test_step_39x_runtime_enforcement.py -q
/root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
  warnings.warn(
......                                                                   [100%]
=============================== warnings summary ===============================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: 5 warnings
security_layer/tests/test_step_39x_runtime_enforcement.py: 6 warnings
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== warnings summary (final) ===========================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
6 passed, 12 warnings in 0.10s
$ python -m pytest backend/security_layer/tests -q
/root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
  warnings.warn(
........................................................................ [ 25%]
........................................................................ [ 51%]
..................................ssssssss.............................. [ 76%]
..................................................................       [100%]
=============================== warnings summary ===============================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: 5 warnings
security_layer/tests/test_artifact_content_scanners.py: 3 warnings
security_layer/tests/test_artifact_controls.py: 2 warnings
security_layer/tests/test_artifact_metadata_contract.py: 5 warnings
security_layer/tests/test_artifact_models.py: 1 warning
security_layer/tests/test_artifact_release_policy.py: 2 warnings
security_layer/tests/test_artifact_validators.py: 3 warnings
security_layer/tests/test_cache_controls.py: 2 warnings
security_layer/tests/test_cache_key_contract.py: 7 warnings
security_layer/tests/test_cache_models.py: 2 warnings
security_layer/tests/test_cache_validators.py: 5 warnings
security_layer/tests/test_demo_attack_runner.py: 8 warnings
security_layer/tests/test_enforce_mode_blast_radius.py: 5 warnings
security_layer/tests/test_enforce_mode_controls.py: 11 warnings
security_layer/tests/test_enforce_mode_feature_flags.py: 6 warnings
security_layer/tests/test_enforce_mode_gates.py: 6 warnings
security_layer/tests/test_enforce_mode_models.py: 3 warnings
security_layer/tests/test_enforce_mode_simulator.py: 6 warnings
security_layer/tests/test_evidence_room_index.py: 4 warnings
security_layer/tests/test_evidence_room_models.py: 3 warnings
security_layer/tests/test_final_review_decision.py: 3 warnings
security_layer/tests/test_final_review_models.py: 3 warnings
security_layer/tests/test_ingestion_controls.py: 6 warnings
security_layer/tests/test_ingestion_models.py: 1 warning
security_layer/tests/test_ingestion_validators.py: 2 warnings
security_layer/tests/test_mcp_controls.py: 1 warning
security_layer/tests/test_mcp_credential_isolation.py: 1 warning
security_layer/tests/test_mcp_egress_policy.py: 1 warning
security_layer/tests/test_mcp_models.py: 1 warning
security_layer/tests/test_mcp_registry_contract.py: 1 warning
security_layer/tests/test_mcp_request_validators.py: 1 warning
security_layer/tests/test_mcp_signing_replay.py: 1 warning
security_layer/tests/test_mcp_validators.py: 1 warning
security_layer/tests/test_monitor_only_cache_adapter.py: 3 warnings
security_layer/tests/test_monitor_only_feature_flags.py: 4 warnings
security_layer/tests/test_monitor_only_models.py: 2 warnings
security_layer/tests/test_monitor_only_shared_sink.py: 2 warnings
security_layer/tests/test_policy_evaluator.py: 9 warnings
security_layer/tests/test_policy_loader.py: 4 warnings
security_layer/tests/test_policy_models.py: 1 warning
security_layer/tests/test_policy_validator.py: 4 warnings
security_layer/tests/test_regression_demo_fixtures.py: 3 warnings
security_layer/tests/test_regression_demo_models.py: 2 warnings
security_layer/tests/test_regression_demo_non_leakage.py: 2 warnings
security_layer/tests/test_regression_demo_runner.py: 3 warnings
security_layer/tests/test_regression_demo_scenarios.py: 2 warnings
security_layer/tests/test_retrieval_context_builder.py: 3 warnings
security_layer/tests/test_retrieval_controls.py: 5 warnings
security_layer/tests/test_retrieval_integration_flags.py: 2 warnings
security_layer/tests/test_retrieval_integration_hook.py: 2 warnings
security_layer/tests/test_retrieval_live_monitor_only_integration.py: 11 warnings
security_layer/tests/test_retrieval_models.py: 1 warning
security_layer/tests/test_retrieval_security_fixtures.py: 6 warnings
security_layer/tests/test_retrieval_security_future_modes.py: 9 warnings
security_layer/tests/test_retrieval_security_monitor_only.py: 1 warning
security_layer/tests/test_retrieval_security_negative_cases.py: 13 warnings
security_layer/tests/test_retrieval_validators.py: 1 warning
security_layer/tests/test_runtime_audit_findings_metrics.py: 1 warning
security_layer/tests/test_runtime_contexts.py: 3 warnings
security_layer/tests/test_runtime_denials.py: 7 warnings
security_layer/tests/test_runtime_wrappers.py: 4 warnings
security_layer/tests/test_shadow_deny_controls.py: 2 warnings
security_layer/tests/test_shadow_deny_decision_schema.py: 2 warnings
security_layer/tests/test_shadow_deny_feature_flags.py: 3 warnings
security_layer/tests/test_shadow_deny_models.py: 1 warning
security_layer/tests/test_shadow_deny_simulator.py: 2 warnings
security_layer/tests/test_staging_checklist.py: 3 warnings
security_layer/tests/test_staging_execution.py: 6 warnings
security_layer/tests/test_staging_models.py: 3 warnings
security_layer/tests/test_step_39x_runtime_enforcement.py: 6 warnings
security_layer/tests/test_tool_argument_validators.py: 4 warnings
security_layer/tests/test_tool_controls.py: 3 warnings
security_layer/tests/test_tool_models.py: 1 warning
security_layer/tests/test_tool_registry_contract.py: 7 warnings
security_layer/tests/test_tool_validators.py: 6 warnings
security_layer/tests/test_vector_controls.py: 3 warnings
security_layer/tests/test_vector_metadata_contract.py: 7 warnings
security_layer/tests/test_vector_models.py: 1 warning
security_layer/tests/test_vector_validators.py: 5 warnings
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== warnings summary (final) ===========================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
274 passed, 8 skipped, 288 warnings in 1.00s
$ python demo_attacks/run_demo_attacks.py
Demo Attack Runner Report
=========================
Scope: deterministic synthetic portfolio demo only.
Runtime behavior modified: no.
Live enforcement claimed or enabled: no.
Network/tool/MCP calls performed: no.

[PASS] prompt_injection: Prompt injection
  risk_category: instruction hierarchy / prompt injection
  expected_decision: denied_or_flagged
  actual_decision: denied_or_flagged
  expected_evidence: instruction_override_detected; unauthorized_data_request

[PASS] retrieval_cross_tenant_leakage: Retrieval cross-tenant leakage
  risk_category: retrieval isolation / tenant boundary
  expected_decision: denied_or_flagged
  actual_decision: denied_or_flagged
  expected_evidence: tenant_mismatch_detected; retrieval_scope_violation

[PASS] unsafe_tool_call: Unsafe tool call
  risk_category: agent tool authorization
  expected_decision: denied_or_flagged
  actual_decision: denied_or_flagged
  expected_evidence: unsafe_tool_intent_detected; missing_approval_context

[PASS] mcp_confused_deputy: MCP confused deputy
  risk_category: MCP authorization / confused deputy
  expected_decision: denied_or_flagged
  actual_decision: denied_or_flagged
  expected_evidence: cross_authority_request_detected; mcp_scope_mismatch

[PASS] sensitive_data_exposure: Sensitive data exposure
  risk_category: sensitive data handling
  expected_decision: denied_or_flagged
  actual_decision: denied_or_flagged
  expected_evidence: synthetic_secret_pattern_detected; disclosure_risk_flagged

Overall result: PASS
$ python scripts/portfolio/check_claim_boundary.py
PASS: claim-boundary check found no unsafe positive readiness claims across 798 reviewer-facing files.
$ python scripts/portfolio/check_no_fake_claims.py
PASS: fake-claim check found no unsupported positive evidence claims across 798 reviewer-facing files.
$ python scripts/portfolio/check_evidence_links.py

Required files present (12):
  - README.md
  - portfolio/README.md
  - portfolio/architecture.md
  - portfolio/reviewer_quickstart.md
  - portfolio/demo_script.md
  - portfolio/claim_boundary.md
  - portfolio/evidence_index.md
  - docs/security/README.md
  - docs/security/execution_tracker.md
  - docs/security/evidence_report.md
  - docs/security/known_limitations.md
  - docs/security/partner_safe_claims.md

Required files missing (0):
  - none

Optional files present (4):
  - docs/security/final_claim_boundary.md
  - docs/security/final_evidence_package_index.md
  - docs/security/evidence/step_34x_oracle_free_vps/go_no_go.md
  - deployment/docker_compose/docker-compose.step34x-minimal.yml

Optional files absent (0):
  - none

PASS: all required reviewer evidence files are present.
$ python scripts/portfolio/check_release_candidate.py

PASS: Required release-candidate files
  Present (11):
    - portfolio/release_candidate/README.md
    - portfolio/release_candidate/v0.1.0_portfolio_review.md
    - portfolio/release_candidate/final_go_no_go.md
    - portfolio/release_candidate/final_reviewer_path.md
    - portfolio/release_candidate/final_commands.md
    - portfolio/release_candidate/final_status_badges.md
    - portfolio/release_candidate/final_outreach_pack.md
    - portfolio/release_candidate/final_manual_review_checklist.md
    - docs/security/evidence/release_candidate/README.md
    - docs/security/evidence/release_candidate/release_candidate_go_no_go.md
    - docs/security/evidence/release_candidate/final_evidence_map.md
  Missing (0):
    - none

PASS: Required existing portfolio packages
  Present (13):
    - README.md
    - PORTFOLIO_CASE_STUDY.md
    - CLAIM_BOUNDARY.md
    - portfolio/README.md
    - portfolio/evidence_index.md
    - portfolio/release_prep/README.md
    - portfolio/public_sharing_audit/README.md
    - demo_attacks/README.md
    - demo_attacks/run_demo_attacks.py
    - scripts/portfolio/check_public_sharing_readiness.py
    - scripts/portfolio/check_claim_boundary.py
    - scripts/portfolio/check_no_fake_claims.py
    - scripts/portfolio/check_evidence_links.py
  Missing (0):
    - none

PASS: all required release-candidate and prerequisite files are present.
$ python scripts/portfolio/check_step_42x_staging_evidence.py
PASS: Step 42X evidence package is complete in docs/security/evidence/step_42x_live_staging_deployment_evidence
PASS: blocked-deployment claim boundaries are present.
$ python scripts/portfolio/check_step_43x_github_sync_evidence.py
PASS: Step 43X evidence package is complete in docs/security/evidence/step_43x_github_remote_pr_ci_verification_gate
PASS: PR/CI status is explicitly blocked or unavailable, with claim boundaries preserved.
$ python scripts/portfolio/check_step_44x_repository_recovery_evidence.py
PASS: Step 44X evidence package is complete in docs/security/evidence/step_44x_local_repository_recovery_branch_commit_integrity_gate
PASS: repository recovery remains explicitly blocked, with claim boundaries preserved.
$ python scripts/portfolio/check_step_45x_pr_chain_ci_evidence.py
PASS: Step 45X evidence package is complete with classification PR_CHAIN_PARTIALLY_VERIFIED.
PASS: CI, PR metadata, live staging, enterprise, external validation, and compliance boundaries are preserved.
$ python scripts/portfolio/check_step_46x_ci_evidence.py
PASS: Step 46X evidence package is complete with classification CI_ACTIONS_BLOCKED.
PASS: CI success, live staging, enterprise, external validation, and compliance claim boundaries are preserved.
$ python scripts/portfolio/check_step_47x_docker_staging_evidence.py
PASS: Step 47X evidence package is complete with classification DOCKER_STAGING_BLOCKED.
PASS: Docker/local staging, live staging, enterprise, external validation, and compliance claim boundaries are preserved.
$ git diff --check

```

## Claim boundaries

This Step 47X evidence does not claim live cloud/VPS staging validation, production readiness, enterprise production readiness, external validation, compliance certification, full Onyx-wide enforcement, customer deployment, CI pass, or local Docker staging success.

## Readiness status after Step 47X

- Production-style portfolio readiness: 87%.
- Enterprise production-candidate readiness: NO-GO / 5%.
- Local Docker staging evidence: BLOCKED.
- Live staging/cloud validation: PENDING.
- CI Actions evidence: BLOCKED.
- External validation: PENDING.
- Compliance certification: NOT CLAIMED.

