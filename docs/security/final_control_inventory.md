# Final Control Inventory

This inventory maps each requested control to the code, tests, demo attacks, evidence docs, environment flags, proven claims, and limitations that are visible in this repository.

## 1) OPA Retrieval ACL

- **Status:** implemented, tested, demoed, evidence-backed.
- **Code files:** `backend/onyx/security_layer/opa/*`, `backend/onyx/security_layer/retrieval_guard/*`.
- **Tests:** `backend/tests/security_layer/test_opa_retrieval_acl.py`, `backend/tests/security_layer/test_opa_retrieval_context_filter.py`, `backend/tests/security_layer/test_retrieval_acl_proof.py`, `backend/tests/security_layer/test_runtime_retrieval_acl_step_63x.py`.
- **Demo attacks:** `scripts/security/demo_attacks/opa/retrieval_acl_policy_bypass_demo.py`, `scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py`.
- **Evidence docs:** `docs/security/evidence/retrieval_acl_design/`, `docs/security/evidence/retrieval_acl_minimal/`, `docs/security/evidence/retrieval_acl_validation/`, `docs/security/evidence/bundle_*_retrieval_acl_*.md`, `docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/`, `docs/security/evidence/langfuse/`.
- **Env flags:** `SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT`, `ONYX_SECURITY_RETRIEVAL_ACL_MODE`.
- **Proven claims:** retrieval inputs are normalized; denied chunks are excluded from final RAG context; fallback deny behavior exists when OPA is unavailable; audit/tracing metadata stays safe.
- **Limitations:** full live tenant isolation is not claimed; live production traffic is not validated; fallback behavior is still a local and staged proof point, not a production attestation.

## 2) OpenTelemetry tracing

- **Status:** implemented, tested, evidence-backed.
- **Code files:** `backend/onyx/security_layer/tracing.py`, `backend/onyx/security_layer/opa/retrieval_context_filter.py`, `backend/onyx/security_layer/scanners/rag_injection_scanner.py`, `backend/onyx/security_layer/tool_governance/decision_mapper.py`, `backend/onyx/security_layer/mcp_governance/decision_mapper.py`, `backend/onyx/security_layer/gateway_governance/decision_mapper.py`.
- **Tests:** `backend/tests/security_layer/test_security_tracing.py`, `backend/tests/unit/onyx/tracing/test_flows_registry.py`, `backend/tests/unit/onyx/tracing/test_tracing_setup.py`, `backend/tests/external_dependency_unit/tracing/test_llm_span_recording.py`.
- **Demo attacks:** all security demo scripts emit decision/evidence metadata through the traced decision paths.
- **Evidence docs:** `docs/security/evidence/langfuse/trace_schema.md`, `docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/telemetry_sample.md`.
- **Env flags:** OpenTelemetry import availability; no special feature flag is required for the helper itself.
- **Proven claims:** the helper creates security spans when OpenTelemetry is installed; scalar attribute sanitization works; security decision paths set span attributes.
- **Limitations:** this does not prove a full OpenTelemetry deployment, collector pipeline, or backend-wide trace coverage.

## 3) Langfuse-safe evidence bridge

- **Status:** implemented, tested, evidence-backed.
- **Code files:** `backend/onyx/security_layer/langfuse_evidence.py`, `backend/onyx/security_layer/redaction.py`.
- **Tests:** `backend/tests/security_layer/test_langfuse_evidence.py`.
- **Demo attacks:** `scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py`, `scripts/security/demo_attacks/tool_governance/high_risk_tool_requires_approval_demo.py`, `scripts/security/demo_attacks/mcp_governance/mcp_scope_bypass_demo.py`.
- **Evidence docs:** `docs/security/evidence/langfuse/`, `docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/audit_log_sample.md`, `docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/telemetry_sample.md`.
- **Env flags:** `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`.
- **Proven claims:** the bridge allowlists only safe metadata, redacts defense-in-depth fields, and no-ops safely when Langfuse is unavailable.
- **Limitations:** Langfuse runtime emission is optional and dependency-gated; this is a safe evidence bridge, not an independent validation service.

