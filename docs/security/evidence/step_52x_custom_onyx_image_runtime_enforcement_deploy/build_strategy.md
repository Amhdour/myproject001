# Build Strategy

## Dockerfile and Compose Discovery

```text
$ find . -maxdepth 5 -iname "Dockerfile*" -o -iname "*dockerfile*" | sort
./.devcontainer/Dockerfile
./backend/Dockerfile
./backend/Dockerfile.model_server
./backend/tests/integration/Dockerfile
./cli/Dockerfile
./web/Dockerfile
./web/node_modules/linguist-languages/data/Dockerfile.d.ts
./web/node_modules/linguist-languages/data/Dockerfile.js
./web/node_modules/ts-unused-exports/Dockerfile
$ find . -maxdepth 6 -path "*backend*" -iname "Dockerfile*" | sort
./backend/Dockerfile
./backend/Dockerfile.model_server
./backend/tests/integration/Dockerfile
./backend/tests/integration/mock_services/mock_connector_server/Dockerfile
$ find . -maxdepth 5 -iname "*compose*.yml" -o -iname "*compose*.yaml" | sort
./backend/tests/integration/mock_services/docker-compose.mock-it-services.yml
./deployment/docker_compose/docker-compose.coolify-staging.yml
./deployment/docker_compose/docker-compose.craft.yml
./deployment/docker_compose/docker-compose.dev.yml
./deployment/docker_compose/docker-compose.mcp-api-key-test.yml
./deployment/docker_compose/docker-compose.mcp-oauth-test.yml
./deployment/docker_compose/docker-compose.mcp-per-user-key-test.yml
./deployment/docker_compose/docker-compose.multitenant-dev.yml
./deployment/docker_compose/docker-compose.onyx-lite.yml
./deployment/docker_compose/docker-compose.prod-cloud.yml
./deployment/docker_compose/docker-compose.prod-no-letsencrypt.yml
./deployment/docker_compose/docker-compose.prod.yml
./deployment/docker_compose/docker-compose.resources.yml
./deployment/docker_compose/docker-compose.search-testing.yml
./deployment/docker_compose/docker-compose.step34x-minimal.yml
./deployment/docker_compose/docker-compose.yml
./profiling/docker-compose.yml
$ find deployment -maxdepth 5 -type f 2>/dev/null | sort || true
[deployment compose, nginx, AWS ECS, and Helm files were found; no secrets were printed]
$ grep -R "onyxdotapp/onyx-backend\|api_server\|background\|build:" -n deployment docker-compose* . 2>/dev/null | head -200
[backend services reference onyxdotapp/onyx-backend and build with context ../../backend and dockerfile Dockerfile]
```

## Selected Path

`Path D — Build blocked` for this execution environment.

Reason: a clear backend Dockerfile exists (`backend/Dockerfile`), and compose files can build backend services from it, but this workspace has no Docker CLI or Docker Compose. Therefore the image could not be built or runtime-checked locally. Direct Oracle deployment also could not proceed because SSH hostname resolution failed.

## Dockerfile Inclusion Fix

`backend/Dockerfile` was updated to copy the repository-local security-layer package into the backend image:

```dockerfile
COPY --chown=onyx:onyx ./security_layer /app/backend/security_layer
```

This makes the expected image path `/app/backend/security_layer/runtime_enforcement` available when a backend image is successfully built from the repository Dockerfile. `backend/.dockerignore` was added for the backend build context and excludes `.env`, env-like files, caches, logs, private-key-like filename patterns, and common secret files.

## Intended Build Command When Docker Is Available

```bash
docker build -t rag-agent-security-onyx-backend:step52x-bf7212c -f backend/Dockerfile backend
```

For the Oracle ARM64 host, build on the VPS directly or use a trusted multi-architecture builder targeting `linux/arm64`. Do not push to a public registry with secrets. Do not embed `.env` or private keys in the image.
