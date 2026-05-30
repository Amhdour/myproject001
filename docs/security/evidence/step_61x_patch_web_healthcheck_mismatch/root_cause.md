# Root Cause

## Finding addressed

- Finding ID: `SIM-F-003`.
- Source type: simulated reviewer response / simulated finding, not real external validation.
- Scope: web Docker healthcheck mismatch only.

## Observed mismatch

Step 50X evidence showed:

| Probe | Result |
|---|---|
| API health after MinIO/file-store staging diagnostic fix | GO |
| Web app reachability by container hostname/IP | GO |
| Web Docker healthcheck | NOT GO |
| Host port `8000` | Redirects to `/login` |
| Host port `8088` | nginx `200 OK` |
| Host port `80` | `404` |

The Docker healthcheck command in the Coolify staging compose file targeted `http://127.0.0.1:3000/`. The Step 50X Oracle VPS evidence showed the web app responding by container hostname/IP while `127.0.0.1:3000` returned connection refusal.

## Repository source located

The matching healthcheck command was found in:

- `deployment/docker_compose/docker-compose.coolify-staging.yml`
- `deployment/docker_compose/docker-compose.yml`

## Root cause statement

The healthcheck was coupled to loopback (`127.0.0.1`) even though the Oracle staging web process was reachable on the container network identity. The healthcheck therefore reported NOT GO while the web application itself was reachable through container hostname/IP and host/proxy paths.
