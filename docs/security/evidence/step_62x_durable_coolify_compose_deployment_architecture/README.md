# Step 62X — Durable Coolify/Compose Deployment Architecture

## Purpose

Step 62X creates a durable, reproducible Coolify/Compose deployment architecture for Oracle staging so the prior diagnostic deployment work is expressed as repeatable configuration and operator runbooks.

## Classification

`DURABLE_DEPLOYMENT_ARCHITECTURE_READY_RETEST_PENDING`

## Simulated Finding Addressed

This package addresses simulated finding `SIM-F-004`: diagnostic deployment not durable. The finding and remediation context remain simulated reviewer material; no real external validation is claimed.

## Scope Boundary

This is architecture/configuration readiness. It is not verified redeploy evidence unless an Oracle VPS redeploy/retest is actually executed and recorded in a later evidence package.

## Readiness Boundary

| Item | Status |
|---|---|
| Production-style portfolio readiness | historical readiness snapshot |
| Enterprise production-candidate | NO-GO |
| External validation | simulated response only / real validation pending |
| Compliance certification | NOT CLAIMED |

## Evidence Files

- `current_diagnostic_gap.md`
- `architecture_decision.md`
- `compose_changes.md`
- `minio_durable_service.md`
- `custom_backend_image_strategy.md`
- `web_healthcheck_preservation.md`
- `oracle_vps_redeploy_plan.md`
- `retest_checklist.md`
- `rollback_plan.md`
- `go_no_go.md`
- `remaining_limitations.md`
- `redaction_note.md`