## 4) Redaction utility

- **Status:** implemented, tested, evidence-backed.
- **Code files:** `backend/onyx/security_layer/redaction.py`, `backend/onyx/security_layer/audit/redaction.py`.
- **Tests:** `backend/tests/security_layer/test_redaction.py`, `backend/tests/unit/onyx/server/features/build/sandbox/test_exec_helpers_redaction.py`.
- **Demo attacks:** all evidence-emitting demo scripts and redteam parsers rely on the redaction boundary.
- **Evidence docs:** `docs/security/evidence/redteam/limitations.md`, `docs/security/evidence/redteam/redteam_summary.md`, `docs/security/evidence/step_57x_external_validation_staging_review/redaction_and_public_safety_review.md`.
- **Env flags:** Presidio installation availability; no dedicated feature flag is required for the fallback redaction path.
- **Proven claims:** emails, bearer tokens, API keys, JWT-like strings, and nested secret-like fields are redacted; the utility can use Presidio when available and regex fallback otherwise.
- **Limitations:** this is a best-effort safety layer, not a guarantee that every possible secret shape is covered.

## 5) RAG injection scanner

- **Status:** implemented, tested, demoed, evidence-backed.
- **Code files:** `backend/onyx/security_layer/scanners/rag_injection_scanner.py`, `backend/onyx/security_layer/scanners/decision_mapper.py`, `backend/onyx/security_layer/scanners/llamafirewall_adapter.py`, `backend/onyx/security_layer/scanners/agentshield_adapter.py`.
- **Tests:** `backend/tests/security_layer/test_rag_injection_scanner.py`, `backend/tests/security_layer/test_demo_attacks.py`, `backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py`.
- **Demo attacks:** `scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py`.
- **Evidence docs:** `docs/security/evidence/retrieval_monitor_only_validation/`, `docs/security/evidence/retrieval_security_test_validation/`, `docs/security/evidence/retrieval_security_test_skeletons/`, `docs/security/evidence/regression_demo_attack_bundle/`, `docs/security/evidence/langfuse/`.
- **Env flags:** `SECURITY_RAG_INJECTION_SCANNER_ENABLED`, `SECURITY_RAG_INJECTION_SCANNER_MODE`, `SECURITY_RAG_INJECTION_SCANNER_FAILURE_MODE`, `SECURITY_RAG_SCANNER_PROVIDER`, `SECURITY_RAG_SCANNER_FALLBACK_PROVIDER`, `SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT`.
- **Proven claims:** obvious prompt-injection text can be denied or sanitized; disabled mode preserves current behavior; safe evidence excludes raw chunk text.
- **Limitations:** live behavior depends on the selected provider path; optional backend adapters are fallback-tested unless explicitly dependency-backed.

## 6) Optional LlamaFirewall adapter

- **Status:** implemented as optional adapter, fallback-tested.
- **Code files:** `backend/onyx/security_layer/scanners/llamafirewall_adapter.py`.
- **Tests:** `backend/tests/security_layer/test_rag_injection_scanner.py`.
- **Demo attacks:** `scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py`.
- **Evidence docs:** `docs/security/evidence/retrieval_security_test_validation/`, `docs/security/evidence/retrieval_monitor_only_validation/`.
- **Env flags:** `SECURITY_RAG_SCANNER_PROVIDER`, `SECURITY_RAG_SCANNER_FALLBACK_PROVIDER`.
- **Proven claims:** the adapter is optional, safe when missing, and can fall back without exporting raw content.
- **Limitations:** real LlamaFirewall backend behavior is not proven unless the dependency is installed and exercised in a dependency-backed run.

## 7) Optional AgentShield adapter

