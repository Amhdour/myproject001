# Coolify Staging Deployment Plan

## Purpose
Prepare a staging-only deployment evidence bundle for Step 29X without enabling
enforce mode, shadow-deny runtime mode, live blocking, live filtering, or any
application behavior change.

## Scope
- Target environment: Coolify-managed staging environment using placeholder
  configuration values only.
- Evidence folder: `docs/security/evidence/coolify_staging_evidence_bundle/`.
- Helper scope: isolated models and checklist helpers under
  `backend/security_layer/staging/`.

## Prerequisites
1. Confirm the work branch is `coolify-staging-evidence-bundle`.
2. Confirm the required staging docs, helper package, tests, and evidence folder
   exist.
3. Confirm no real domains, IPs, credentials, tokens, private keys, or secrets
   are committed.
4. Confirm any real Coolify execution is performed only by an approved operator
   with out-of-band secrets management.

## Deployment Sequence
1. Review the environment template and replace placeholders outside the
   repository in the approved Coolify secret store.
2. Deploy the current branch to a staging-only Coolify application.
3. Run the staging smoke test plan against the staging URL kept outside the
   repository.
4. Capture sanitized evidence summaries only; never paste secrets, private
   endpoint details, or tokens into evidence files.
5. Keep live staging validation marked pending if no real deployment occurred.

## Safety Boundaries
- Enforce mode remains disabled.
- Shadow-deny runtime mode remains disabled.
- Live blocking and live filtering remain disabled.
- No production traffic is routed to the staging deployment.
- No production-readiness claim is made by this plan.

## Current Step 29X State
No real Coolify deployment was executed as part of this repository change. Live
staging validation is therefore pending.
