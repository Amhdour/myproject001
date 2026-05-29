# Step 37X Restore Drill Plan

## Status

- Restore drill status: **PENDING**.
- Restore validation status: **not validated**.

This plan documents the required restore drill but does not claim restore success.

## Planned Restore Drill

1. Create a new VM.
2. Install Docker.
3. Install or restore Coolify.
4. Restore Coolify data/config from the approved backup source.
5. Restore required secrets from a password manager or secret manager without committing values to git.
6. Reconnect the GitHub App or repository integration if needed.
7. Redeploy `step34x-health` using the minimal nginx deployment configuration.
8. Run the local health check:

   ```bash
   curl -I http://localhost:8088
   ```

9. Record success or failure in sanitized evidence.
10. If successful, update go/no-go status with exact timestamp, target VM identity, and command output.

## Required Evidence After Future Execution

- New VM identity, with sensitive identifiers redacted as needed.
- Docker and Coolify install status.
- Restore source description without secrets.
- `step34x-health` deployment status.
- `curl -I http://localhost:8088` output.
- Clear pass/fail result.

## Non-Claim

No restore drill was executed or validated as part of this repository-only Step 37X update.
