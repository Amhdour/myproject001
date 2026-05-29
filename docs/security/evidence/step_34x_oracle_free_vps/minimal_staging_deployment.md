# Step 34X Minimal Staging Deployment

## Target

| Field | Value |
|---|---|
| Target compose file | `deployment/docker_compose/docker-compose.step34x-minimal.yml` |
| Coolify project | `rag-agent-security-minimal-staging` |
| Expected container | `step34x-health` |
| Expected port | `8088` |
| Expected public URL | `http://84.8.223.251:8088` |

## Expected health check

HTTP 200 or HTTP 301/302/304 is acceptable from the nginx root depending on response headers.

## Deployment result

**PENDING** until the user redeploys through Coolify.

## Evidence boundary

Codex prepared the repository-side minimal compose target only. Codex did not execute or validate a live Coolify redeploy in this update.
