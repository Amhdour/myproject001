# Deployed Container Verification

## Status

`NOT VERIFIED`: no deployed Oracle container verification could be executed from this workspace because SSH hostname resolution failed and no image was deployed.

## Required Commands for Post-Deploy Evidence

Use dynamic discovery; do not hardcode old container IDs.

```bash
docker ps --filter "network=lu8fgylyjp4so3adpxep8ixb" --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
API_CONTAINER=$(docker ps --filter "network=lu8fgylyjp4so3adpxep8ixb" --format "{{.Names}}" | grep '^api_server' | head -1); echo "$API_CONTAINER"
BACKGROUND_CONTAINER=$(docker ps --filter "network=lu8fgylyjp4so3adpxep8ixb" --format "{{.Names}}" | grep '^background' | head -1); echo "$BACKGROUND_CONTAINER"
docker inspect "$API_CONTAINER" --format '{{.Config.Image}}'
docker exec "$API_CONTAINER" sh -c 'test -d /app/backend/security_layer/runtime_enforcement && echo FOUND || echo MISSING'
docker exec "$API_CONTAINER" sh -c 'grep -R "_apply_step_39x_runtime_enforcement_hook" -n /app 2>/dev/null | head -20 || true'
docker exec "$API_CONTAINER" sh -c 'find /app -path "*runtime_enforcement*" 2>/dev/null | head -50'
docker inspect "$API_CONTAINER" --format '{{json .Config.Env}}' | jq -r '.[] | select(test("SOURCE_COMMIT|COOLIFY_BRANCH|STEP_39X|RUNTIME|ENFORCEMENT"))'
docker logs --tail=150 "$API_CONTAINER"
docker logs --tail=120 "$BACKGROUND_CONTAINER"
```

## Current Deployed API Image Result

Unknown from this workspace. Based on Step 51X, assume the upstream `onyxdotapp/onyx-backend:latest` image remains deployed until this file is replaced with VPS evidence proving the custom image is running.
