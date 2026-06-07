# Final Evidence Index

This index points reviewers to the major evidence areas that support the final portfolio package.

## Top-level portfolio files

- [`portfolio_readiness_report.md`](portfolio_readiness_report.md)
- [`final_control_inventory.md`](final_control_inventory.md)
- [`final_demo_script.md`](final_demo_script.md)
- [`final_safe_claims.md`](final_safe_claims.md)
- [`final_known_limitations.md`](final_known_limitations.md)
- [`final_architecture_map.md`](final_architecture_map.md)
- [`final_readiness_scorecard.md`](final_readiness_scorecard.md)

## Core evidence areas

| Area | Evidence path | Why it matters |
|---|---|---|
| Retrieval ACL design | `docs/security/evidence/retrieval_acl_design/` | Shows the policy and test-plan foundation for OPA retrieval access control. |
| Retrieval ACL minimal + validation | `docs/security/evidence/retrieval_acl_minimal/`, `docs/security/evidence/retrieval_acl_validation/` | Shows the isolated proof path and validation cleanup. |
| Retrieval ACL shadow / live-adjacent bundles | `docs/security/evidence/bundle_a_retrieval_acl_shadow_mode_proof.md`, `docs/security/evidence/bundle_f_retrieval_acl_shadow_integration_proof.md`, `docs/security/evidence/bundle_h_retrieval_acl_live_adjacent_seam_proof.md` | Shows the staged proof chain without overstating live production enforcement. |
| Runtime retrieval ACL review package | `docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/` | Contains the final review helper coverage, audit sample, telemetry sample, demo results, and limitations. |
| Langfuse evidence | `docs/security/evidence/langfuse/` | Documents the safe evidence bridge schema, limitations, and reproduction commands. |
| Tool authorization and governance | `docs/security/evidence/tool_authorization_design/`, `docs/security/evidence/tool_governance/` | Shows tool-risk registry, approval flow, and demo results. |
| MCP hardening and governance | `docs/security/evidence/mcp_hardening_design/`, `docs/security/evidence/mcp_hardening_validation/`, `docs/security/evidence/mcp_governance/` | Shows MCP registry, request-security model, validation, and fixture-backed demo evidence. |
| Gateway governance | `docs/security/evidence/gateway_governance/` | Shows route-policy evidence, demo results, and safe metadata handling. |
| RAG security evaluations | `docs/security/evidence/evaluations/` | Contains the datasets, evaluation results, limitations, and reproduction commands. |
| Red-team evidence foundation | `docs/security/evidence/redteam/` | Contains PyRIT/garak fixture summaries, findings-to-controls mapping, and claim boundaries. |
| Retrieval monitoring / safety proofs | `docs/security/evidence/retrieval_monitor_only_validation/`, `docs/security/evidence/retrieval_security_test_validation/`, `docs/security/evidence/retrieval_context_builder_isolated/` | Shows monitor-only and safe-metadata boundary behavior for the retrieval path. |
| Safe denial and metadata handling | `docs/security/evidence/safe_denial_validation/`, `docs/security/evidence/step_11_retrieval_acl_audit_telemetry_combined_proof_summary.md` | Shows safe denial behavior and audit/telemetry shaping. |
| Public-safety / redaction reviews | `docs/security/evidence/step_56x_external_validation_staging_review/redaction_and_public_safety_review.md`, `docs/security/evidence/step_57x_external_reviewer_response_intake_finding_tracker/redaction_note.md`, `docs/security/evidence/step_58x_external_reviewer_response_intake_finding_tracker/redaction_note.md` | Shows that sensitive artifacts are sanitized before distribution. |
| Final partner/demo bundles | `docs/security/evidence/final_pilot_partner_go_no_go_bundle/`, `docs/security/evidence/partner_evidence_room_bundle/` | Shows the reviewer-facing evidence-room style packaging. |

## Scripts used as evidence generators

- `scripts/security/demo_attacks/opa/retrieval_acl_policy_bypass_demo.py`
- `scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py`
- `scripts/security/demo_attacks/tool_governance/high_risk_tool_requires_approval_demo.py`
- `scripts/security/demo_attacks/mcp_governance/mcp_scope_bypass_demo.py`
- `scripts/security/demo_attacks/gateway_governance/external_secret_route_block_demo.py`
- `scripts/security/demo_attacks/gateway_governance/restricted_tenant_external_route_demo.py`
- `scripts/security/evaluations/run_rag_security_eval.py`
- `scripts/security/redteam/run_external_redteam_summary.py`
- `scripts/security/validate_security_evidence.py`

## Test suites supporting the package

- `backend/tests/security_layer/test_opa_retrieval_acl.py`
- `backend/tests/security_layer/test_opa_retrieval_context_filter.py`
- `backend/tests/security_layer/test_security_tracing.py`
- `backend/tests/security_layer/test_langfuse_evidence.py`
- `backend/tests/security_layer/test_redaction.py`
- `backend/tests/security_layer/test_rag_injection_scanner.py`
- `backend/tests/security_layer/test_tool_governance.py`
- `backend/tests/security_layer/test_tool_authorization.py`
- `backend/tests/security_layer/test_mcp_governance.py`
- `backend/tests/security_layer/test_mcp_governance_enforcement.py`
- `backend/tests/security_layer/test_gateway_governance.py`
- `backend/tests/security_layer/test_rag_security_evaluations.py`
- `backend/tests/security_layer/test_redteam_evidence.py`
- `backend/tests/security/demo_attacks/`

## CI / workflow evidence

- `.github/workflows/opa-policy-checks.yml`
- `.github/workflows/retrieval-acl-shadow-observation-export-tests.yml`
- `.github/workflows/retrieval-acl-adapter-tests.yml`
- `.github/workflows/retrieval-acl-noop-seam-hook-tests.yml`
- `.github/workflows/retrieval-acl-live-adjacent-seam-tests.yml`
- `.github/workflows/retrieval-acl-enforce-harness-tests.yml`
- `.github/workflows/retrieval-acl-search-pipeline-gate-tests.yml`
- `.github/workflows/retrieval-acl-real-path-shadow-observation-tests.yml`
- `.github/workflows/retrieval-acl-shadow-integration-tests.yml`
- `.github/workflows/runtime-retrieval-acl-security.yml`

## Final claim boundaries

Use this index to support reviewer-facing evidence navigation, not production-readiness language.
