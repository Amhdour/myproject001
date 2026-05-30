# Oracle VPS Test Plan

## Status

`PENDING_USER_EXECUTION`

Codex does not have access to the Oracle VPS in this repository execution environment. Run the commands below on the Oracle staging host after deploying the Step 61X compose patch.

## Pre-deploy baseline capture

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | sed -n '1,80p'
docker inspect --format '{{.Name}} {{json .Config.Healthcheck}}' $(docker ps -q --filter name=web_server) 2>/dev/null
```

## Deploy patched compose through the existing Coolify/redeploy path

Use the same Coolify or compose deployment workflow used for the current Oracle staging stack. Do not manually edit the generated runtime container in a way that hides whether the repository patch works.

## Verify effective healthcheck source

```bash
WEB_CONTAINER=$(docker ps --format '{{.Names}}' | grep -m1 'web_server')
docker inspect "$WEB_CONTAINER" --format '{{json .Config.Healthcheck.Test}}'
```

Expected: the test contains `require('os').hostname()` or the equivalent deployed Step 61X healthcheck command, not the old hardcoded `http://127.0.0.1:3000/` command.

## Verify in-container probe behavior

```bash
WEB_CONTAINER=$(docker ps --format '{{.Names}}' | grep -m1 'web_server')
docker exec "$WEB_CONTAINER" node -e "const http=require('http'),host=process.env.WEB_HEALTHCHECK_HOST||require('os').hostname(); console.log('target='+host); http.get('http://'+host+':3000/', r => { console.log('status='+r.statusCode); process.exit(r.statusCode < 500 ? 0 : 1); }).on('error', e => { console.error(e); process.exit(1); })"
```

Expected: exit code `0` and HTTP status below `500`.

## Verify Docker health becomes healthy

```bash
WEB_CONTAINER=$(docker ps --format '{{.Names}}' | grep -m1 'web_server')
for i in $(seq 1 12); do
  docker inspect "$WEB_CONTAINER" --format '{{.State.Health.Status}} {{range .State.Health.Log}}{{.ExitCode}}:{{.Output}}{{end}}'
  sleep 10
done
```

Expected: `healthy` after the healthcheck interval/start period allows Docker to run the patched probe.

## Verify host/proxy checks still pass

```bash
curl -sS -I http://127.0.0.1:8000/ | sed -n '1,20p'
curl -sS -I http://127.0.0.1:8088/ | sed -n '1,20p'
curl -sS -I http://127.0.0.1:80/ | sed -n '1,20p'
```

Expected based on current evidence: port `8000` still redirects to `/login`, port `8088` still returns nginx `200 OK`, and port `80` behavior is recorded without converting it into a full staging GO claim.

## Evidence to paste into `test_results.md`

- Effective healthcheck command after redeploy.
- In-container patched probe output and exit code.
- Docker health status loop output.
- Host/proxy curl headers.
- Any relevant web container logs with secrets redacted.
