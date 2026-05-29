# Step 36X Rollback/Redeploy Commands

## Before-stop health check

```bash
curl -I http://localhost:8088
```

Observed result included:

```text
HTTP/1.1 200 OK
Server: nginx/1.31.1
```

## Stop verification

```bash
sudo docker ps -a | grep step34x-health || true
```

Observed result: no `step34x-health` output.

```bash
curl -I http://localhost:8088 || true
```

Observed result:

```text
curl: (7) Failed to connect to localhost port 8088 after 0 ms: Couldn't connect to server
```

## Redeploy verification

```bash
sudo docker ps
```

Observed result included container `be0db257c549`, image `nginx:alpine`, status `Up`, binding `0.0.0.0:8088->80/tcp`, and name `step34x-health-pdegb9g6obvbmmayzijiifjt-155959540822`.

```bash
curl -I http://localhost:8088
```

Observed result:

```text
HTTP/1.1 200 OK
Server: nginx/1.31.1
Content-Type: text/html
Content-Length: 896
```
