# Step 38X Monitoring Baseline Evidence

## Purpose

Step 38X defines the monitoring baseline evidence plan for the Oracle VPS + Coolify minimal staging environment that was established after Step 34X minimal live VPS staging.

The purpose is to identify the minimum command outputs and operator artifacts needed to prove basic visibility into the host, Docker runtime, Coolify-managed minimal app, and backup/restore status before any later readiness claim can be considered.

## Scope

This bundle is limited to a **basic monitoring baseline for minimal staging** on the known Oracle Cloud VPS environment:

- VPS: `rag-agent-security-staging-v2`
- Provider: Oracle Cloud
- OS: Ubuntu 24.04.4 LTS ARM64
- Public IP: `84.8.223.251`
- Disk: about 193 GB
- Swap: 8 GiB active
- Coolify: 4.1.1
- Minimal app: `step34x-health` using `nginx:alpine`
- Binding: `0.0.0.0:8088->80/tcp`
- Known local health check: `HTTP/1.1 200 OK`

## Dependencies

Step 38X depends on the following prior work:

- Step 34X: minimal live Oracle VPS + Coolify staging evidence.
- Step 36X: minimal rollback/redeploy validation.
- Step 37X: backup plan completion, with actual backup/restore execution still pending.

## Current Status

Status: **PLANNED**.

No new live command output is included in this repository update. Monitoring execution remains **PENDING USER EXECUTION** until the operator captures and stores real outputs from the target VPS/Coolify environment.

## Non-Claims

This Step 38X bundle does **not** claim:

- Production monitoring readiness.
- Enterprise observability readiness.
- Alerting readiness.
- Uptime, SLO, or SLA readiness.
- External validation.
- Compliance certification.
- Full Onyx monitoring validation.
