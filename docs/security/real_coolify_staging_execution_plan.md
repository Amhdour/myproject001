# Real Coolify Staging Execution Plan

## Purpose

Step 32X prepares the real Coolify staging execution bundle from the current work branch while preserving the existing safety boundary. This document is an execution plan and evidence index; it is not proof that a real deployment occurred.

## Required Branch

`real-coolify-staging-execution-bundle`

## Current Execution Status

- Real Coolify deployment executed: **no**.
- Live staging validation status: **PENDING**.
- Partner-demo evidence review decision: **GO**.
- Production readiness decision: **NO-GO**.
- Enterprise production readiness decision: **NO-GO**.
- External validation status: **PENDING**.
- Compliance certification status: **NOT CLAIMED**.

## Prerequisites

1. Confirm the repository branch is `real-coolify-staging-execution-bundle`.
2. Confirm Step 29X Coolify staging preparation docs exist.
3. Confirm Step 31X final partner-demo go/no-go remains partner-demo only.
4. Confirm no secrets, domains, IPs, credentials, tokens, SSH keys, API keys, or private keys are committed.
5. Confirm any real Coolify credentials, staging domains, and deployment variables are handled outside the repository by an approved operator.

## Execution Sequence for an Approved Operator

1. Review this plan and the operator runbook.
2. Prepare Coolify staging configuration using out-of-band secret management only.
3. Deploy the current branch to a staging-only Coolify application.
4. Run the smoke validation checklist.
5. Capture sanitized evidence using the evidence capture template.
6. Record only redacted summaries in `docs/security/evidence/real_coolify_staging_execution_bundle/`.
7. Keep production readiness at **NO-GO** regardless of staging outcome until separate production gates are approved.

## Safety Boundary

- Do not enable enforce mode.
- Do not enable shadow-deny runtime mode.
- Do not add live blocking.
- Do not add live filtering.
- Do not change application behavior.
- Do not claim production readiness, enterprise production readiness, external validation, or compliance certification.
