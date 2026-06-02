# Oracle VPS Staging Foundation - Staging Prep Validation

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-STAGING-PREP-VALIDATION
- Step: Oracle VPS staging foundation
- Status: draft
- Environment: local, CI, or Oracle VPS staging
- Commit SHA: TBD
- Timestamp: TBD
- Operator: AI Trust & Security Readiness Engineer
- Redaction status: required before publication

## Validation Command

```bash
bash deploy/oracle-vps/validate_staging_prep.sh
```

## CI Validation

Workflow:

```text
.github/workflows/oracle-vps-staging-prep.yml
```

Expected CI artifact:

```text
oracle-vps-staging-prep-evidence
```

The CI workflow validates staging-prep file consistency and renders the Docker Compose example into an artifact for review.

## Expected Checks

| Check | Expected result | Actual result | Status |
|---|---|---|---|
| Required deployment-prep files exist | all required files present | TBD | pending |
| Common secret patterns absent | no obvious private keys/tokens found | TBD | pending |
| Raw IPv4-like values absent or reviewed | no live public IP published | TBD | pending |
| Docker Compose syntax validation | compose renders with example env when Docker is available | TBD | pending |
| CI workflow present | `.github/workflows/oracle-vps-staging-prep.yml` exists | present | complete |
| Rendered compose artifact | artifact uploaded by CI | TBD | pending |
| Script exit code | `0` when all required checks pass | TBD | pending |

## Raw Output

Paste redacted output here after execution:

```text
TBD
```

## Exit Code

```text
TBD
```

## Interpretation

- PASS means deployment-prep files are internally consistent and public-safe enough for the next staging step.
- SKIP for Docker Compose syntax is acceptable only when Docker Compose is unavailable in the execution environment.
- FAIL blocks the staging foundation go/no-go until remediated.
- CI pass means the staging-prep validation is repeatable in GitHub Actions, but still does not prove live deployment.

## Non-Claim Statement

This validation proves only staging-prep file consistency and CI repeatability. It does not prove live deployment, runtime enforcement, security-control effectiveness, enterprise readiness, production readiness, or compliance.
