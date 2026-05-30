# Deployment Attempt

## SSH/VPS Access Attempt

```text
$ ssh -o BatchMode=yes -o ConnectTimeout=8 rag-agent-security-staging-v2 'hostname; docker --version; docker compose version'
ssh: Could not resolve hostname rag-agent-security-staging-v2: Temporary failure in name resolution
```

```text
$ ssh -o BatchMode=yes -o ConnectTimeout=8 rag-agent-security-staging-v2 'hostname; docker ps --filter "network=lu8fgylyjp4so3adpxep8ixb" --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'
ssh: Could not resolve hostname rag-agent-security-staging-v2: Temporary failure in name resolution
EXIT:255
```

## Deployment Path Used

No deployment path was executed from this workspace. Coolify config update, compose override, and manual container replacement were all blocked by lack of direct VPS access and lack of a locally built custom image.

## User-Executable Deployment Template

If the operator has direct VPS access, use a cautious compose/Coolify update path rather than manual replacement where possible. Before running any destructive command, capture inventory and rollback evidence.

```bash
# On the Oracle VPS, from a trusted checkout of this repository at the desired commit:
git rev-parse HEAD
docker --version
docker compose version

docker ps --filter "network=lu8fgylyjp4so3adpxep8ixb" --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
docker image ls | sed -n '1,80p'

# Build the custom backend image on ARM64 host.
docker build -t rag-agent-security-onyx-backend:step52x-bf7212c -f backend/Dockerfile backend

# Prove image contains runtime code before deployment.
docker run --rm rag-agent-security-onyx-backend:step52x-bf7212c sh -c 'test -d /app/backend/security_layer/runtime_enforcement && echo FOUND || echo MISSING'
docker run --rm rag-agent-security-onyx-backend:step52x-bf7212c sh -c 'grep -R "_apply_step_39x_runtime_enforcement_hook" -n /app 2>/dev/null | head -20 || true'
```

Then update the Coolify/compose backend image for both `api_server` and `background` to `rag-agent-security-onyx-backend:step52x-bf7212c`, preserving volumes, environment, networks, database, Redis, OpenSearch/Vespa, MinIO, and web services. Do not replace data services unless explicitly necessary.

## Result

`PENDING_USER_EXECUTION`: no Oracle backend container replacement occurred from this environment.
