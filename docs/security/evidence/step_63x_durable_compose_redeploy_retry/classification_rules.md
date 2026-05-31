# Classification Rules

## Verified classification

Use `ORACLE_DURABLE_COMPOSE_REDEPLOY_VERIFIED` only when all of the following are true in the captured Step 63X output:

1. `api_server` and `background` containers are discovered and both inspect to the same intended durable backend image.
2. The API container contains `/app/backend/security_layer/runtime_enforcement`.
3. The API container contains `_apply_step_39x_runtime_enforcement_hook` in the deployed code path.
4. The in-container Step 39X runtime-enforcement pytest command passes, or an unavailable pytest environment is documented separately and replaced by equivalent runtime-code evidence.
5. MinIO is reachable on the `onyx_default` network and `onyx-file-store-bucket` is listed.
6. The web container health JSON is healthy, or the manual Node healthcheck returns `status=200`, `status=30x`, or another status lower than 500.
7. Host/proxy curl evidence shows expected HTTP reachability for the deployed staging route, or any proxy exception is documented as outside the Compose redeploy scope.
8. `docker ps` shows the relevant Onyx, MinIO, and proxy containers in expected running or healthy states.

## Partial GO / NO-GO classification

Use `ORACLE_DURABLE_COMPOSE_REDEPLOY_PARTIAL_GO_OR_NO_GO` if any required check fails, is missing, or has ambiguous output. Do not upgrade a partial result based on intent, operator recollection, or uncaptured terminal history.

## Unsupported claims

The Step 63X retry evidence does not by itself establish production readiness, enterprise production-candidate readiness, external validation completion, or compliance certification.
