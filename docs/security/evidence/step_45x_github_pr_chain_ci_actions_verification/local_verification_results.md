# Step 45X Local Verification Results

## Results

| Command | Result | Notes |
|---|---|---|
| `python -m pytest backend/security_layer/tests/test_step_39x_runtime_enforcement.py -q` | PASS | `6 passed, 12 warnings` with system Python. The venv lacked pytest, so exact command was rerun without venv and passed. |
| `python -m pytest backend/security_layer/tests -q` | PASS | `274 passed, 8 skipped, 288 warnings` with system Python. The venv lacked pytest, so exact command was rerun without venv and passed. |
| `python demo_attacks/run_demo_attacks.py` | PASS | Synthetic demo attacks passed. |
| `python scripts/portfolio/check_claim_boundary.py` | PASS | No unsafe positive readiness claims found. |
| `python scripts/portfolio/check_no_fake_claims.py` | PASS | No unsupported positive evidence claims found. |
| `python scripts/portfolio/check_evidence_links.py` | PASS | Required reviewer evidence files present. |
| `python scripts/portfolio/check_release_candidate.py` | PASS | Required release-candidate files present. |
| `python scripts/portfolio/check_step_42x_staging_evidence.py` | PASS | Step 42X evidence package complete and blocked-deployment boundaries present. |
| `python scripts/portfolio/check_step_43x_github_sync_evidence.py` | PASS | Step 43X evidence package complete with PR/CI unavailable boundaries. |
| `python scripts/portfolio/check_step_44x_repository_recovery_evidence.py` | PASS | Step 44X evidence package complete with repository recovery blocked boundaries. |
| `python scripts/portfolio/check_step_45x_pr_chain_ci_evidence.py` | PASS | Step 45X evidence package and claim-boundary checks passed. |
| `git diff --check` | PASS | No whitespace errors reported. |

## Dependency note

Following repository guidance, the virtual environment was tried for pytest first. It failed with `No module named pytest`. The exact requested pytest commands were then run with the default Python environment and passed.

## Boundary

Passing local verification does not prove GitHub Actions success, production readiness, live staging/cloud validation, external validation, compliance certification, full Onyx-wide enforcement, or customer deployment.
