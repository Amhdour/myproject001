# Final Demo Script

This is the recruiter/client-friendly walkthrough for the final portfolio package.

## Presenter opening

> This repository is a portfolio-grade AI Trust & Security Readiness evidence package. It shows implemented, tested, demoed, and evidence-backed controls for an Onyx-based RAG and autonomous-agent security stack. It does **not** claim production readiness, enterprise readiness, or external validation.

## Walkthrough order

### 1) Cross-tenant retrieval blocked

**Run:**

```bash
python scripts/security/demo_attacks/opa/retrieval_acl_policy_bypass_demo.py
```

**What to say:**

- This demonstrates the OPA Retrieval ACL control.
- The demo models a Tenant A subject trying to reach Tenant B context.
- The expected result is denial of cross-tenant retrieval and exclusion of the unauthorized chunk from the final RAG context.

**What to point at:**

- `backend/onyx/security_layer/opa/retrieval_context_filter.py`
- `backend/tests/security_layer/test_opa_retrieval_acl.py`
- `docs/security/evidence/retrieval_acl_design/`
- `docs/security/evidence/step_63x_runtime_retrieval_acl_review_package/demo_attack_results.md`

### 2) Malicious retrieved chunk denied or sanitized

**Run:**

```bash
python scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
```

**What to say:**

- This shows the retrieved-chunk prompt-injection path.
- A malicious chunk can be denied or sanitized depending on scanner mode.
- The safe evidence path avoids exporting raw retrieved content.

**What to point at:**

- `backend/onyx/security_layer/scanners/rag_injection_scanner.py`
- `backend/onyx/security_layer/scanners/llamafirewall_adapter.py`
- `backend/onyx/security_layer/scanners/agentshield_adapter.py`
- `backend/tests/security_layer/test_rag_injection_scanner.py`
- `backend/tests/security_layer/test_langfuse_evidence.py`

### 3) High-risk tool requires approval

**Run:**

```bash
python scripts/security/demo_attacks/tool_governance/high_risk_tool_requires_approval_demo.py
```

**What to say:**

- This demonstrates tool governance.
- High-risk tool actions can be marked approval-required instead of silently allowed.
- The evidence payload is safe and does not export raw tool args or secret-like content.

**What to point at:**

- `backend/onyx/security_layer/tool_governance/decision_mapper.py`
- `backend/onyx/security_layer/tool_governance/enforcement.py`
- `backend/tests/security_layer/test_tool_governance.py`
- `backend/tests/security_layer/test_tool_authorization.py`
- `docs/security/evidence/tool_governance/`

### 4) MCP scope bypass denied

**Run:**

```bash
python scripts/security/demo_attacks/mcp_governance/mcp_scope_bypass_demo.py
```

**What to say:**

- This demonstrates MCP governance.
- A scope-bypass attempt is denied when required scopes are missing.
- The evidence bridge keeps raw MCP payload content out of the exported evidence.

**What to point at:**

- `backend/onyx/security_layer/mcp_governance/decision_mapper.py`
- `backend/onyx/security_layer/mcp_governance/enforcement.py`
- `backend/tests/security_layer/test_mcp_governance.py`
- `backend/tests/security_layer/test_mcp_governance_enforcement.py`
- `docs/security/evidence/mcp_governance/`

### 5) Secret external route denied

**Run:**

```bash
python scripts/security/demo_attacks/gateway_governance/external_secret_route_block_demo.py
```

**What to say:**

- This shows gateway governance stopping secret-bearing external routing.
- The request is not treated as a safe external-route candidate.
- The route decision is blocked instead of silently forwarded.

**What to point at:**

- `backend/onyx/security_layer/gateway_governance/decision_mapper.py`
- `backend/onyx/security_layer/gateway_governance/route_policy.py`
- `backend/tests/security_layer/test_gateway_governance.py`
- `docs/security/evidence/gateway_governance/`

### 6) Restricted tenant external route blocked or routed privately

**Run:**

```bash
python scripts/security/demo_attacks/gateway_governance/restricted_tenant_external_route_demo.py
```

**What to say:**

- This is the restricted-tenant routing scenario.
- Depending on policy mode, the request is either blocked or routed privately.
- The demo shows the control boundary without claiming live deployment attestation.

**What to point at:**

- `backend/onyx/security_layer/gateway_governance/decision_mapper.py`
- `backend/onyx/security_layer/gateway_governance/route_policy.py`
- `backend/tests/security_layer/test_gateway_governance.py`

### 7) Evaluation summary generated

**Run:**

```bash
python scripts/security/evaluations/run_rag_security_eval.py
```

**What to say:**

- This generates the local RAG security evaluation summary.
- The evaluation is fixture-based and documents limitations clearly.
- Optional Ragas and promptfoo paths are dependency-gated.

**What to point at:**

- `backend/onyx/security_layer/evaluations/rag_security_eval.py`
- `backend/tests/security_layer/test_rag_security_evaluations.py`
- `docs/security/evidence/evaluations/`

### 8) Red-team finding mapped to control

**Run:**

```bash
python scripts/security/redteam/run_external_redteam_summary.py
```

**What to say:**

- This is the red-team evidence foundation.
- Fixture-based PyRIT and garak inputs are parsed and mapped back to controls.
- The summary is explicit that real dependency-backed executions are not proven unless they are actually run.

**What to point at:**

- `backend/onyx/security_layer/redteam/pyrit_adapter.py`
- `backend/onyx/security_layer/redteam/garak_adapter.py`
- `backend/onyx/security_layer/redteam/findings_mapper.py`
- `backend/tests/security_layer/test_redteam_evidence.py`
- `docs/security/evidence/redteam/`

## Closing line

> The important takeaway is not that every enterprise security requirement is complete. The takeaway is that the repository contains a disciplined, evidence-backed security portfolio with clear boundaries, explicit limitations, and reviewer-friendly demos.
