# Health After Deploy

## Status

No deploy occurred, so API and web/proxy health after custom-image deployment are `NOT VERIFIED`.

## Required Commands After Deployment

```bash
curl -i http://localhost:8000 || true
curl -i http://127.0.0.1:8000 || true
curl -i http://localhost:8088 || true
```

Also confirm MinIO remains available, API and background containers are running, and the web service remains at least as reachable as Step 50X. Do not convert the known web Docker healthcheck mismatch into a GO claim unless new evidence proves it is fixed.
