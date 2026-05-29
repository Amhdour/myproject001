# Step 36X Rollback/Redeploy Evidence Plan

## Purpose

Step 36X documents rollback/redeploy readiness evidence requirements for the completed Step 34X minimal live VPS staging deployment and the Step 35X finalized evidence package.

## Scope

This bundle is scoped only to the minimal staging rollback/redeploy path for the `step34x-health` nginx container on the Oracle Ubuntu 22.04 ARM64 VPS at `84.8.223.251`.

## Out of scope

- Full Onyx rollback readiness.
- Production rollback readiness.
- Enterprise rollback readiness.
- Compliance certification.

## Dependencies

- Step 34X minimal live VPS staging evidence: Coolify installed and healthy, GitHub import validated, `step34x-health` minimal nginx deployment validated, and local health check returned `HTTP/1.1 200 OK`.
- Step 35X evidence finalization: prior evidence package finalized at commit `e798c7124ee463703145bceaa92e6e5135831d5a`.

## Current status

**PLANNED / PENDING USER EXECUTION.**

No repository evidence currently proves that a rollback/redeploy was executed for Step 36X. This package records the plan, required commands, required evidence, limitations, and go/no-go boundary for a future operator-executed rollback/redeploy test.
