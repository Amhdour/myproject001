# Healthcheck Patch

## Files patched

- `deployment/docker_compose/docker-compose.coolify-staging.yml`
- `deployment/docker_compose/docker-compose.yml`

## Before

```javascript
require('http').get('http://127.0.0.1:3000/', (r) => process.exit(r.statusCode < 500 ? 0 : 1)).on('error', () => process.exit(1))
```

## After

```javascript
const http=require('http'),host=process.env.WEB_HEALTHCHECK_HOST||require('os').hostname();http.get('http://'+host+':3000/',(r)=>process.exit(r.statusCode<500?0:1)).on('error',()=>process.exit(1))
```

## Why this is stable across redeploys

- It does not hardcode a container IP.
- It does not hardcode a one-time container ID/hostname.
- It uses the current runtime hostname from inside the container.
- It allows an explicit `WEB_HEALTHCHECK_HOST` override if a future runtime requires a different service-local probe host.

## Expected behavior

The probe should succeed in the same class of environment where the web app responds by container hostname/IP. A real Oracle VPS retest is still required before marking the web Docker healthcheck as fixed.
