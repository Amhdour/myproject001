# Web Healthcheck Preservation

## Preserved Step 61X Patch

Step 62X preserves the Step 61X web healthcheck patch in:

- `deployment/docker_compose/docker-compose.coolify-staging.yml`
- `deployment/docker_compose/docker-compose.yml`

## Required Behavior

The web healthcheck includes the operational override `WEB_HEALTHCHECK_HOST` and a hostname-compatible service-local default:

```javascript
process.env.WEB_HEALTHCHECK_HOST || require('os').hostname()
```

## Unsafe Values Avoided

The durable architecture does not hardcode the old `10.0.3.11` diagnostic IP, the old one-time container hostname, or a fixed `127.0.0.1:3000` assumption for the web container healthcheck.

## Verification Boundary

The patch is preserved in repository configuration. Oracle VPS healthcheck retest remains pending unless a later redeploy/retest records evidence.
