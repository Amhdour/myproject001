# Oracle VPS Staging Foundation - Staging Prep Validation

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-STAGING-PREP-VALIDATION
- Step: Oracle VPS staging foundation
- Status: CI validation passed
- Environment: GitHub Actions
- Commit SHA: `755e61658de76a7356fcfa1e163705f40752a29c`
- Timestamp: 2026-06-02T19:00:04Z
- Operator: AI Trust & Security Readiness Engineer
- Redaction status: artifact requires review before publication

## Validation Command

```bash
bash deploy/oracle-vps/validate_staging_prep.sh
```

## CI Validation

Workflow:

```text
.github/workflows/oracle-vps-staging-prep.yml
```

Workflow run:

```text
Oracle VPS Staging Prep Validation / run 28 / success
```

Expected CI artifact:

```text
oracle-vps-staging-prep-evidence
```

Artifact record:

```text
artifact id: 7367151385
artifact digest: sha256:721f37fc099915864de3c57908a442a957cad1a1c2ef3041398962117970a533
created_at: 2026-06-02T19:00:04Z
expires_at: 2026-06-16T19:00:04Z
```

The CI workflow validates staging-prep file consistency and renders the Docker Compose example into an artifact for review.

## Expected Checks

| Check | Expected result | Actual result | Status |
|---|---|---|---|
| Required deployment-prep files exist | all required files present | CI passed | complete |
| Common secret patterns absent | no obvious private keys/tokens found | CI passed | complete |
| Raw IPv4-like values absent or reviewed | no live public IP published | CI passed | complete |
| Docker Compose syntax validation | compose renders with example env when Docker is available | CI passed | complete |
| CI workflow present | `.github/workflows/oracle-vps-staging-prep.yml` exists | present | complete |
| Rendered compose artifact | artifact uploaded by CI | artifact `7367151385` | complete |
| Script exit code | `0` when all required checks pass | CI success | complete |

## Raw Output

Raw CI logs and artifact are retained in GitHub Actions for the workflow run. Do not paste full logs here unless redacted.

```text
See GitHub Actions workflow run 26841540765 and artifact 7367151385.
```

## Exit Code

```text
0 via successful GitHub Actions job conclusion
```

## Interpretation

- PASS means deployment-prep files are internally consistent and public-safe enough for the next staging step.
- CI pass means the staging-prep validation is repeatable in GitHub Actions.
- Artifact presence confirms the rendered compose evidence was produced.
- This still does not prove live deployment.

## Non-Claim Statement

This validation proves only staging-prep file consistency and CI repeatability. It does not prove live deployment, runtime enforcement, security-control effectiveness, enterprise readiness, production readiness, or compliance.
