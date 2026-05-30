# MinIO File-Store Fix

## Original blocker

The Onyx API expected an S3-compatible file-store endpoint at `http://minio:9000`, but MinIO was initially missing from the Onyx Docker network.

Relevant API environment expectation:

```text
FILE_STORE_BACKEND=s3
SERVICE_NAME_MINIO=minio
S3_ENDPOINT_URL=http://minio:9000
S3_FILE_STORE_BUCKET_NAME=onyx-file-store-bucket
```

## Failure evidence

The API startup failed with a MinIO bucket endpoint error:

```text
botocore.exceptions.EndpointConnectionError: Could not connect to the endpoint URL: "http://minio:9000/onyx-file-store-bucket"
```

## Staging diagnostic fix

- A MinIO container was added manually to the Onyx Docker network.
- The container was given the network alias `minio`.
- The bucket `onyx-file-store-bucket` was created successfully.
- After restarting services, `api_server` became healthy.

## Architecture boundary

The manual MinIO addition is staging diagnostic evidence only. It is not a durable production architecture and should be converted into managed deployment configuration before any production or enterprise production-candidate claim.
