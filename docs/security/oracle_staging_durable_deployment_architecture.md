# Oracle Staging Durable Deployment Architecture

## Status

`DURABLE_DEPLOYMENT_ARCHITECTURE_READY_RETEST_PENDING`

This document summarizes the Step 62X durable Coolify/Compose architecture. It addresses simulated finding `SIM-F-004` by replacing diagnostic-only staging actions with repeatable Compose/Coolify configuration and operator runbooks.

## Selected Pattern

The selected pattern is Option B: a dedicated Compose override at `deployment/docker_compose/docker-compose.oracle-staging.override.yml`.

## Durable Components

- `api_server` and `background` use the same `ONYX_BACKEND_IMAGE` value.
- Oracle staging example: `rag-agent-security-onyx-backend:step53x-b77bee6`.
- MinIO is represented as the `minio` service with the `minio` network alias and `minio_data:/data` volume.
- Required bucket: `onyx-file-store-bucket`.
- Required file-store variables: `FILE_STORE_BACKEND=s3`, `SERVICE_NAME_MINIO=minio`, `S3_ENDPOINT_URL=http://minio:9000`, and `S3_FILE_STORE_BUCKET_NAME=onyx-file-store-bucket`.
- The Step 61X web healthcheck patch remains in the base compose files with `WEB_HEALTHCHECK_HOST` and `require('os').hostname()`.

## Claim Boundary

This architecture is ready for retest but is not claimed as verified on Oracle VPS in Step 62X. Production readiness is NO-GO, enterprise production-candidate readiness is NO-GO / 7–9%, external validation is simulated response only / real validation pending, and compliance certification is NOT CLAIMED.
