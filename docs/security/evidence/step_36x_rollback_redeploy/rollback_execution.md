# Step 36X Rollback/Redeploy Execution Evidence

## Validation status

Step 36X rollback/redeploy evidence is **VALIDATED for the minimal `step34x-health` nginx deployment only**.

## Before-stop evidence

The VPS target was `rag-agent-security-staging-v2`. Before stopping the app resource through Coolify, the minimal app container was running with this observed state:

| Field | Evidence |
|---|---|
| Image | `nginx:alpine` |
| Container name prefix | `step34x-health` |
| Port binding | `0.0.0.0:8088->80/tcp` |
| Coolify containers | Healthy |

Local health check before stop returned:

```text
HTTP/1.1 200 OK
Server: nginx/1.31.1
```

## Stop evidence

After stopping the app resource through Coolify, this command was executed:

```bash
sudo docker ps -a | grep step34x-health || true
```

Result: no `step34x-health` output was returned.

Health check after stop:

```bash
curl -I http://localhost:8088 || true
```

Result:

```text
curl: (7) Failed to connect to localhost port 8088 after 0 ms: Couldn't connect to server
```

## Redeploy evidence

After redeploying through Coolify, this command was executed:

```bash
sudo docker ps
```

The result included:

| Field | Evidence |
|---|---|
| Container ID | `be0db257c549` |
| Image | `nginx:alpine` |
| Status | `Up` |
| Port binding | `0.0.0.0:8088->80/tcp` |
| Container name | `step34x-health-pdegb9g6obvbmmayzijiifjt-155959540822` |

Health check after redeploy:

```bash
curl -I http://localhost:8088
```

Result:

```text
HTTP/1.1 200 OK
Server: nginx/1.31.1
Content-Type: text/html
Content-Length: 896
```

## Boundary

This evidence validates only the minimal nginx rollback/redeploy path for `step34x-health`. It does not validate full Onyx rollback, database rollback, production rollback readiness, enterprise rollback readiness, external validation, or compliance certification.
