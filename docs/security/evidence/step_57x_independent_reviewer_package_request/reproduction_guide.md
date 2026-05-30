# Safe Reproduction Guide

## Scope

These steps help an independent reviewer inspect and reproduce evidence safely without requiring secrets. VPS runtime reproduction requires controlled access from the owner and should not be attempted with public credentials.

## Steps

1. Checkout the repository branch or commit provided by the owner.
2. Inspect the Step 56X package at `docs/security/evidence/step_56x_external_validation_staging_review/`.
3. Inspect Step 50X–55X evidence references, especially:
   - `docs/security/evidence/step_50x_oracle_staging_evidence_healthcheck_decision/`
   - `docs/security/evidence/step_52x_custom_onyx_image_runtime_enforcement_deploy/`
   - `docs/security/evidence/step_56x_external_validation_staging_review/step_55x_behavior_summary.md`
4. If the local environment supports Python dependencies, run local Step 39X targeted tests from the repository root after activating the project environment if needed.
5. Verify evidence checker scripts, including claim-boundary and fake-claim checks.
6. Do not require Oracle secrets for repository-level review.
7. Do not publish raw environment values, cookie values, token values, SSH material, or provider credentials.
8. Treat VPS runtime reproduction as controlled-access work only. If granted access, capture only sanitized command summaries and redacted outputs.

## Suggested Local Checks

```bash
python scripts/portfolio/check_claim_boundary.py
python scripts/portfolio/check_no_fake_claims.py
python scripts/portfolio/check_evidence_links.py
python scripts/portfolio/check_release_candidate.py
python scripts/portfolio/check_step_50x_oracle_staging_evidence.py
python scripts/portfolio/check_step_52x_custom_image_evidence.py
python scripts/portfolio/check_step_57x_independent_review_package.py
```

## Secret-Safety Rules

- Do not paste raw `.env` files into reviewer notes.
- Do not include raw session cookies or request headers.
- Do not include private SSH material.
- Do not include raw cloud provider credentials.
- Use synthetic data for smoke tests where possible.
