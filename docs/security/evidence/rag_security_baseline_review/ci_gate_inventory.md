# CI Gate Inventory

## Purpose
Inventory CI workflows related to RAG security, retrieval ACL, demo attacks, tests, evidence, lint/type checks, and claim boundaries.

## Commands or search methods used
- `find .github -maxdepth 5 -type f | sort`
- `find .github/workflows -maxdepth 1 -type f -printf '%f\n' | sort`
- `rg -n "pytest|retrieval|demo_attack|security_layer|evidence|lint|pyright|mypy" .github/workflows`
- Direct inspection of selected workflow YAML files.

## Files found
- `.github/workflows/security-layer-tests.yml`
- `.github/workflows/security-readiness.yml`
- `.github/workflows/retrieval-acl-runtime-tests.yml`
- `.github/workflows/retrieval-acl-telemetry-tests.yml`
- `.github/workflows/retrieval-acl-search-pipeline-gate-tests.yml`
- `.github/workflows/runtime-retrieval-acl-security.yml`
- `.github/workflows/evidence-integrity.yml`
- `.github/workflows/portfolio-claim-boundary.yml`
- Multiple focused retrieval ACL workflow files for adapter, seam, shadow, monitor-only, and enforcement-harness tests.

## Relevant code paths found
- `security-layer-tests.yml` runs `python -m pytest backend/security_layer/tests -q` with minimal dependencies and explicitly states that passing tests do not prove production security.
- `security-readiness.yml` runs `PYTHONPATH=. pytest -q --confcutdir=backend/tests/security backend/tests/security` and validates security evidence files for paths matching the workflow trigger.
- Retrieval ACL focused workflows run specific isolated retrieval ACL tests and upload artifacts.
- Evidence and claim-boundary workflows run portfolio evidence/claim scripts.

## Findings
- CI workflow definitions exist for isolated security-layer tests, security demo attack tests, retrieval ACL focused tests, evidence integrity, and claim-boundary checks.
- Workflow comments repeatedly bound claims to isolated proof and explicitly avoid production/enterprise readiness claims.

## Gaps
- This review did not access remote GitHub Actions run status.
- Repository files do not prove CI passed for this branch.
- No CI workflow was found proving live staging, live Vespa/Postgres integration, external audit, or production deployment validation.

## Claim boundary
CI workflow definitions exist. CI pass status is not confirmed.
