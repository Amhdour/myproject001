# Step 34X Oracle Free VPS Coolify Staging Deployment Run

## Deployment metadata

| Field | Value |
|---|---|
| Repository | `Amhdour/myproject001` |
| Branch | `main` |
| Commit | `353ee0127ed826e8b139aa4f264e3477143b007c` |
| Compose path used | `deployment/docker_compose/docker-compose.yml` |
| Deployment result | **BLOCKED** |
| Blocker | Docker Compose build context path resolved outside repository |
| Error | `unable to prepare context: path "/backend" not found` |

## Access and integration status

| Check | Status |
|---|---|
| VPS access | **VALIDATED** |
| Coolify install | **VALIDATED** |
| Coolify dashboard access | **VALIDATED** |
| GitHub App integration | **VALIDATED** |
| Repository import | **VALIDATED** |

## Blocker details

Coolify ran Docker Compose with the repository root as the project directory while using `deployment/docker_compose/docker-compose.yml`. The base compose file contains relative build contexts such as `../../backend` and `../../web`. Under the Coolify project-directory behavior, those paths resolved outside the checked-out repository, causing Docker to fail before service startup.

## Repository fix prepared

A Coolify-specific staging compose file was added at `deployment/docker_compose/docker-compose.coolify-staging.yml`. It is based on the existing compose file but removes service-level `build:` blocks so Coolify uses the declared prebuilt images instead of attempting local image builds from relative contexts.

## Follow-up minimal deployment status

A later Step 34X minimal deployment was validated separately with `deployment/docker_compose/docker-compose.step34x-minimal.yml`, the `nginx:alpine` `step34x-health` container, binding `0.0.0.0:8088->80/tcp`, and a local `HTTP/1.1 200 OK` nginx health response. This earlier deployment-run record is retained to document the original full-stack blocker and does not claim that the full Onyx stack became production-ready.
