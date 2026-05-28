# Real Coolify Staging Smoke Validation

## Current Status

Live staging validation status: **PENDING**.

No real Coolify staging deployment evidence is included in this repository change.

## Smoke Checks for a Real Staging Deployment

1. Confirm the staging application deploys the intended branch.
2. Confirm staging health checks return expected successful status through approved operator tooling.
3. Confirm a staging-only user can reach the frontend.
4. Confirm authentication works with staging-only credentials.
5. Confirm representative read-only pages load.
6. Confirm no enforce mode is enabled.
7. Confirm no shadow-deny runtime mode is enabled.
8. Confirm no live blocking or live filtering is enabled.
9. Confirm logs do not expose secrets in captured evidence.
10. Confirm any failures are recorded as sanitized summaries.

## Passing Criteria

A future run may mark live staging validation **PASSED** only when a real Coolify deployment was executed and each smoke check has sanitized evidence. Without that evidence, validation remains **PENDING**.
