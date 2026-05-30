# Runtime Hook Verification

## Source-Level Hook Evidence

The repository source contains `_apply_step_39x_runtime_enforcement_hook` in `backend/onyx/context/search/retrieval/search_runner.py`, and the runtime enforcement modules exist under `backend/security_layer/runtime_enforcement`.

## Deployed-Container Hook Evidence

`NOT VERIFIED`: the hook was not verified inside an Oracle VPS API container in Step 52X because build and deployment were blocked.

## Required Passing Evidence Before Claiming Oracle Runtime Code Present

A future update may classify `ORACLE_CUSTOM_IMAGE_DEPLOYED_RUNTIME_CODE_PRESENT` only after all of the following are captured from the deployed Oracle API container:

- `docker inspect "$API_CONTAINER" --format '{{.Config.Image}}'` returns the custom backend image tag.
- `docker exec "$API_CONTAINER" sh -c 'test -d /app/backend/security_layer/runtime_enforcement && echo FOUND || echo MISSING'` returns `FOUND`.
- `docker exec "$API_CONTAINER" sh -c 'grep -R "_apply_step_39x_runtime_enforcement_hook" -n /app 2>/dev/null | head -20 || true'` finds the hook.
- Runtime-enforcement module import checks pass or any failures are documented without overclaiming active enforcement behavior.
