# Coolify Staging Rollback Plan

## Purpose
Define staging-only rollback expectations for a future real Coolify deployment.

## Rollback Triggers
- Staging application fails to start.
- Smoke tests fail.
- Unexpected runtime mode is enabled.
- Any evidence of live blocking or live filtering appears.
- Logs or evidence expose secrets or sensitive raw content.

## Rollback Steps
1. Stop routing staging test traffic to the changed staging revision.
2. Revert the Coolify staging application to the prior known staging image or
   branch revision.
3. Confirm runtime boundary flags remain false.
4. Re-run the smoke checks required to validate the restored staging revision.
5. Capture sanitized rollback evidence in the staging evidence bundle.

## Boundaries
- This rollback plan is staging-only.
- It does not authorize production rollout or production rollback activity.
- It does not enable enforce mode, shadow-deny runtime mode, live blocking, or
  live filtering.
