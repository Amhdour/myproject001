# Oracle VPS Redeploy Plan

These are user-run commands for the Oracle VPS. They are not claimed as executed by Step 62X.

## 1. Backup Current Containers and Config

```bash
mkdir -p ~/onyx-step62x-backup
cd /path/to/onyx/repo
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' | tee ~/onyx-step62x-backup/docker-ps-before.txt
docker compose -f deployment/docker_compose/docker-compose.yml ps | tee ~/onyx-step62x-backup/compose-ps-before.txt
cp deployment/docker_compose/docker-compose.yml ~/onyx-step62x-backup/docker-compose.yml.before
cp deployment/docker_compose/docker-compose.coolify-staging.yml ~/onyx-step62x-backup/docker-compose.coolify-staging.yml.before 2>/dev/null || true
```

## 2. Pull Latest Repo

```bash
cd /path/to/onyx/repo
git fetch origin
git checkout step-62x-durable-coolify-compose-deployment-architecture
git pull --ff-only origin step-62x-durable-coolify-compose-deployment-architecture
```

## 3. Verify Compose Files Exist

```bash
test -f deployment/docker_compose/docker-compose.yml
test -f deployment/docker_compose/docker-compose.oracle-staging.override.yml
test -f deployment/docker_compose/docker-compose.coolify-staging.yml
```

## 4. Set Required Staging Variables

```bash
export ONYX_BACKEND_IMAGE=rag-agent-security-onyx-backend:step53x-b77bee6
export FILE_STORE_BACKEND=s3
export SERVICE_NAME_MINIO=minio
export S3_ENDPOINT_URL=http://minio:9000
export S3_FILE_STORE_BUCKET_NAME=onyx-file-store-bucket
export MINIO_ROOT_USER='CHANGE_ME_OUTSIDE_REPO'
export MINIO_ROOT_PASSWORD='CHANGE_ME_OUTSIDE_REPO'
export S3_AWS_ACCESS_KEY_ID="$MINIO_ROOT_USER"
export S3_AWS_SECRET_ACCESS_KEY="$MINIO_ROOT_PASSWORD"
```

## 5. Validate Compose Render

```bash
docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore config > ~/onyx-step62x-backup/oracle-compose-config.txt
```

## 6. Deploy Using Selected Compose/Override

```bash
docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore up -d
```

## 7. Verify Container Images

```bash
docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore ps

docker inspect --format '{{.Name}} {{.Config.Image}}' \
  $(docker compose -f deployment/docker_compose/docker-compose.yml -f deployment/docker_compose/docker-compose.oracle-staging.override.yml --profile s3-filestore ps -q api_server background)
```

## 8. Verify MinIO Service and Bucket

```bash
docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore ps minio

docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore exec minio mc alias set local http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore exec minio mc mb --ignore-existing local/onyx-file-store-bucket

docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore exec minio mc ls local/onyx-file-store-bucket
```

## 9. Verify API Health

```bash
API_CONTAINER=$(docker compose -f deployment/docker_compose/docker-compose.yml -f deployment/docker_compose/docker-compose.oracle-staging.override.yml --profile s3-filestore ps -q api_server)
docker exec "$API_CONTAINER" python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8080/health').status)"
docker inspect --format '{{.Name}} {{.State.Health.Status}}' "$API_CONTAINER"
```

## 10. Verify Web Health

```bash
WEB_CONTAINER=$(docker compose -f deployment/docker_compose/docker-compose.yml -f deployment/docker_compose/docker-compose.oracle-staging.override.yml --profile s3-filestore ps -q web_server)
docker inspect --format '{{.Name}} {{json .Config.Healthcheck}} {{.State.Health.Status}}' "$WEB_CONTAINER"
docker exec "$WEB_CONTAINER" node -e "const http=require('http'),host=process.env.WEB_HEALTHCHECK_HOST||require('os').hostname();http.get('http://'+host+':3000/',r=>{console.log(r.statusCode);process.exit(r.statusCode<500?0:1)}).on('error',e=>{console.error(e.message);process.exit(1)})"
```

## 11. Verify Step 39X Runtime Code Inside API Container

```bash
docker exec "$API_CONTAINER" test -d /app/backend/security_layer/runtime_enforcement
docker exec "$API_CONTAINER" find /app/backend/security_layer/runtime_enforcement -maxdepth 2 -type f | sort | head -50
```

## 12. Host/Proxy Curl Checks

```bash
curl -i http://127.0.0.1:8000/ | head -40
curl -i http://127.0.0.1:8088/nginx-health | head -40
```

## 13. Rollback Command

This rollback command is included for retest safety.

```bash
export ONYX_BACKEND_IMAGE=onyxdotapp/onyx-backend:latest
docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore up -d
```
