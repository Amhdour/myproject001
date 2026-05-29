# Reviewer Quickstart

This quickstart helps reviewers inspect the project quickly while preserving the repository's claim boundaries.

## 1. Inspect the Project at a High Level

Start from the repository root and verify the current branch, commit, and local status:

```bash
git status --short --branch
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
```

Then read the portfolio entry point:

```bash
sed -n '1,220p' portfolio/README.md
```

## 2. Recommended Reading Order

1. [`portfolio/README.md`](README.md) — reviewer entry point and current status.
2. [`portfolio/claim_boundary.md`](claim_boundary.md) — safe claims, forbidden claims, and status matrix.
3. [`portfolio/architecture.md`](architecture.md) — layered architecture and non-enforcement boundary.
4. [`portfolio/evidence_index.md`](evidence_index.md) — map from reviewer questions to repository evidence.
5. [`docs/security/final_claim_boundary.md`](../docs/security/final_claim_boundary.md) — final claim boundary where present.
6. [`docs/security/evidence_report.md`](../docs/security/evidence_report.md) and [`docs/security/execution_tracker.md`](../docs/security/execution_tracker.md) — detailed security-readiness evidence and execution history.
7. [`docs/security/known_limitations.md`](../docs/security/known_limitations.md) — limitations, blockers, and NO-GO context.

## 3. Run the Security-Layer Tests

Run the isolated security-layer test suite from the repository root:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests -q
```

If the repository virtual environment is needed, activate it first and rerun the same command:

```bash
source .venv/bin/activate
PYTHONPATH=. python -m pytest backend/security_layer/tests -q
```

If `pytest` is missing from `.venv`, document the exact dependency error as a local environment blocker. Do not mark that as a project test failure if the non-venv command passes successfully in the current environment.

## 4. Interpret Passing Tests Carefully

Passing tests prove isolated security-layer behavior only. Passing tests do not prove production security, enterprise readiness, live Onyx integration, live enforce-mode protection, live shadow-deny runtime, live blocking, live filtering, compliance certification, or external validation.

## 5. Inspect Deployment Evidence

Deployment/staging evidence should be inspected as scoped evidence only:

- [`docs/security/evidence/step_34x_oracle_free_vps/go_no_go.md`](../docs/security/evidence/step_34x_oracle_free_vps/go_no_go.md) records the Step 34X staging decision if present.
- [`deployment/docker_compose/docker-compose.step34x-minimal.yml`](../deployment/docker_compose/docker-compose.step34x-minimal.yml) records a minimal nginx health-check target if present.

Minimal staging artifacts do not prove full Onyx live staging, production monitoring, backup, rollback, live blocking, or live filtering.

## 6. Inspect Limitations and NO-GO Decisions

Use these files to verify limitations and current decision language:

- [`docs/security/known_limitations.md`](../docs/security/known_limitations.md)
- [`docs/security/partner_safe_claims.md`](../docs/security/partner_safe_claims.md)
- [`docs/security/final_claim_boundary.md`](../docs/security/final_claim_boundary.md)
- [`portfolio/claim_boundary.md`](claim_boundary.md)

The intended reviewer conclusion is that this is a strong production-style portfolio and partner-demo evidence package, not production attestation.
