# Oracle VPS Staging Foundation Evidence Bundle

## Purpose

Index the evidence records for the Oracle VPS staging foundation step.

## Status

Draft. This bundle supports staging preparation only and does not claim enterprise readiness, production readiness, compliance, or runtime control effectiveness.

## Evidence Records

| Evidence ID | File | Purpose | Status |
|---|---|---|---|
| EVID-ORACLE-VPS-PREREQ | `prerequisite_check.md` | Confirm prerequisites before VPS staging work | draft |
| EVID-ORACLE-VPS-INVENTORY | `vps_inventory.md` | Record VPS inventory with redaction rules | draft |
| EVID-ORACLE-VPS-STACK | `open_source_stack_decision.md` | Record selected open-source stack and deferred stack | draft |
| EVID-ORACLE-VPS-BOUNDARY | `security_boundary_checklist.md` | Track security boundary requirements | draft |
| EVID-ORACLE-VPS-STAGING-PREP-VALIDATION | `staging_prep_validation.md` | Record validation command, output, and exit code | draft |
| EVID-ORACLE-VPS-SMOKE-TEST | `staging_smoke_test.md` | Record runtime foundation smoke-test output and exit code | draft |
| EVID-ORACLE-VPS-ROLLBACK-BACKUP-RESTORE | `rollback_backup_restore.md` | Record rollback helper output and backup/restore checklist | draft |
| EVID-ORACLE-VPS-GNG | `go_no_go.md` | Record staging foundation go/no-go decision | draft |

## Required Execution Before GO

1. Run `bash deploy/oracle-vps/validate_staging_prep.sh`.
2. Paste redacted output into `staging_prep_validation.md`.
3. Record VPS details in `vps_inventory.md` without secrets.
4. Complete `security_boundary_checklist.md`.
5. After staging services are copied and started on the VPS, run `bash smoke_test_staging.sh` from the staging directory.
6. Paste redacted output into `staging_smoke_test.md`.
7. Run `bash rollback_staging.sh` or record why rollback execution is skipped.
8. Complete `rollback_backup_restore.md`.
9. Complete `go_no_go.md`.

## Non-Claim Statement

This evidence bundle is for staging-foundation readiness only. It does not prove live deployment, live security enforcement, enterprise readiness, production readiness, or compliance.
