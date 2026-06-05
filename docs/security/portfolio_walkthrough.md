# Portfolio Walkthrough — AI Trust & Security Readiness MVP

## Problem statement

RAG and autonomous-agent systems need runtime controls that can prove security decisions, not only describe them. This MVP demonstrates policy-as-code, enforcement, audit logging, telemetry, negative tests, demo attacks, and evidence reporting for selected control points.

## Threats demonstrated

- Cross-tenant retrieval attempt.
- Missing tenant context in retrieval.
- High-risk tool execution without approval.
- Unsafe sandbox action without approval.
- Prompt injection in retrieved content documented as a current limitation.

## Controls implemented

- Default-deny policy decisions.
- Approval-required policy decisions for high-risk tool/sandbox actions.
- Monitor-only decision mode.
- Runtime enforcer with safe blocking exception.
- Synthetic, redacted audit events.
- In-memory telemetry metrics and latency samples.
- Retrieval search runner hook for context/cross-tenant filtering.

## How to run tests

```bash
PYTHONPATH=. pytest -q --confcutdir=backend/tests/security backend/tests/security
```

## How to run demo attacks

```bash
PYTHONPATH=. pytest -q --confcutdir=backend/tests/security backend/tests/security/demo_attacks
```

## How to inspect audit logs

Open `docs/security/evidence/audit/sample_security_audit_events.jsonl`.

## How to inspect telemetry

Open `docs/security/evidence/telemetry/sample_security_metrics.json`.

## How to read the evidence report

Start with `docs/security/evidence_report.md`, then review `docs/security/control_traceability_matrix.md` and `docs/security/known_limitations.md`.

## Safe public claim

This repository demonstrates an MVP security-readiness layer for selected RAG/agent control points, including policy-as-code decisions, runtime enforcement, deny/approval behavior, audit logging, telemetry samples, negative tests, demo attacks, and evidence reporting. It is portfolio-ready for demonstrating technical AI security engineering skills, but it is not claimed as production-ready, enterprise-ready, or compliance-certified.

## Recruiter/client demo script

1. Show `backend/security/policy/security_policy.py` for default-deny and approval-required logic.
2. Show `backend/security/enforcement/security_enforcer.py` for runtime blocking behavior.
3. Run the security tests and demo attack tests.
4. Open the audit JSONL and telemetry JSON samples.
5. Open the evidence report and traceability matrix.
6. Close with limitations and next PR recommendations.
