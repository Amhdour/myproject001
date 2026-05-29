# Step 37X Backup Evidence Plan

## Purpose

Step 37X defines backup evidence planning and backup-scope documentation for the Oracle VPS + Coolify minimal staging environment that was established and validated across the preceding staging steps.

The purpose of this bundle is to document what must be backed up, what evidence must be captured, what commands are safe to run, and what future restore drill must be completed before any backup or disaster recovery readiness claim can be made.

## Scope

This scope is limited to backup evidence planning for the minimal VPS/Coolify staging environment:

- VPS: `rag-agent-security-staging-v2`
- Provider: Oracle Cloud
- OS: Ubuntu 24.04.4 LTS ARM64
- Public IP: `84.8.223.251`
- Disk: approximately 193 GB
- Swap: 8 GiB active
- Coolify: 4.1.1
- Minimal app: `step34x-health` using `nginx:alpine`
- Binding: `0.0.0.0:8088->80/tcp`
- Local health check: `HTTP/1.1 200 OK`

## Dependencies

Step 37X depends on the prior evidence and status from:

- Step 34X: minimal live VPS staging evidence and full Onyx resource blocker.
- Step 35X: finalization of Step 34X evidence.
- Step 36X: minimal rollback/redeploy validation for `step34x-health` nginx.

## Current Status

- Step 37X repository status: **PLANNED / PARTIAL**.
- Backup scope documentation: **COMPLETE** in this repository update.
- Actual backup execution: **PENDING**.
- Restore drill execution: **PENDING**.

No real backup archive creation, off-server backup copy, Oracle boot volume backup, or restore drill is validated by this repository-only documentation update.

## Non-Claims

This bundle does not claim:

- Actual backup execution.
- Actual restore validation.
- Production backup readiness.
- Enterprise backup readiness.
- Disaster recovery readiness.
- Full Onyx backup readiness.
- Database restore readiness.
- RPO/RTO validation.
- External validation.
- Compliance certification.
