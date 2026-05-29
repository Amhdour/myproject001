# Security Baseline Evidence

This directory contains documentation/evidence artifacts for the clean baseline rebuild on branch `security-layer-mvp`.

Baseline evidence is stored under:
- `docs/security/evidence/baseline/`

These files are raw or near-raw command outputs intended to preserve an auditable chain for baseline validation.

## Step 34X Oracle Free VPS Coolify Staging

Step 34X evidence is stored under:
- `docs/security/evidence/step_34x_oracle_free_vps/`

This bundle records the validated VPS/Coolify/GitHub setup, the failed full-Onyx deployment at commit `a4012826cf06a2ecb859b932a9a14d2b7c44bbf1`, the resource-blocker decision for the Oracle Free Tier VPS class, and the repository-side minimal nginx compose target prepared for a future approved redeploy. No secrets or live minimal redeploy evidence are included.

## Step 37X Backup Evidence Plan

Step 37X evidence is stored under:
- `docs/security/evidence/step_37x_backup_evidence/`

This bundle records backup scope, safe planned backup commands, Oracle boot volume backup evidence requirements, Coolify backup handling, a planned restore drill, limitations, and go/no-go status for the minimal Oracle VPS + Coolify staging environment. Minimal backup planning is complete, while actual backup execution and restore drill validation remain **PENDING**. Production backup readiness, enterprise backup readiness, disaster recovery readiness, and Full Onyx backup readiness remain **NO-GO**. External validation remains **PENDING** and compliance certification is **NOT CLAIMED**.
