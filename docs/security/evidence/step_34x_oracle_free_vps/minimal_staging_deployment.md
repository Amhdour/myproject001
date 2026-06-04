# Step 34X Minimal Staging Deployment

## Deployment target and result

| Field | Value |
|---|---|
| Target compose file | `deployment/docker_compose/docker-compose.step34x-minimal.yml` |
| Coolify project | `rag-agent-security-minimal-staging` |
| Deployment status | **VALIDATED** |
| Container name | `step34x-health` |
| Container image | `nginx:alpine` |
| Container binding | `0.0.0.0:8088->80/tcp` |
| Local health URL | `http://localhost:8088` |
| Public URL | `http://84.8.223.251:8088` |

## Health evidence

The local health check was validated with:

```bash
curl -I http://localhost:8088
```

Recorded result:

```text
HTTP/1.1 200 OK
Server: nginx/1.31.1
```

Public mobile browser access to `http://84.8.223.251:8088` also worked, but was slow.

## What this proves

- The Oracle Ubuntu 22.04 ARM64 VPS can run Coolify.
- Coolify can import the GitHub repository.
- Coolify can run the minimal `nginx:alpine` deployment.
- The minimal health container can bind `8088` publicly on the host.
- The host can serve a basic HTTP health response from the minimal container.

## What this does not prove

- It does not prove full Onyx runtime readiness.
- It does not prove production readiness.
- It does not prove enterprise readiness.
- It does not prove compliance certification.
- It does not prove independent external validation beyond the reported public mobile browser access.
