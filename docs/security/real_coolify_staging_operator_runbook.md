# Real Coolify Staging Operator Runbook

## Scope

This runbook is for a staging-only Coolify operator. It intentionally omits real domains, IP addresses, credentials, tokens, SSH keys, API keys, private keys, and secret values.

## Operator Responsibilities

- Use the required branch: `real-coolify-staging-execution-bundle`.
- Use out-of-band secret storage for all Coolify variables.
- Deploy only to a staging application.
- Keep production traffic out of scope.
- Capture sanitized evidence only.

## Pre-Deployment Checks

1. Confirm the branch and commit to deploy.
2. Confirm staging application isolation.
3. Confirm placeholders are replaced only in the approved Coolify secret store.
4. Confirm no enforce-mode or shadow-deny runtime activation variables are enabled.
5. Confirm rollback access is available before deployment.

## Deployment Steps

1. Trigger a staging-only deployment in Coolify.
2. Wait for the deployment to finish.
3. Confirm service health through staging-only operator tooling.
4. Run smoke validation steps.
5. Record sanitized deployment status in the evidence template.

## Stop Conditions

Stop and mark validation **PENDING** or **NO-GO** if any of the following occur:

- A production route or production dataset is in scope.
- A secret would need to be pasted into the repository.
- Enforce mode, shadow-deny runtime mode, live blocking, or live filtering would be enabled.
- Application behavior would change beyond staging deployment execution.
- Evidence cannot be sanitized.