- **Status:** implemented as optional adapter, fallback-tested.
- **Code files:** `backend/onyx/security_layer/scanners/agentshield_adapter.py`.
- **Tests:** `backend/tests/security_layer/test_rag_injection_scanner.py`.
- **Demo attacks:** `scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py`.
- **Evidence docs:** `docs/security/evidence/retrieval_security_test_validation/`, `docs/security/evidence/retrieval_monitor_only_validation/`.
- **Env flags:** `SECURITY_RAG_SCANNER_PROVIDER`, `SECURITY_RAG_SCANNER_FALLBACK_PROVIDER`.
- **Proven claims:** the adapter is optional, safe when missing, and can fall back without exporting raw content.
- **Limitations:** real AgentShield backend behavior is not proven unless the dependency is installed and exercised in a dependency-backed run.

## 8) Tool governance

- **Status:** implemented, tested, demoed, evidence-backed.
- **Code files:** `backend/onyx/security_layer/tool_governance/decision_mapper.py`, `backend/onyx/security_layer/tool_governance/enforcement.py`, `backend/onyx/security_layer/tool_governance/approval.py`, `backend/onyx/security_layer/tool_governance/risk_registry.py`, `backend/onyx/security_layer/tool_governance/receipts.py`.
- **Tests:** `backend/tests/security_layer/test_tool_governance.py`, `backend/tests/security_layer/test_tool_authorization.py`, `backend/tests/security_layer/test_tool_argument_scanner.py`, `backend/tests/security/test_security_enforcement_integration.py`, `backend/tests/security/test_security_enforcer.py`.
- **Demo attacks:** `scripts/security/demo_attacks/tool_governance/high_risk_tool_requires_approval_demo.py`.
- **Evidence docs:** `docs/security/evidence/tool_authorization_design/`, `docs/security/evidence/tool_governance/`, `docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/`.
- **Env flags:** `SECURITY_TOOL_GOVERNANCE_ENFORCEMENT`, `SECURITY_LAYER_ENABLED`, `SECURITY_LAYER_MODE`, `SECURITY_LAYER_REQUIRE_CONTEXT`, `SECURITY_LAYER_FAIL_CLOSED_IN_ENFORCE`.
- **Proven claims:** low-risk tools can be allowed; high-risk or critical tools can require approval or be denied; approval replay protection exists; raw tool payload is excluded from evidence.
- **Limitations:** this is not a blanket proof of every tool path in the product.

## 9) MCP governance

- **Status:** implemented, tested, demoed, evidence-backed.
- **Code files:** `backend/onyx/security_layer/mcp_governance/decision_mapper.py`, `backend/onyx/security_layer/mcp_governance/enforcement.py`, `backend/onyx/security_layer/mcp_governance/registry.py`, `backend/onyx/security_layer/mcp_governance/receipts.py`.
- **Tests:** `backend/tests/security_layer/test_mcp_governance.py`, `backend/tests/security_layer/test_mcp_governance_enforcement.py`, `backend/tests/security_layer/test_mcp_authorization.py`.
- **Demo attacks:** `scripts/security/demo_attacks/mcp_governance/mcp_scope_bypass_demo.py`.
- **Evidence docs:** `docs/security/evidence/mcp_governance/`, `docs/security/evidence/mcp_hardening_design/`, `docs/security/evidence/mcp_hardening_validation/`.
- **Env flags:** `SECURITY_MCP_GOVERNANCE_ENFORCEMENT`, `SECURITY_MCP_AUTH_ENABLED`, `SECURITY_LAYER_REQUIRE_CONTEXT`, `SECURITY_LAYER_MODE`.
- **Proven claims:** scope-based decisions work; missing context can deny in enforce mode; audit evidence is produced; raw MCP payload is excluded from safe evidence.
- **Limitations:** real external MCP server enforcement is not claimed here.

## 10) Gateway governance

