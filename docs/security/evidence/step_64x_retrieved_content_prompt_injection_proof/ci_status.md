# Step 64X CI Status

| Field | Value |
|---|---|
| Date | 2026-06-07 |
| Command run | `.github/workflows/retrieved-content-prompt-injection-security.yml` was added; no GitHub-hosted Actions run URL is available in this workspace. |
| Exit code | Not available |
| Result | Focused CI workflow definition exists and is configured to run detector tests, demo attacks, evidence validation, and claim-boundary validation. |
| Limitation | CI pass is not claimed until a real GitHub Actions run completes and is linked. |
| Safe claim supported | CI workflow definition exists; CI success is not claimed. |

## Workflow commands

The workflow runs:

```bash
PYTHONPATH=. pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py backend/security_layer/tests/test_demo_attack_runner.py -q
python demo_attacks/run_demo_attacks.py
python scripts/security/validate_security_evidence.py
python scripts/portfolio/check_claim_boundary.py
python scripts/portfolio/check_no_fake_claims.py
python scripts/portfolio/check_evidence_links.py
```
