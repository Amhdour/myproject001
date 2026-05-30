# MinIO Durable Service

## Durable Service Contract

| Item | Value |
|---|---|
| Service name | `minio` |
| Network alias | `minio` |
| Internal API port | `9000` |
| Console port | `9001` internally; expose only if operationally needed |
| Required bucket | `onyx-file-store-bucket` |
| Data volume | `minio_data:/data` |
| Endpoint URL | `http://minio:9000` |

## Required File-Store Variables

```bash
FILE_STORE_BACKEND=s3
SERVICE_NAME_MINIO=minio
S3_ENDPOINT_URL=http://minio:9000
S3_FILE_STORE_BUCKET_NAME=onyx-file-store-bucket
```

## Credential Boundary

No real MinIO credentials are committed in the repository. Operators must inject MinIO root credentials and S3 client credentials through Coolify environment variables, host environment variables, or a non-committed env file.

## Durability Boundary

MinIO is durable through Compose/Coolify configuration when the override and `s3-filestore` profile are used. Step 62X does not claim this has been redeployed and proven on Oracle VPS.
