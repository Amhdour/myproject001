# Step 43X Local Verification Results

## Environment Note
The project guidance recommends activating `.venv`. In this sandbox, `.venv` exists but does not contain `pytest`; the system Python environment does contain `pytest`. The exact `.venv` probe is recorded, and the required test commands were then run successfully with `python` from the available environment.

### `source .venv/bin/activate 2>/dev/null || true; python -m pytest backend/security_layer/tests/test_step_39x_runtime_enforcement.py -q`

```text
/workspace/myproject001/.venv/bin/python: No module named pytest
```

## Required Local Verification Commands

### `python -m pytest backend/security_layer/tests/test_step_39x_runtime_enforcement.py -q`

```text
......                                                                   [100%]
6 passed, 12 warnings in 0.15s
```

Result: **PASS**.

### `python -m pytest backend/security_layer/tests -q`

```text
........................................................................ [ 25%]
........................................................................ [ 51%]
..................................ssssssss.............................. [ 76%]
..................................................................       [100%]
274 passed, 8 skipped, 288 warnings in 1.83s
```

Result: **PASS**.

### `python demo_attacks/run_demo_attacks.py`

```text
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
```

Result: **PASS**.

### `python scripts/portfolio/check_claim_boundary.py`

```text
PASS: claim-boundary check found no unsafe positive readiness claims across 740 reviewer-facing files.
```

Result: **PASS**.

### `python scripts/portfolio/check_no_fake_claims.py`

```text
PASS: fake-claim check found no unsupported positive evidence claims across 740 reviewer-facing files.
```

Result: **PASS**.

### `python scripts/portfolio/check_evidence_links.py`

```text
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
```

Result: **PASS**.

### `python scripts/portfolio/check_release_candidate.py`

```text
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
```

Result: **PASS**.

### `python scripts/portfolio/check_step_42x_staging_evidence.py`

```text
PASS: Step 42X evidence package is complete in docs/security/evidence/step_42x_live_staging_deployment_evidence
PASS: blocked-deployment claim boundaries are present.
```

Result: **PASS**.

### `git diff --check`

```text
```

Result: **PASS**.

### Non-claim unsafe phrase scan: `rg -n "production ready|enterprise ready|certified|externally validated|compliance certified|live deployment proven|customer deployment|full enforcement|Onyx-wide enforcement" README.md PORTFOLIO_CASE_STUDY.md docs portfolio backend || true`

```text
The scan returned claim-boundary, negative, or non-claim statements only. It included existing lines that explicitly state the portfolio is not production-ready, not enterprise-ready, not compliance-certified, not externally validated, does not prove live/customer deployment, and does not prove full Onyx-wide enforcement.
```

Result: **PASS after manual review**.

## Summary
All required local verification commands passed after using the available Python environment. No local command result supports a claim that GitHub CI ran or passed.
