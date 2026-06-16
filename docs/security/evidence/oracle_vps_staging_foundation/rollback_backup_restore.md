# Oracle VPS Staging Foundation - Rollback, Backup, and Restore Evidence

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-ROLLBACK-BACKUP-RESTORE
- Step: Oracle VPS staging foundation
- Status: draft
- Environment: Oracle VPS staging
- Commit SHA: TBD
- Timestamp: TBD
- Operator: AI Trust & Security Readiness Engineer
- Redaction status: required before publication

## Purpose

Record whether the Oracle VPS staging foundation has a recoverability path before any staging go/no-go decision.

## Rollback Helper Command

Run from the staging directory on the Oracle VPS:

```bash
COMPOSE_FILE="compose.staging.yml" \
ENV_FILE=".env.staging" \
APP_SERVICE="app" \
PREVIOUS_IMAGE_TAG="ghcr.io/REPLACE_OWNER/REPLACE_IMAGE:previous" \
bash rollback_staging.sh
```

If no previous image exists yet, omit `PREVIOUS_IMAGE_TAG` and record image rollback as skipped:

```bash
COMPOSE_FILE="compose.staging.yml" \
ENV_FILE=".env.staging" \
APP_SERVICE="app" \
bash rollback_staging.sh
```

## Rollback Checks

| Check | Expected result | Actual result | Status |
|---|---|---|---|
| Compose file available | `compose.staging.yml` exists | TBD | pending |
| Env file available outside git | `.env.staging` exists on VPS only | TBD | pending |
| Docker Compose available | command exists | TBD | pending |
| Pre-rollback state captured | compose ps/config stored under backup directory | TBD | pending |
| Previous image identified | previous image tag recorded or skipped with reason | TBD | pending/skipped |
| Rollback command reviewed | manual rollback command recorded | TBD | pending |
| Post-rollback smoke test | `smoke_test_staging.sh` executed after rollback | TBD | pending |
| Rollback exit code | `0` for prechecks | TBD | pending |

## Backup/Restore Checklist

| Area | Minimum staging requirement | Actual result | Status |
|---|---|---|---|
| PostgreSQL backup | documented command for `pg_dump` or volume snapshot | TBD | pending |
| PostgreSQL restore | documented restore command tested on staging/synthetic data | TBD | pending |
| Qdrant backup | snapshot/export path documented | TBD | pending |
| Qdrant restore | restore path documented/tested with synthetic data | TBD | pending |
| Compose config backup | rendered config saved after redaction review | TBD | pending |
| Env backup | not committed; stored securely outside git | TBD | pending |
| Evidence redaction | logs/configs reviewed before publication | TBD | pending |

## Raw Rollback Output

Paste redacted output here:

```text
TBD
```

## Exit Code

```text
TBD
```

## Recovery Decision

- Recoverability status: TBD
- Blockers: TBD
- Required follow-up: TBD

## Non-Claim Statement

This evidence record covers staging recoverability planning and rollback-helper execution only. It does not prove production disaster recovery, enterprise resilience, compliance, live security enforcement, or production readiness.
