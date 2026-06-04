# Step 34X Smoke Tests

## Validated smoke-test evidence

| Check | Status | Evidence |
|---|---|---|
| Container running | **VALIDATED** | Minimal deployment container was `step34x-health`. |
| Container image | **VALIDATED** | Minimal deployment used `nginx:alpine`. |
| Container binding | **VALIDATED** | `0.0.0.0:8088->80/tcp`. |
| Local HTTP health | **VALIDATED** | `curl -I http://localhost:8088` returned `HTTP/1.1 200 OK`. |
| Local HTTP server header | **VALIDATED** | Health response included `Server: nginx/1.31.1`. |
| Public browser access | **VALIDATED WITH LIMITATION** | Public mobile browser access worked, but was slow. |
| Independent external validation | **PENDING** | No independent third-party validation is recorded as complete. |

## Commands recorded for validation

```bash
sudo docker ps
curl -I http://localhost:8088
```

The key recorded local response was:

```text
HTTP/1.1 200 OK
Server: nginx/1.31.1
```

## Public access note

Public mobile browser access to `http://84.8.223.251:8088` worked, but was slow. This is enough to record minimal public reachability for the nginx health container, but it is not enough to claim production-grade availability, latency, monitoring, failover, TLS, or external validation.

## Non-claims

- These smoke tests do not validate the full Onyx runtime.
- These smoke tests do not validate production readiness.
- These smoke tests do not validate enterprise readiness.
- These smoke tests do not validate compliance certification.