- **Status:** implemented, tested, demoed, evidence-backed.
- **Code files:** `backend/onyx/security_layer/gateway_governance/decision_mapper.py`, `backend/onyx/security_layer/gateway_governance/route_policy.py`, `backend/onyx/security_layer/gateway_governance/evidence.py`, `backend/onyx/security_layer/gateway_governance/models.py`.
- **Tests:** `backend/tests/security_layer/test_gateway_governance.py`.
- **Demo attacks:** `scripts/security/demo_attacks/gateway_governance/external_secret_route_block_demo.py`, `scripts/security/demo_attacks/gateway_governance/restricted_tenant_external_route_demo.py`.
- **Evidence docs:** `docs/security/evidence/gateway_governance/`, `docs/security/evidence/evaluations/`, `docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/`.
- **Env flags:** `SECURITY_GATEWAY_GOVERNANCE_ENABLED`, `SECURITY_GATEWAY_RESTRICTED_EXTERNAL_MODE`, `SECURITY_GATEWAY_PII_EXTERNAL_MODE`, `SECURITY_GATEWAY_HIGH_RISK_MODE`.
- **Proven claims:** clean low-risk external requests can route externally; secret-bearing external requests are denied; restricted tenant data can be routed privately or denied; evidence excludes raw prompt/context.
- **Limitations:** external routing behavior is policy-driven and not a deployment attestation.

## 11) RAG/security evaluations

- **Status:** implemented, tested, generated evidence, fixture-backed.
- **Code files:** `backend/onyx/security_layer/evaluations/rag_security_eval.py`, `backend/onyx/security_layer/evaluations/ragas_adapter.py`, `backend/onyx/security_layer/evaluations/promptfoo_adapter.py`, `backend/onyx/security_layer/evaluations/models.py`.
- **Tests:** `backend/tests/security_layer/test_rag_security_evaluations.py`.
- **Demo attacks:** `scripts/security/evaluations/run_rag_security_eval.py`.
- **Evidence docs:** `docs/security/evidence/evaluations/README.md`, `docs/security/evidence/evaluations/eval_results.md`, `docs/security/evidence/evaluations/limitations.md`, `docs/security/evidence/evaluations/reproduction_commands.md`.
- **Env flags:** no dedicated flag is required for the local fixture evaluation; dependency-backed Ragas and promptfoo execution is optional.
- **Proven claims:** local fixture datasets can be evaluated; the result bundle is written successfully; promptfoo bundle generation works; dependency-missing paths safely no-op.
- **Limitations:** real Ragas and promptfoo execution is not proven unless dependency-backed runs are performed.

## 12) PyRIT/garak evidence foundation

- **Status:** implemented as a fixture-backed evidence foundation, tested, mapped to controls.
- **Code files:** `backend/onyx/security_layer/redteam/pyrit_adapter.py`, `backend/onyx/security_layer/redteam/garak_adapter.py`, `backend/onyx/security_layer/redteam/findings_mapper.py`, `backend/onyx/security_layer/redteam/models.py`.
- **Tests:** `backend/tests/security_layer/test_redteam_evidence.py`.
- **Demo attacks:** `scripts/security/redteam/run_external_redteam_summary.py`.
- **Evidence docs:** `docs/security/evidence/redteam/README.md`, `docs/security/evidence/redteam/redteam_summary.md`, `docs/security/evidence/redteam/limitations.md`, `docs/security/evidence/redteam/reproduction_commands.md`, `docs/security/evidence/redteam/findings_to_controls.md`, `docs/security/evidence/redteam/fixtures/`.
- **Env flags:** dependency availability for `pyrit` and `garak`; fixture mode is the default local path.
- **Proven claims:** fixture parsing works; findings map back to controls; sanitized summaries exclude raw evidence; optional dependency checks no-op safely.
- **Limitations:** true PyRIT or garak execution is not proven unless a dependency-backed run is performed.
