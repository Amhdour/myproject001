# Rollback Plan

## Scope

This rollback plan covers only the Step 61X web healthcheck command change.

## Git rollback

Revert the Step 61X commit or restore these files to their prior healthcheck command:

- `deployment/docker_compose/docker-compose.coolify-staging.yml`
- `deployment/docker_compose/docker-compose.yml`

Prior command:

```javascript
require('http').get('http://127.0.0.1:3000/', (r) => process.exit(r.statusCode < 500 ? 0 : 1)).on('error', () => process.exit(1))
```

## Operational rollback on Oracle VPS

1. Redeploy the previous compose configuration through the same Coolify/redeploy path.
2. Confirm the effective healthcheck command with:

```bash
WEB_CONTAINER=$(docker ps --format '{{.Names}}' | grep -m1 'web_server')
docker inspect "$WEB_CONTAINER" --format '{{json .Config.Healthcheck.Test}}'
```

3. Re-check API, web reachability, and host/proxy behavior.
4. Keep the classification at PARTIAL GO or lower unless a new retest provides stronger evidence.

## Claim boundary after rollback

Rollback would return SIM-F-003 to an unresolved state. Do not claim web Docker healthcheck GO after rollback unless separate evidence proves a different durable fix.
