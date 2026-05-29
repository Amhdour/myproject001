# Security Baseline Evidence

This directory contains documentation/evidence artifacts for the clean baseline rebuild on branch `security-layer-mvp`.

Baseline evidence is stored under:
- `docs/security/evidence/baseline/`

These files are raw or near-raw command outputs intended to preserve an auditable chain for baseline validation.

## Step 34X Oracle Free VPS Coolify Staging

Step 34X evidence is stored under:
- `docs/security/evidence/step_34x_oracle_free_vps/`

This bundle records the validated VPS/Coolify/GitHub setup, the failed full-Onyx deployment at commit `a4012826cf06a2ecb859b932a9a14d2b7c44bbf1`, the resource-blocker decision for the Oracle Free Tier VPS class, and the repository-side minimal nginx compose target prepared for a future approved redeploy. No secrets or live minimal redeploy evidence are included.

## Step 38X Monitoring Baseline Evidence

Step 38X monitoring baseline evidence is stored under:
- `docs/security/evidence/step_38x_monitoring_baseline/`

This bundle defines the basic monitoring baseline plan for the Oracle VPS + Coolify minimal staging environment. It covers planned host, Docker, Coolify, minimal app health, optional public endpoint, deployment log, and Step 37X backup/restore status evidence.

Status: **MONITORING PLAN COMPLETE / EXECUTION PENDING**. No real monitoring command output is included in this repository update. Production monitoring readiness is **NO-GO**, Enterprise observability readiness is **NO-GO**, Alerting readiness is **NO-GO**, SLO/SLA readiness is **NO-GO**, External validation is **PENDING**, and Compliance certification is **NOT CLAIMED**.
