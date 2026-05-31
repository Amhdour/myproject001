# Operator Command Bundle

Run this on the Oracle VPS after the Step 62X durable Compose override has been applied. The bundle writes no secrets to the repository and avoids raw environment dumps.

```bash
OUT="$HOME/step63x-durable-compose-retry"
NETWORK="onyx_default"
: "${MINIO_ROOT_USER:?Set MINIO_ROOT_USER outside the repo before running Step 63X}"
: "${MINIO_ROOT_PASSWORD:?Set MINIO_ROOT_PASSWORD outside the repo before running Step 63X}"
mkdir -p "$OUT"

API_CONTAINER=$(docker ps --format "{{.Names}}" | grep '^onyx-api_server' | head -1)
BACKGROUND_CONTAINER=$(docker ps --format "{{.Names}}" | grep '^onyx-background' | head -1)
WEB_CONTAINER=$(docker ps --format "{{.Names}}" | grep '^onyx-web_server' | head -1)
MINIO_CONTAINER=$(docker ps --format "{{.Names}}" | grep '^onyx-minio' | head -1)

echo "API_CONTAINER=$API_CONTAINER" | tee "$OUT/containers.txt"
echo "BACKGROUND_CONTAINER=$BACKGROUND_CONTAINER" | tee -a "$OUT/containers.txt"
echo "WEB_CONTAINER=$WEB_CONTAINER" | tee -a "$OUT/containers.txt"
echo "MINIO_CONTAINER=$MINIO_CONTAINER" | tee -a "$OUT/containers.txt"

echo "=== deployed_images_final ===" | tee "$OUT/deployed_images_final.txt"
docker inspect "$API_CONTAINER" --format '{{.Config.Image}}' | tee -a "$OUT/deployed_images_final.txt"
docker inspect "$BACKGROUND_CONTAINER" --format '{{.Config.Image}}' | tee -a "$OUT/deployed_images_final.txt"

echo "=== runtime_code_check_final ===" | tee "$OUT/runtime_code_check_final.txt"
docker exec "$API_CONTAINER" sh -c 'test -d /app/backend/security_layer/runtime_enforcement && echo DEPLOYED_STEP39X_DIR_FOUND || echo DEPLOYED_STEP39X_DIR_MISSING' | tee -a "$OUT/runtime_code_check_final.txt"
docker exec "$API_CONTAINER" sh -c 'grep -R "_apply_step_39x_runtime_enforcement_hook" -n /app 2>/dev/null | head -20 || true' | tee -a "$OUT/runtime_code_check_final.txt"
docker exec "$API_CONTAINER" sh -c 'cd /app && python -m pytest backend/security_layer/tests/test_step_39x_runtime_enforcement.py -q' | tee -a "$OUT/runtime_code_check_final.txt" || echo "PYTEST_FAILED_OR_UNAVAILABLE" | tee -a "$OUT/runtime_code_check_final.txt"

echo "=== minio_bucket_final ===" | tee "$OUT/minio_bucket_final.txt"
docker run --rm --network "$NETWORK" -e MINIO_ROOT_USER -e MINIO_ROOT_PASSWORD --entrypoint /bin/sh minio/mc:latest -c 'mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" && mc mb -p local/onyx-file-store-bucket || true && mc ls local && mc ls local/onyx-file-store-bucket' | tee -a "$OUT/minio_bucket_final.txt" || echo "MINIO_BUCKET_CHECK_FAILED" | tee -a "$OUT/minio_bucket_final.txt"

echo "=== web_health_final ===" | tee "$OUT/web_health_final.txt"
docker inspect "$WEB_CONTAINER" --format '{{json .State.Health}}' | jq | tee -a "$OUT/web_health_final.txt" || true
docker exec "$WEB_CONTAINER" node -e "require('http').get('http://' + (process.env.WEB_HEALTHCHECK_HOST || require('os').hostname()) + ':3000/', (r) => { console.log('status=' + r.statusCode); process.exit(r.statusCode < 500 ? 0 : 1) }).on('error', (e) => { console.error(e.message); process.exit(1) })" | tee -a "$OUT/web_health_final.txt" || echo "WEB_HEALTHCHECK_MANUAL_FAILED" | tee -a "$OUT/web_health_final.txt"

echo "=== host_proxy_final ===" | tee "$OUT/host_proxy_final.txt"
curl -i http://localhost:8000 2>&1 | sed -E 's/(Set-Cookie: ).*/\1<REDACTED>/I' | tee -a "$OUT/host_proxy_final.txt" || true
curl -i http://127.0.0.1:8000 2>&1 | sed -E 's/(Set-Cookie: ).*/\1<REDACTED>/I' | tee -a "$OUT/host_proxy_final.txt" || true
curl -i http://localhost:8088 2>&1 | tee -a "$OUT/host_proxy_final.txt" || true

echo "=== status_final ===" | tee "$OUT/status_final.txt"
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" | grep -E "onyx-api_server|onyx-background|onyx-web_server|onyx-minio|coolify-proxy" | tee -a "$OUT/status_final.txt" || true

echo "=== classification_final ===" | tee "$OUT/classification_final.txt"
echo "If all required checks passed: ORACLE_DURABLE_COMPOSE_REDEPLOY_VERIFIED" | tee -a "$OUT/classification_final.txt"
echo "If any required check failed: ORACLE_DURABLE_COMPOSE_REDEPLOY_PARTIAL_GO_OR_NO_GO" | tee -a "$OUT/classification_final.txt"
```

## Notes

The `BACKGROUND_CONTAINER` assignment must be a complete shell command. If the shell prompt shows only `| grep '^onyx-background' | head -1)`, restart the bundle from the `API_CONTAINER=...` line because the pasted command was split.
