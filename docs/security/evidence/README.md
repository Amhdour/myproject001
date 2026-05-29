# Security Baseline Evidence

This directory contains documentation/evidence artifacts for the clean baseline rebuild on branch `security-layer-mvp`.

Baseline evidence is stored under:
- `docs/security/evidence/baseline/`

These files are raw or near-raw command outputs intended to preserve an auditable chain for baseline validation.

## Step 34X Oracle Free VPS Coolify Staging

Step 34X evidence is stored under:
- `docs/security/evidence/step_34x_oracle_free_vps/`

This bundle records the validated VPS/Coolify/GitHub setup, the failed full-Onyx deployment at commit `a4012826cf06a2ecb859b932a9a14d2b7c44bbf1`, the resource-blocker decision for the Oracle Free Tier VPS class, and the repository-side minimal nginx compose target prepared for a future approved redeploy. No secrets or live minimal redeploy evidence are included.

## Step 36X Rollback/Redeploy Evidence Plan

Step 36X evidence is stored under:
- `docs/security/evidence/step_36x_rollback_redeploy/`

This bundle records the rollback/redeploy readiness plan for the previously validated Step 34X minimal live VPS staging deployment. Scope is limited to the minimal `step34x-health` nginx staging container and does not claim full Onyx rollback readiness, production readiness, enterprise readiness, or compliance certification.

Current status: **PLANNED / PENDING USER EXECUTION**. No real rollback/redeploy execution evidence has been provided in this repository update.
