# Compose Changes

## Files Changed

- `deployment/docker_compose/docker-compose.oracle-staging.override.yml`
  - Adds an Oracle staging override that keeps `api_server` and `background` on the same configurable backend image.
  - Makes MinIO a required dependency for `api_server` and `background` in the Oracle staging compose path.
  - Adds explicit file-store variables: `FILE_STORE_BACKEND=s3`, `SERVICE_NAME_MINIO=minio`, `S3_ENDPOINT_URL=http://minio:9000`, and `S3_FILE_STORE_BUCKET_NAME=onyx-file-store-bucket`.
  - Adds placeholder-only MinIO credential variables so real credentials are supplied by the deployment environment and are not committed.
  - Preserves the Step 61X web healthcheck override by allowing `WEB_HEALTHCHECK_HOST` to be set without changing the patched healthcheck command.
  - Adds explicit default network naming with `ONYX_COMPOSE_NETWORK_NAME` and a `minio` alias.
  - Relies on the base compose file for existing Postgres (`db_volume`) and OpenSearch (`opensearch-data`) volumes; Redis remains the base ephemeral cache configuration unless a later requirement explicitly changes cache persistence.

## Base Compose Compatibility

The existing compose files are left compatible with the normal Onyx flow. The override is only used when the Oracle staging deployment intentionally includes it.

## How to Use the Override

Example operator command for Oracle staging:

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
docker compose \
  -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml \
  --profile s3-filestore up -d
```

## Rollback Compatibility

Rollback can remove the override from the compose command or reset `ONYX_BACKEND_IMAGE` to `onyxdotapp/onyx-backend:latest`. The MinIO volume should be preserved unless the operator intentionally deletes staging test data.
