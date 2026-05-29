# Step 36X Rollback/Redeploy Plan

## Preconditions

Before executing the rollback/redeploy test, confirm:

- Coolify is running.
- The `step34x-health` container is running.
- The local health check returns `HTTP/1.1 200 OK` from `curl -I http://localhost:8088`.

## Rollback test plan

1. Capture the current `docker ps` output.
2. Stop the app resource through Coolify.
3. Confirm the `step34x-health` container stops.
4. Redeploy the app through Coolify.
5. Confirm a new `step34x-health` container is running.
6. Run `curl -I http://localhost:8088`.
7. Record deployment logs from Coolify.

## Acceptance criteria

- The container restarts successfully.
- The `0.0.0.0:8088->80/tcp` port binding is restored.
- The local health check returns `HTTP/1.1 200 OK`.
- No secret values are exposed in screenshots, logs, command output, or committed evidence.

## Claim boundary

Until the above evidence is captured, minimal rollback/redeploy readiness remains **PENDING**. This plan does not claim full Onyx rollback readiness, production rollback readiness, enterprise rollback readiness, external validation, or compliance certification.
