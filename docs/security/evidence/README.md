# Security Baseline Evidence

This directory contains documentation/evidence artifacts for the clean baseline rebuild on branch `security-layer-mvp`.

Baseline evidence is stored under:
- `docs/security/evidence/baseline/`

These files are raw or near-raw command outputs intended to preserve an auditable chain for baseline validation.

## Step 34X Oracle Free VPS Coolify Staging

Step 34X evidence is stored under:
- `docs/security/evidence/step_34x_oracle_free_vps/`

This bundle records the validated VPS/Coolify/GitHub setup, the failed full-Onyx deployment at commit `a4012826cf06a2ecb859b932a9a14d2b7c44bbf1`, the resource-blocker decision for the Oracle Free Tier VPS class, and the repository-side minimal nginx compose target prepared for a future approved redeploy. No secrets or live minimal redeploy evidence are included.

## Step 36X Minimal Rollback/Redeploy Validation

Step 36X evidence is stored under:
- `docs/security/evidence/step_36x_rollback_redeploy/`

This bundle records real Coolify/VPS rollback and redeploy evidence for the minimal `step34x-health` nginx deployment on `rag-agent-security-staging-v2`. The minimal rollback/redeploy path is **VALIDATED** based on before-stop, after-stop, and after-redeploy local evidence. Full Onyx rollback is **NO-GO / RESOURCE-BLOCKED**, production rollback readiness is **NO-GO**, enterprise rollback readiness is **NO-GO**, external validation remains **PENDING**, and compliance certification is **NOT CLAIMED**.

## Step 64X Retrieved-Content Prompt-Injection Proof

Step 64X evidence is stored under:
- `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/`

This bundle records focused detector tests, bounded real search-runner hook wiring proof, synthetic demo attack output, redacted audit sample, telemetry sample, reviewer command output, CI workflow-definition status, and limitations. It supports only retrieved-content prompt-injection detection/protection claims covered by tests and demo evidence. It does not claim full prompt-injection defense, live blocking/filtering, production readiness, enterprise readiness, external validation, or compliance certification.
