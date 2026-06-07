# Portfolio Readiness Report — AI Trust & Security Readiness

## Executive summary

This package is the final portfolio evidence bundle for the AI Trust & Security Readiness project.

It summarizes implemented, tested, demoed, and evidence-backed controls for an Onyx-based RAG and autonomous-agent security portfolio. It does **not** claim production readiness, enterprise readiness, external validation, or compliance certification.

### Final posture

- **Portfolio readiness:** `99%` evidence-package completeness.
- **Production-style control coverage:** `83%` of the requested control set is implemented and locally demonstrated; `17%` remains optional, fallback-backed, or dependency-backed only.
- **Enterprise-production claim:** **not made**.
- **External-validation claim:** **not made**.

### What this package proves

- OPA Retrieval ACL enforcement is implemented and tested.
- OpenTelemetry-based security tracing is wired for the security spans used in the portfolio.
- Langfuse evidence emission is safety-wrapped to exclude raw prompts, chunks, tokens, and secret material.
- Redaction is available as a defense-in-depth utility.
- RAG injection scanning is implemented with deny/sanitize/monitor-style policies and optional adapter paths.
- Tool governance, MCP governance, and gateway governance are implemented with evidence, receipts, and safe metadata handling.
- Fixture-backed evaluation and red-team evidence foundations are present and mapped back to controls.

### What this package does not prove

- Live production traffic validation.
- Enterprise audit completion.
- Full backend-wide integration coverage.
- Real dependency-backed PyRIT, garak, Ragas, promptfoo, LlamaFirewall, or AgentShield behavior unless those dependencies are explicitly installed and exercised.

## Controlled demo path

Use the following sequence for a recruiter/client-friendly walkthrough:

1. Show the claim boundary and safe claims in [`final_safe_claims.md`](final_safe_claims.md).
2. Show the control inventory in [`final_control_inventory.md`](final_control_inventory.md).
3. Show the evidence index in [`final_evidence_index.md`](final_evidence_index.md).
4. Walk the demo script in [`final_demo_script.md`](final_demo_script.md).
5. Show the readiness scorecard in [`final_readiness_scorecard.md`](final_readiness_scorecard.md).
6. Close with the known limitations in [`final_known_limitations.md`](final_known_limitations.md).

## Final demo path required by this package

The final demo path is bounded to the controls that are implemented and evidenced in this repository:

- cross-tenant retrieval blocked;
- malicious retrieved chunk denied or sanitized;
- high-risk tool requires approval;
- MCP scope bypass denied;
- secret external route denied;
- restricted tenant external route blocked or routed privately;
- evaluation summary generated;
- red-team finding mapped to control.

## Command checklist

Run these commands to validate the package and its surrounding evidence:

```bash
git diff --check
python scripts/security/validate_security_evidence.py
python scripts/security/evaluations/run_rag_security_eval.py
python scripts/security/redteam/run_external_redteam_summary.py
python scripts/security/demo_attacks/opa/retrieval_acl_policy_bypass_demo.py
python scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
python scripts/security/demo_attacks/tool_governance/high_risk_tool_requires_approval_demo.py
python scripts/security/demo_attacks/mcp_governance/mcp_scope_bypass_demo.py
python scripts/security/demo_attacks/gateway_governance/external_secret_route_block_demo.py
python scripts/security/demo_attacks/gateway_governance/restricted_tenant_external_route_demo.py
```

## Safe boundary statement

This is a portfolio-grade evidence package for security review, not a production-readiness attestation and not an enterprise-readiness attestation.
